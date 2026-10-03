# FlexGrid MVP

A 72-hour, 15-minute-resolution simulation prototype for neighbourhood-scale renewable intermittency management.

Pipeline:
Solar + Demand -> Forecast -> Shortfall Detection -> Decision Engine -> Battery + Flexible Loads -> Reliability Metrics

Run:
    python -m pip install -r requirements.txt
    python run_simulation.py

Optional dashboard:
    streamlit run dashboard/dashboard.py

All numerical values are prototype assumptions, not measured field results.
