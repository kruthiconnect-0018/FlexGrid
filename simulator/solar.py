import numpy as np
import pandas as pd

def generate_solar_profile(config):
    steps = int(config.days * 24 * 60 / config.interval_minutes)
    timestamps = pd.date_range(
        start="2026-01-01 00:00:00",
        periods=steps,
        freq=f"{config.interval_minutes}min"
    )
    rng = np.random.default_rng(config.seed)

    cloud_factor = np.ones(config.days * 24 + 1)
    for _ in range(max(4, config.days * 3)):
        start = int(rng.integers(5, max(6, config.days * 24 - 4)))
        duration = int(rng.integers(1, 5))
        reduction = float(rng.uniform(0.25, 0.70))
        cloud_factor[start:min(start + duration, len(cloud_factor))] *= (1 - reduction)

    solar = []
    for ts in timestamps:
        hour = ts.hour + ts.minute / 60
        clear = np.sin(np.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 0.0
        elapsed_hours = (ts - timestamps[0]).total_seconds() / 3600
        left = int(np.floor(elapsed_hours))
        right = min(left + 1, len(cloud_factor) - 1)
        frac = elapsed_hours - left
        cloud = cloud_factor[left] * (1-frac) + cloud_factor[right] * frac
        power = max(0.0, config.solar_capacity_kw * max(0, clear) * cloud * rng.normal(1.0, 0.025))
        solar.append(power)

    return pd.DataFrame({"timestamp": timestamps, "solar_kw": solar})
