import numpy as np

def forecast_next_steps(data, current_index, horizon):
    recent = data.iloc[max(0, current_index-4):current_index]
    recent_demand = float(recent["demand_kw"].mean()) if len(recent) else float(data.iloc[current_index]["demand_kw"])
    recent_solar = float(recent["solar_kw"].mean()) if len(recent) else float(data.iloc[current_index]["solar_kw"])
    max_solar = max(float(data["solar_kw"].max()), 1.0)

    rows = []
    for offset in range(1, horizon + 1):
        idx = min(current_index + offset, len(data) - 1)
        ts = data.iloc[idx]["timestamp"]
        hour = ts.hour + ts.minute / 60
        clear = np.sin(np.pi * (hour - 6) / 12) if 6 <= hour <= 18 else 0.0
        factor = np.clip(recent_solar / max_solar, 0.35, 1.0) if clear > 0 else 1.0
        solar_forecast = max(0.0, max_solar * max(0, clear) * factor)
        demand_forecast = 0.7 * recent_demand + 0.3 * float(data.iloc[idx]["demand_kw"])
        rows.append((ts, solar_forecast, max(0.0, demand_forecast)))

    return rows
