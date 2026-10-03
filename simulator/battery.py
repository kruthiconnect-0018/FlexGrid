from dataclasses import dataclass

@dataclass
class Battery:
    capacity_kwh: float
    max_charge_kw: float
    max_discharge_kw: float
    soc: float
    reserve_soc: float
    charge_efficiency: float
    discharge_efficiency: float

    def energy_kwh(self):
        return self.capacity_kwh * self.soc

    def available_for_discharge_kwh(self):
        return max(0.0, self.energy_kwh() - self.capacity_kwh * self.reserve_soc)

    def charge(self, requested_kw, interval_hours):
        requested_kw = max(0.0, min(requested_kw, self.max_charge_kw))
        room = max(0.0, self.capacity_kwh - self.energy_kwh())
        max_kw = room / (interval_hours * self.charge_efficiency)
        actual = min(requested_kw, max_kw)
        self.soc = min(1.0, self.soc + actual * interval_hours * self.charge_efficiency / self.capacity_kwh)
        return actual

    def discharge(self, requested_kw, interval_hours):
        requested_kw = max(0.0, min(requested_kw, self.max_discharge_kw))
        available = self.available_for_discharge_kwh()
        max_kw = available * self.discharge_efficiency / interval_hours
        actual = min(requested_kw, max_kw)
        self.soc = max(self.reserve_soc, self.soc - actual * interval_hours / (self.capacity_kwh * self.discharge_efficiency))
        return actual
