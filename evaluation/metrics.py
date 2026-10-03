def calculate_metrics(results):
    h = results["interval_hours"].iloc[0]
    base = results["baseline_shortfall_kw"].sum() * h
    flex = results["flexgrid_unmet_kw"].sum() * h
    base_steps = (results["baseline_shortfall_kw"] > 0).sum()
    flex_steps = (results["flexgrid_unmet_kw"] > 0).sum()
    total = len(results)

    return {
        "Baseline unmet energy (kWh)": base,
        "FlexGrid unmet energy (kWh)": flex,
        "Unmet energy reduction (%)": (1 - flex / max(base, 1e-9)) * 100,
        "Baseline supply availability (%)": (1 - base_steps / total) * 100,
        "FlexGrid supply availability (%)": (1 - flex_steps / total) * 100,
        "Peak demand (kW)": results["demand_kw"].max(),
        "Peak residual demand after FlexGrid (kW)": results["flexgrid_net_demand_kw"].max(),
        "Battery minimum SOC (%)": results["battery_soc"].min() * 100,
        "Battery maximum SOC (%)": results["battery_soc"].max() * 100,
        "Total shifted load (kWh)": results["load_shift_kw"].sum() * h,
        "Total battery discharge (kWh)": results["battery_discharge_kw"].sum() * h,
        "Total battery charge (kWh)": results["battery_charge_kw"].sum() * h,
    }
