from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="FlexGrid Dashboard", layout="wide")
st.title("FlexGrid — Neighbourhood Energy Flexibility")
st.caption("Simulation dashboard")

out = Path("outputs")
if not (out / "simulation_results.csv").exists():
    st.warning("Run `python run_simulation.py` first.")
    st.stop()

r = pd.read_csv(out / "simulation_results.csv")
m = pd.read_csv(out / "metrics.csv")
mm = dict(zip(m.Metric, m.Value))

a,b,c,d = st.columns(4)
a.metric("Baseline unmet energy", f"{mm['Baseline unmet energy (kWh)']:.1f} kWh")
b.metric("FlexGrid unmet energy", f"{mm['FlexGrid unmet energy (kWh)']:.1f} kWh")
c.metric("Unmet energy reduction", f"{mm['Unmet energy reduction (%)']:.1f}%")
d.metric("FlexGrid availability", f"{mm['FlexGrid supply availability (%)']:.1f}%")

st.subheader("Solar vs Demand")
st.line_chart(r.set_index("timestamp")[["solar_kw", "demand_kw"]])

st.subheader("Baseline vs FlexGrid Shortfall")
st.line_chart(r.set_index("timestamp")[["baseline_shortfall_kw", "flexgrid_unmet_kw"]])

st.subheader("Battery SOC")
st.line_chart(r.set_index("timestamp")[["battery_soc"]] * 100)

st.subheader("Battery Dispatch")
st.line_chart(r.set_index("timestamp")[["battery_charge_kw", "battery_discharge_kw"]])

st.subheader("Flexible Load Shifting")
st.line_chart(r.set_index("timestamp")[["load_shift_kw"]])

st.subheader("Metrics")
st.dataframe(m, use_container_width=True)
