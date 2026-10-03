def decide_action(forecast, battery, min_shortfall_kw, flexible_shift_limit_kw, battery_target_soc):
    if not forecast:
        return {"load_shift_kw": 0.0, "battery_charge_kw": 0.0, "battery_discharge_kw": 0.0}

    _, solar, demand = forecast[0]
    current_shortfall = max(0.0, demand - solar)
    future_shortfall = max(0.0, max(d - s for _, s, d in forecast))

    if current_shortfall >= min_shortfall_kw:
        shift = min(current_shortfall * 0.45, flexible_shift_limit_kw)
        discharge = min(current_shortfall - shift, battery.max_discharge_kw)
        return {"load_shift_kw": shift, "battery_charge_kw": 0.0, "battery_discharge_kw": discharge}

    excess = max(0.0, solar - demand)
    if excess > 0 and future_shortfall >= min_shortfall_kw and battery.soc < battery_target_soc:
        return {"load_shift_kw": 0.0, "battery_charge_kw": min(excess, battery.max_charge_kw), "battery_discharge_kw": 0.0}

    return {"load_shift_kw": 0.0, "battery_charge_kw": 0.0, "battery_discharge_kw": 0.0}
