import numpy as np
import pandas as pd

def generate_demand_profile(config):
    steps = int(config.days * 24 * 60 / config.interval_minutes)
    timestamps = pd.date_range(
        start="2026-01-01 00:00:00",
        periods=steps,
        freq=f"{config.interval_minutes}min"
    )
    rng = np.random.default_rng(config.seed + 1)

    total, flexible, critical = [], [], []

    for ts in timestamps:
        hour = ts.hour + ts.minute / 60
        demand = config.base_demand_kw

        if 6 <= hour < 10:
            demand += 16
        elif 10 <= hour < 18:
            demand += 9
        elif 18 <= hour < 23:
            demand += 30
        else:
            demand += 2

        demand += rng.normal(0, 2.0)
        demand = max(demand, 1.0)

        flex = min(config.flexible_load_kw, max(0.0, demand * 0.18))
        crit = min(config.critical_load_kw, demand * 0.55)

        total.append(demand)
        flexible.append(flex)
        critical.append(crit)

    return pd.DataFrame({
        "timestamp": timestamps,
        "demand_kw": total,
        "flexible_load_kw": flexible,
        "critical_load_kw": critical
    })
