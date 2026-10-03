def decide_action(
    forecast,
    battery,
    min_shortfall_kw,
    flexible_shift_limit_kw,
    battery_target_soc
):
    """
    Forecast-aware rule-based FlexGrid controller.

    Decision priority:
    1. Detect the current renewable shortfall.
    2. Reduce flexible demand first.
    3. Use the community battery for the remaining shortfall.
    4. During renewable excess, charge the battery if a future
       shortfall is predicted.
    5. Respect the battery reserve and target SOC.

    Returns:
        dict containing:
        - load_shift_kw
        - battery_charge_kw
        - battery_discharge_kw
    """

    # No forecast available -> no action
    if not forecast:
        return {
            "load_shift_kw": 0.0,
            "battery_charge_kw": 0.0,
            "battery_discharge_kw": 0.0
        }

    # ---------------------------------------------------------
    # CURRENT AND FUTURE CONDITIONS
    # ---------------------------------------------------------

    _, current_solar, current_demand = forecast[0]

    current_shortfall = max(
        0.0,
        current_demand - current_solar
    )

    future_shortfall = max(
        0.0,
        max(
            demand - solar
            for _, solar, demand in forecast
        )
    )

    # ---------------------------------------------------------
    # CASE 1: CURRENT RENEWABLE SHORTFALL
    # ---------------------------------------------------------

    if current_shortfall >= min_shortfall_kw:

        # First use flexible demand.
        #
        # We do not shift more than:
        # - 45% of the current shortfall
        # - configured flexible-load limit
        requested_shift = current_shortfall * 0.45

        load_shift = min(
            requested_shift,
            flexible_shift_limit_kw
        )

        remaining_shortfall = max(
            0.0,
            current_shortfall - load_shift
        )

        # -----------------------------------------------------
        # BATTERY DISCHARGE
        # -----------------------------------------------------

        battery_discharge = 0.0

        # Do not intentionally discharge when the battery is
        # already at/below its reserve SOC.
        #
        # getattr() keeps the controller compatible with the
        # existing Battery implementation.
        current_soc = getattr(battery, "soc", 0.0)
        reserve_soc = getattr(battery, "reserve_soc", 0.20)

        if (
            remaining_shortfall > 0
            and current_soc > reserve_soc
        ):
            battery_discharge = min(
                remaining_shortfall,
                battery.max_discharge_kw
            )

        return {
            "load_shift_kw": load_shift,
            "battery_charge_kw": 0.0,
            "battery_discharge_kw": battery_discharge
        }

    # ---------------------------------------------------------
    # CASE 2: RENEWABLE EXCESS
    # ---------------------------------------------------------

    renewable_excess = max(
        0.0,
        current_solar - current_demand
    )

    # If renewable energy is available and a future shortfall
    # is expected, store some of that energy.
    if (
        renewable_excess > 0
        and future_shortfall >= min_shortfall_kw
        and getattr(battery, "soc", 0.0) < battery_target_soc
    ):

        battery_charge = min(
            renewable_excess,
            battery.max_charge_kw
        )

        return {
            "load_shift_kw": 0.0,
            "battery_charge_kw": battery_charge,
            "battery_discharge_kw": 0.0
        }

    # ---------------------------------------------------------
    # CASE 3: NO FLEXIBILITY ACTION REQUIRED
    # ---------------------------------------------------------

    return {
        "load_shift_kw": 0.0,
        "battery_charge_kw": 0.0,
        "battery_discharge_kw": 0.0
    }