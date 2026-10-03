from config import CONFIG
from simulator.solar import generate_solar_profile
from simulator.demand import generate_demand_profile

def test_solar():
    d = generate_solar_profile(CONFIG)
    assert len(d) > 0
    assert (d.solar_kw >= 0).all()

def test_demand():
    d = generate_demand_profile(CONFIG)
    assert (d.demand_kw > 0).all()
    assert (d.critical_load_kw <= d.demand_kw).all()
