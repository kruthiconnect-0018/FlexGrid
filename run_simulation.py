from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from config import CONFIG
from simulator.solar import generate_solar_profile
from simulator.demand import generate_demand_profile
from simulator.battery import Battery
from forecasting.forecast import forecast_next_steps
from optimization.controller import decide_action
from evaluation.metrics import calculate_metrics

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

def main():
    solar = generate_solar_profile(CONFIG)
    demand = generate_demand_profile(CONFIG)
    data = solar.merge(demand, on="timestamp")
    data["baseline_shortfall_kw"] = (data.demand_kw - data.solar_kw).clip(lower=0)

    battery = Battery(
        CONFIG.battery_capacity_kwh, CONFIG.battery_max_charge_kw,
        CONFIG.battery_max_discharge_kw, CONFIG.battery_initial_soc,
        CONFIG.battery_reserve_soc, CONFIG.battery_charge_efficiency,
        CONFIG.battery_discharge_efficiency
    )
    h = CONFIG.interval_minutes / 60
    records = []

    for i in range(len(data)):
        row = data.iloc[i]
        fc = forecast_next_steps(data, i, CONFIG.forecast_horizon_steps)
        action = decide_action(
            fc, battery, CONFIG.min_shortfall_kw,
            CONFIG.flexible_shift_limit_kw, CONFIG.battery_target_soc
        )

        shift = min(action["load_shift_kw"], row.flexible_load_kw)
        excess = max(0, row.solar_kw - row.demand_kw)
        charge = battery.charge(min(action["battery_charge_kw"], excess), h)

        residual_demand = max(0, row.demand_kw - shift)
        residual_shortfall = max(0, residual_demand - row.solar_kw)
        discharge = battery.discharge(
            min(action["battery_discharge_kw"], residual_shortfall), h
        )
        unmet = max(0, residual_shortfall - discharge)

        records.append({
            "timestamp": row.timestamp,
            "solar_kw": row.solar_kw,
            "demand_kw": row.demand_kw,
            "flexible_load_kw": row.flexible_load_kw,
            "critical_load_kw": row.critical_load_kw,
            "baseline_shortfall_kw": row.baseline_shortfall_kw,
            "load_shift_kw": shift,
            "battery_charge_kw": charge,
            "battery_discharge_kw": discharge,
            "battery_soc": battery.soc,
            "flexgrid_unmet_kw": unmet,
            "flexgrid_net_demand_kw": residual_demand,
            "interval_hours": h
        })

    results = pd.DataFrame(records)
    metrics = calculate_metrics(results)

    results.to_csv(OUT / "simulation_results.csv", index=False)
    pd.DataFrame(metrics.items(), columns=["Metric", "Value"]).to_csv(
        OUT / "metrics.csv", index=False
    )

    plots = [
        ("01_solar_vs_demand.png", ["solar_kw", "demand_kw"],
         "Solar Generation vs Neighbourhood Demand", "Power (kW)"),
        ("02_baseline_vs_flexgrid.png", ["baseline_shortfall_kw", "flexgrid_unmet_kw"],
         "Baseline vs FlexGrid Shortfall", "Shortfall (kW)"),
        ("03_battery_soc.png", ["battery_soc"],
         "Community Battery State of Charge", "SOC"),
        ("04_battery_dispatch.png", ["battery_charge_kw", "battery_discharge_kw"],
         "Community Battery Dispatch", "Power (kW)"),
        ("05_load_shifting.png", ["load_shift_kw"],
         "Flexible Load Shifting", "Power (kW)")
    ]

    for filename, cols, title, ylabel in plots:
        plt.figure(figsize=(13, 5))
        for col in cols:
            series = results[col] * 100 if col == "battery_soc" else results[col]
            plt.plot(results["timestamp"], series, label=col.replace("_", " ").title())
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel(ylabel)
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(OUT / filename, dpi=180)
        plt.close()

    print("\n=== FLEXGRID SIMULATION ===")
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}")
    print("\nOutputs saved in outputs/")

if __name__ == "__main__":
    main()
