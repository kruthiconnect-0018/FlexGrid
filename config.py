from dataclasses import dataclass

@dataclass
class SimulationConfig:
    days: int = 3
    interval_minutes: int = 15
    seed: int = 42
    households: int = 100
    solar_capacity_kw: float = 100.0
    base_demand_kw: float = 42.0
    flexible_load_kw: float = 15.0
    critical_load_kw: float = 25.0
    battery_capacity_kwh: float = 200.0
    battery_max_charge_kw: float = 50.0
    battery_max_discharge_kw: float = 50.0
    battery_initial_soc: float = 0.70
    battery_reserve_soc: float = 0.20
    battery_charge_efficiency: float = 0.95
    battery_discharge_efficiency: float = 0.95
    forecast_horizon_steps: int = 8
    min_shortfall_kw: float = 2.0
    flexible_shift_limit_kw: float = 15.0
    battery_target_soc: float = 0.35

CONFIG = SimulationConfig()
