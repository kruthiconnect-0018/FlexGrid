import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FlexGrid | Energy Operations",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"

RESULTS_FILE = OUTPUT_DIR / "simulation_results.csv"
METRICS_FILE = OUTPUT_DIR / "metrics.csv"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_results():
    return pd.read_csv(RESULTS_FILE, parse_dates=["timestamp"])


@st.cache_data
def load_metrics():
    df = pd.read_csv(METRICS_FILE)
    return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))


try:
    results = load_results()
    metrics = load_metrics()
except Exception as e:
    st.error(
        "Unable to load simulation data. "
        "Run `python run_simulation.py` first."
    )
    st.exception(e)
    st.stop()


# ============================================================
# HELPER
# ============================================================

def metric_value(name, default=0):
    value = metrics.get(name, default)

    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def format_number(value, decimals=1):
    return f"{value:,.{decimals}f}"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background-color: #101827;
    }

    section[data-testid="stSidebar"] * {
        color: #e8edf5;
    }

    .sidebar-brand {
        padding: 10px 5px 25px 5px;
    }

    .brand-symbol {
        font-size: 32px;
        font-weight: 800;
        color: #f5b942;
    }

    .brand-name {
        font-size: 24px;
        font-weight: 800;
        color: white;
        margin-top: -4px;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 5px;
    }

    .sidebar-section {
        color: #64748b;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 28px;
        margin-bottom: 8px;
    }

    /* ---------- HEADER ---------- */

    .eyebrow {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .page-title {
        color: #111827;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    .page-subtitle {
        color: #64748b;
        font-size: 15px;
        margin-top: 8px;
        margin-bottom: 24px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
        border-radius: 20px;
        padding: 7px 13px;
        font-size: 12px;
        font-weight: 700;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        display: inline-block;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    .kpi-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .kpi-value {
        color: #111827;
        font-size: 29px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    .kpi-unit {
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 11px;
        margin-top: 8px;
    }

    /* ---------- SECTION ---------- */

    .section-title {
        color: #111827;
        font-size: 21px;
        font-weight: 750;
        margin-top: 28px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 15px;
    }

    /* ---------- INSIGHT CARD ---------- */

    .insight {
        background: white;
        border-left: 4px solid #f5b942;
        border-radius: 10px;
        padding: 16px 18px;
        margin: 10px 0;
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
    }

    .insight-title {
        font-weight: 750;
        color: #111827;
        font-size: 14px;
    }

    .insight-text {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
        line-height: 1.5;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-symbol">⚡</div>
            <div class="brand-name">FlexGrid</div>
            <div class="brand-subtitle">
                Neighbourhood Energy Flexibility Platform
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-section">NAVIGATION</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Reliability",
            "Battery",
            "Flexible Loads",
            "Simulation Data",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-section">SIMULATION</div>',
        unsafe_allow_html=True,
    )

    st.caption("Model status")
    st.success("Simulation data loaded")

    st.caption(
        f"Time horizon: "
        f"{results['timestamp'].min().strftime('%d %b')} → "
        f"{results['timestamp'].max().strftime('%d %b')}"
    )

    st.caption(
        f"Intervals: {len(results)}"
    )


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        '<div class="eyebrow">ENERGY OPERATIONS / SIMULATION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">Neighbourhood Energy Control</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="page-subtitle">
        Forecast renewable availability, coordinate community storage,
        shift flexible demand and protect local electricity supply.
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_right:

    st.markdown(
        """
        <div style="text-align:right; padding-top:10px;">
            <span class="status-pill">
                <span class="status-dot"></span>
                SIMULATION RUN
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# KPI SECTION
# ============================================================

baseline_unmet = metric_value(
    "Baseline unmet energy (kWh)"
)

flexgrid_unmet = metric_value(
    "FlexGrid unmet energy (kWh)"
)

reduction = metric_value(
    "Unmet energy reduction (%)"
)

availability = metric_value(
    "FlexGrid supply availability (%)"
)

peak_demand = metric_value(
    "Peak demand (kW)"
)

min_soc = metric_value(
    "Battery minimum SOC (%)"
)

max_soc = metric_value(
    "Battery maximum SOC (%)"
)

shifted_load = metric_value(
    "Total shifted load (kWh)"
)


k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">BASELINE UNMET ENERGY</div>
            <div class="kpi-value">
                {format_number(baseline_unmet)}
                <span class="kpi-unit">kWh</span>
            </div>
            <div class="kpi-description">
                Without coordinated flexibility
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">FLEXGRID UNMET ENERGY</div>
            <div class="kpi-value">
                {format_number(flexgrid_unmet)}
                <span class="kpi-unit">kWh</span>
            </div>
            <div class="kpi-description">
                After battery + load flexibility
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">UNMET ENERGY REDUCTION</div>
            <div class="kpi-value">
                {format_number(reduction)}
                <span class="kpi-unit">%</span>
            </div>
            <div class="kpi-description">
                Improvement versus baseline
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">SUPPLY AVAILABILITY</div>
            <div class="kpi-value">
                {format_number(availability)}
                <span class="kpi-unit">%</span>
            </div>
            <div class="kpi-description">
                FlexGrid simulation result
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="section-title">Neighbourhood Energy Balance</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
        Renewable generation is compared with neighbourhood demand.
        FlexGrid responds when available supply falls below demand.
        </div>
        """,
        unsafe_allow_html=True,
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["solar_kw"],
            name="Solar Supply",
            mode="lines",
            line=dict(width=2.5),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["demand_kw"],
            name="Demand",
            mode="lines",
            line=dict(width=2.5),
        )
    )

    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=20, b=10),
        hovermode="x unified",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        legend=dict(
            orientation="h",
            y=1.08,
            x=0,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Reliability Impact</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=results["timestamp"],
                y=results["baseline_shortfall_kw"],
                name="Baseline",
                mode="lines",
                line=dict(width=2),
            )
        )

        fig.add_trace(
            go.Scatter(
                x=results["timestamp"],
                y=results["flexgrid_unmet_kw"],
                name="FlexGrid",
                mode="lines",
                line=dict(width=2),
            )
        )

        fig.update_layout(
            title="Shortfall Before vs After FlexGrid",
            height=360,
            margin=dict(l=10, r=10, t=45, b=10),
            hovermode="x unified",
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Time",
            yaxis_title="Unmet Power (kW)",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with c2:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=results["timestamp"],
                y=results["battery_soc"] * 100,
                name="Battery SOC",
                mode="lines",
                line=dict(width=2.5),
                fill="tozeroy",
            )
        )

        fig.update_layout(
            title="Community Battery State of Charge",
            height=360,
            margin=dict(l=10, r=10, t=45, b=10),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title="Time",
            yaxis_title="SOC (%)",
            yaxis=dict(range=[0, 100]),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">
                FlexGrid intervention
            </div>
            <div class="insight-text">
                The simulation reduced unmet energy by
                <b>{format_number(reduction)}%</b>
                compared with the baseline through coordinated
                battery dispatch and flexible-load shifting.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# RELIABILITY
# ============================================================

elif page == "Reliability":

    st.markdown(
        '<div class="section-title">Reliability Analysis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
        Measures how FlexGrid responds to renewable intermittency
        and reduces electricity shortfalls.
        </div>
        """,
        unsafe_allow_html=True,
    )

    baseline_availability = metric_value(
        "Baseline supply availability (%)"
    )

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Baseline availability",
            f"{baseline_availability:.1f}%"
        )

    with r2:
        st.metric(
            "FlexGrid availability",
            f"{availability:.1f}%"
        )

    with r3:
        st.metric(
            "Unmet energy reduction",
            f"{reduction:.1f}%"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["baseline_shortfall_kw"],
            name="Baseline shortfall",
            mode="lines",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["flexgrid_unmet_kw"],
            name="FlexGrid unmet",
            mode="lines",
            line=dict(width=2),
        )
    )

    fig.update_layout(
        height=500,
        hovermode="x unified",
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Time",
        yaxis_title="Shortfall (kW)",
        margin=dict(l=10, r=10, t=20, b=10),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-title">
                What this shows
            </div>
            <div class="insight-text">
                The blue baseline represents unmet demand without
                coordinated flexibility. The FlexGrid curve represents
                the remaining unmet demand after the controller uses
                flexible loads and community battery storage.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# BATTERY
# ============================================================

elif page == "Battery":

    st.markdown(
        '<div class="section-title">Community Battery</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
        Monitor battery state of charge and dispatch decisions
        throughout the simulation.
        </div>
        """,
        unsafe_allow_html=True,
    )

    b1, b2, b3 = st.columns(3)

    with b1:
        st.metric(
            "Minimum SOC",
            f"{min_soc:.1f}%"
        )

    with b2:
        st.metric(
            "Maximum SOC",
            f"{max_soc:.1f}%"
        )

    with b3:
        st.metric(
            "Battery discharge",
            f"{metric_value('Total battery discharge (kWh)'):.1f} kWh"
        )

    # SOC

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["battery_soc"] * 100,
            name="Battery SOC",
            mode="lines",
            line=dict(width=2.5),
            fill="tozeroy",
        )
    )

    fig.update_layout(
        title="Battery State of Charge",
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        yaxis_title="SOC (%)",
        xaxis_title="Time",
        yaxis=dict(range=[0, 100]),
        margin=dict(l=10, r=10, t=50, b=10),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # Dispatch

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["battery_charge_kw"],
            name="Charging",
            mode="lines",
            line=dict(width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["battery_discharge_kw"],
            name="Discharging",
            mode="lines",
            line=dict(width=2),
        )
    )

    fig.update_layout(
        title="Battery Dispatch",
        height=420,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        yaxis_title="Power (kW)",
        xaxis_title="Time",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# FLEXIBLE LOADS
# ============================================================

elif page == "Flexible Loads":

    st.markdown(
        '<div class="section-title">Flexible Demand</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
        Flexible electricity demand can be shifted away from
        renewable shortfall periods while preserving critical loads.
        </div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2 = st.columns(2)

    with f1:
        st.metric(
            "Total shifted load",
            f"{shifted_load:.1f} kWh"
        )

    with f2:
        st.metric(
            "Peak demand",
            f"{peak_demand:.1f} kW"
        )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=results["timestamp"],
            y=results["load_shift_kw"],
            name="Flexible load shifted",
            mode="lines",
            line=dict(width=2.5),
            fill="tozeroy",
        )
    )

    fig.update_layout(
        title="Flexible Load Shifting",
        height=450,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        xaxis_title="Time",
        yaxis_title="Shifted Power (kW)",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="insight">
            <div class="insight-title">
                Demand-side flexibility
            </div>
            <div class="insight-text">
                FlexGrid temporarily shifts eligible electricity
                consumption during shortage periods. Examples include
                EV charging, water pumping and other deferrable loads.
                Critical loads are not intentionally shifted.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SIMULATION DATA
# ============================================================

elif page == "Simulation Data":

    st.markdown(
        '<div class="section-title">Simulation Data</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-description">
        Raw simulation output used to generate the dashboard metrics.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        results,
        use_container_width=True,
        height=550,
    )

    st.download_button(
        label="Download Simulation CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="flexgrid_simulation_results.csv",
        mime="text/csv",
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        FLEXGRID · Neighbourhood Energy Flexibility
        · Simulation Prototype · Yuva Yodha 2026
    </div>
    """,
    unsafe_allow_html=True,
)