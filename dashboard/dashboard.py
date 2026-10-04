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
# THEME TOKENS
# ============================================================
 
YELLOW = "#FFC21A"
YELLOW_SOFT = "#FFF4CC"
INK = "#14120B"
MUTED = "#7A776C"
LINE = "#ECEAE3"
BG = "#F5F4F0"
GREEN = "#22A06B"
GREY_LINE = "#B9B6AA"
 
 
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
# HELPERS
# ============================================================
 
def metric_value(name, default=0):
    value = metrics.get(name, default)
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
 
 
def format_number(value, decimals=1):
    return f"{value:,.{decimals}f}"
 
 
def style_chart(fig, title=None, height=380, y_title="", y_range=None):
    """Apply one consistent look to every chart."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color=INK, family="Plus Jakarta Sans"),
            x=0.01,
        ) if title else None,
        height=height,
        margin=dict(l=10, r=10, t=55 if title else 20, b=10),
        hovermode="x unified",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Plus Jakarta Sans", color=MUTED, size=12),
        legend=dict(
            orientation="h", y=1.12 if title else 1.08, x=1, xanchor="right",
            font=dict(size=12, color=INK),
        ),
        hoverlabel=dict(bgcolor=INK, font_color="white", bordercolor=INK),
        xaxis=dict(showgrid=False, showline=True, linecolor=LINE, title=None),
        yaxis=dict(
            gridcolor=LINE, zeroline=False, title=y_title,
            range=y_range,
        ),
    )
    return fig
 
 
def line(fig, x, y, name, color, width=2.5, fill=None, dash=None):
    fig.add_trace(
        go.Scatter(
            x=x, y=y, name=name, mode="lines",
            line=dict(width=width, color=color, dash=dash, shape="spline", smoothing=0.4),
            fill=fill,
            fillcolor="rgba(255,194,26,0.18)" if fill else None,
        )
    )
 
 
def show(fig):
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
 
 
def gauge(value, baseline, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number=dict(suffix="%", font=dict(size=44, color=INK, family="Plus Jakarta Sans")),
        title=dict(text=title, font=dict(size=15, color=INK, family="Plus Jakarta Sans")),
        gauge=dict(
            axis=dict(range=[0, 100], tickcolor=GREY_LINE, tickfont=dict(size=11, color=MUTED)),
            bar=dict(color=YELLOW, thickness=0.28),
            bgcolor="#F1EFE8",
            borderwidth=0,
            threshold=dict(line=dict(color=INK, width=4), thickness=0.85, value=baseline),
        ),
    ))
    fig.update_layout(
        height=300, margin=dict(l=30, r=30, t=60, b=10),
        paper_bgcolor="white", font=dict(family="Plus Jakarta Sans"),
    )
    return fig
 
 
def summary_card(saved, availability, peak, shifted, min_soc, max_soc):
    return f"""
    <div class="summary-card">
        <div class="summary-head">
            <div class="summary-icon">⚡</div>
            <div>
                <div class="summary-title">Energy protected by FlexGrid</div>
                <div class="summary-sub">Unmet demand avoided vs baseline</div>
            </div>
        </div>
        <div class="summary-value">{format_number(saved)}<span>kWh</span></div>
        <div class="summary-bar"><div style="width:{max(min(availability,100),0)}%"></div></div>
        <div class="summary-stats">
            <div><span>Peak demand</span><b>{format_number(peak)} kW</b></div>
            <div><span>Load shifted</span><b>{format_number(shifted)} kWh</b></div>
            <div><span>Battery range</span><b>{min_soc:.0f}-{max_soc:.0f}%</b></div>
        </div>
        <div class="summary-strip">
            Battery and flexible loads covered {format_number(saved)} kWh that would otherwise go unserved.
        </div>
    </div>
    """
 
 
def section(title, description=""):
    st.markdown(
        f'<div class="section-title">{title}</div>'
        f'<div class="section-description">{description}</div>',
        unsafe_allow_html=True,
    )
 
 
def insight(title, text):
    st.markdown(
        f"""
        <div class="insight">
            <div class="insight-icon">⚡</div>
            <div>
                <div class="insight-title">{title}</div>
                <div class="insight-text">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
def stat_card(label, value, unit, desc, icon):
    return f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}<span class="kpi-unit">{unit}</span></div>
        <div class="kpi-description">{desc}</div>
    </div>
    """
 
 
# ============================================================
# CUSTOM CSS
# ============================================================
 
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
 
    html, body, [class*="css"], .stApp, button, input {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
 
    /* ---------- GLOBAL ---------- */
    .stApp {{ background-color: {BG}; }}
    header[data-testid="stHeader"] {{ background: transparent; }}
    #MainMenu, footer {{ visibility: hidden; }}
 
    .block-container {{
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}
 
    /* Charts sit inside white rounded cards */
    div[data-testid="stPlotlyChart"] {{
        background: white;
        border: 1px solid {LINE};
        border-radius: 20px;
        padding: 14px 10px 4px 10px;
        overflow: hidden;
    }}
 
    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {{
        background-color: {INK};
        border-right: none;
    }}
    section[data-testid="stSidebar"] * {{ color: #e9e6dc; }}
 
    .sidebar-brand {{
        display: flex; align-items: center; gap: 12px;
        padding: 6px 4px 8px 4px;
    }}
    .brand-symbol {{
        width: 42px; height: 42px; border-radius: 14px;
        background: {YELLOW};
        display: flex; align-items: center; justify-content: center;
        font-size: 22px;
    }}
    .brand-name {{ font-size: 21px; font-weight: 800; color: white !important; line-height: 1.1; }}
    .brand-subtitle {{ color: #8d897b !important; font-size: 11px; line-height: 1.4; }}
 
    .sidebar-section {{
        color: #7d7a6d !important;
        font-size: 12px; font-weight: 600;
        margin: 30px 0 10px 4px;
    }}
 
    /* Navigation radio -> pill menu */
    section[data-testid="stSidebar"] div[role="radiogroup"] {{ gap: 6px; }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        width: 100%;
        padding: 11px 14px;
        border-radius: 14px;
        cursor: pointer;
        transition: background .15s ease;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: #24211a;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
        display: none;  /* hide radio circle */
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 14px; font-weight: 600;
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background: {YELLOW};
    }}
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
        color: {INK} !important; font-weight: 800;
    }}
 
    section[data-testid="stSidebar"] div[data-testid="stAlert"] {{
        background: #1f2a22; border: 1px solid #2c4434; border-radius: 14px;
    }}
 
    /* ---------- HEADER ---------- */
    .page-title {{
        color: {INK}; font-size: 36px; font-weight: 800;
        letter-spacing: -1px; margin: 0; line-height: 1.15;
    }}
    .page-subtitle {{
        color: {MUTED}; font-size: 15px;
        margin: 8px 0 26px 0; max-width: 680px; line-height: 1.55;
    }}
    .status-pill {{
        display: inline-flex; align-items: center; gap: 8px;
        background: {INK}; color: white;
        border-radius: 30px; padding: 9px 16px;
        font-size: 12px; font-weight: 700;
    }}
    .status-dot {{
        width: 8px; height: 8px; background: {YELLOW};
        border-radius: 50%; display: inline-block;
        box-shadow: 0 0 0 4px rgba(255,194,26,.25);
    }}
 
    /* ---------- KPI CARDS ---------- */
    .kpi-card {{
        background: white;
        border: 1px solid {LINE};
        border-radius: 20px;
        padding: 20px 22px;
        min-height: 150px;
    }}
    .kpi-top {{ display: flex; justify-content: space-between; align-items: center; }}
    .kpi-label {{ color: {MUTED}; font-size: 13px; font-weight: 600; }}
    .kpi-icon {{
        width: 34px; height: 34px; border-radius: 50%;
        background: {YELLOW_SOFT};
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
    }}
    .kpi-value {{
        color: {INK}; font-size: 34px; font-weight: 800;
        letter-spacing: -1px; margin-top: 14px;
    }}
    .kpi-unit {{ color: {MUTED}; font-size: 14px; font-weight: 600; margin-left: 5px; letter-spacing: 0; }}
    .kpi-description {{ color: #a09d90; font-size: 12px; margin-top: 6px; }}
 
    /* Highlighted (hero) KPI */
    .kpi-card.hero {{ background: {YELLOW}; border-color: {YELLOW}; }}
    .kpi-card.hero .kpi-label {{ color: rgba(20,18,11,.7); }}
    .kpi-card.hero .kpi-icon {{ background: {INK}; color: {YELLOW}; }}
    .kpi-card.hero .kpi-unit {{ color: rgba(20,18,11,.65); }}
    .kpi-card.hero .kpi-description {{ color: rgba(20,18,11,.6); }}
 
    /* ---------- SECTIONS ---------- */
    .section-title {{
        color: {INK}; font-size: 22px; font-weight: 800;
        letter-spacing: -.4px; margin-top: 34px; margin-bottom: 4px;
    }}
    .section-description {{
        color: {MUTED}; font-size: 14px; margin-bottom: 16px; max-width: 720px; line-height: 1.5;
    }}
 
    /* ---------- STREAMLIT METRICS AS CARDS ---------- */
    div[data-testid="stMetric"] {{
        background: white; border: 1px solid {LINE};
        border-radius: 20px; padding: 18px 22px;
    }}
    div[data-testid="stMetricLabel"] p {{ color: {MUTED}; font-size: 13px; font-weight: 600; }}
    div[data-testid="stMetricValue"] {{ color: {INK}; font-weight: 800; font-size: 30px; letter-spacing: -.8px; }}
 
    /* ---------- SUMMARY CARD ---------- */
    .summary-card {{
        background: {YELLOW}; border-radius: 20px; padding: 22px 22px 0 22px;
        height: 100%; min-height: 300px; display: flex; flex-direction: column;
        overflow: hidden;
    }}
    .summary-head {{ display: flex; gap: 12px; align-items: center; }}
    .summary-icon {{
        width: 40px; height: 40px; border-radius: 50%; background: {INK};
        display: flex; align-items: center; justify-content: center; font-size: 16px;
    }}
    .summary-title {{ font-weight: 800; color: {INK}; font-size: 16px; }}
    .summary-sub {{ color: rgba(20,18,11,.65); font-size: 12px; }}
    .summary-value {{ color: {INK}; font-size: 44px; font-weight: 800; letter-spacing: -1.5px; margin-top: 16px; }}
    .summary-value span {{ font-size: 16px; font-weight: 700; margin-left: 6px; letter-spacing: 0; }}
    .summary-bar {{ height: 6px; background: rgba(20,18,11,.15); border-radius: 6px; margin: 6px 0 16px 0; }}
    .summary-bar div {{ height: 100%; background: {INK}; border-radius: 6px; }}
    .summary-stats {{ display: flex; gap: 8px; margin-bottom: 18px; }}
    .summary-stats div {{
        flex: 1; border-left: 2px solid rgba(20,18,11,.2); padding-left: 10px;
    }}
    .summary-stats span {{ display: block; color: rgba(20,18,11,.65); font-size: 11px; font-weight: 600; }}
    .summary-stats b {{ color: {INK}; font-size: 15px; font-weight: 800; }}
    .summary-strip {{
        background: {INK}; color: #e9e6dc; font-size: 12.5px; line-height: 1.5;
        margin: auto -22px 0 -22px; padding: 14px 22px;
    }}
 
    /* ---------- INSIGHT ---------- */
    .insight {{
        display: flex; gap: 16px; align-items: flex-start;
        background: {INK}; border-radius: 20px;
        padding: 20px 24px; margin: 22px 0 6px 0;
    }}
    .insight-icon {{
        flex: none; width: 38px; height: 38px; border-radius: 12px;
        background: {YELLOW}; display: flex; align-items: center; justify-content: center;
    }}
    .insight-title {{ font-weight: 800; color: white; font-size: 15px; }}
    .insight-text {{ color: #b7b3a5; font-size: 13.5px; margin-top: 4px; line-height: 1.6; }}
    .insight-text b {{ color: {YELLOW}; }}
 
    /* ---------- BUTTON / TABLE ---------- */
    .stDownloadButton button {{
        background: {INK}; color: white; border: none;
        border-radius: 30px; padding: 10px 24px; font-weight: 700;
    }}
    .stDownloadButton button:hover {{ background: {YELLOW}; color: {INK}; }}
    div[data-testid="stDataFrame"] {{
        border: 1px solid {LINE}; border-radius: 16px; overflow: hidden;
    }}
 
    /* ---------- FOOTER ---------- */
    .footer {{
        text-align: center; color: #a09d90; font-size: 12px;
        margin-top: 48px; padding-top: 20px; border-top: 1px solid {LINE};
    }}
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
            <div>
                <div class="brand-name">FlexGrid</div>
                <div class="brand-subtitle">Neighbourhood energy flexibility</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
    st.markdown('<div class="sidebar-section">Menu</div>', unsafe_allow_html=True)
 
    page = st.radio(
        "Navigation",
        ["Overview", "Reliability", "Battery", "Flexible Loads", "Simulation Data"],
        label_visibility="collapsed",
    )
 
    st.markdown('<div class="sidebar-section">Simulation</div>', unsafe_allow_html=True)
 
    st.success("Simulation data loaded")
 
    st.caption(
        f"Time horizon: "
        f"{results['timestamp'].min().strftime('%d %b')} to "
        f"{results['timestamp'].max().strftime('%d %b')}"
    )
    st.caption(f"Intervals: {len(results)}")
 
 
# ============================================================
# HEADER
# ============================================================
 
header_left, header_right = st.columns([4, 1])
 
with header_left:
    st.markdown(
        """
        <div class="page-title">Neighbourhood Energy Control</div>
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
        <div style="text-align:right; padding-top:8px;">
            <span class="status-pill"><span class="status-dot"></span>Simulation run</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
 
 
# ============================================================
# KPI SECTION
# ============================================================
 
baseline_unmet = metric_value("Baseline unmet energy (kWh)")
flexgrid_unmet = metric_value("FlexGrid unmet energy (kWh)")
reduction = metric_value("Unmet energy reduction (%)")
availability = metric_value("FlexGrid supply availability (%)")
peak_demand = metric_value("Peak demand (kW)")
min_soc = metric_value("Battery minimum SOC (%)")
max_soc = metric_value("Battery maximum SOC (%)")
shifted_load = metric_value("Total shifted load (kWh)")
 
k1, k2, k3, k4 = st.columns(4)
 
with k1:
    st.markdown(
        stat_card("Baseline unmet energy", format_number(baseline_unmet), "kWh",
                  "Without coordinated flexibility", "🔌"),
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        stat_card("FlexGrid unmet energy", format_number(flexgrid_unmet), "kWh",
                  "After battery and load flexibility", "🔋"),
        unsafe_allow_html=True,
    )
with k3:
    card = stat_card("Unmet energy reduction", format_number(reduction), "%",
                     "Improvement versus baseline", "📉")
    st.markdown(card.replace('class="kpi-card"', 'class="kpi-card hero"'),
                unsafe_allow_html=True)
with k4:
    st.markdown(
        stat_card("Supply availability", format_number(availability), "%",
                  "FlexGrid simulation result", "☀️"),
        unsafe_allow_html=True,
    )
 
 
# ============================================================
# OVERVIEW
# ============================================================
 
if page == "Overview":
 
    section(
        "Neighbourhood energy balance",
        "Renewable generation compared with neighbourhood demand. "
        "FlexGrid responds when available supply falls below demand.",
    )
 
    fig = go.Figure()
    line(fig, results["timestamp"], results["solar_kw"], "Solar supply", YELLOW, fill="tozeroy")
    line(fig, results["timestamp"], results["demand_kw"], "Demand", INK)
    style_chart(fig, height=430, y_title="Power (kW)")
    show(fig)
 
    section("Supply reliability", "How much of the time local demand is fully served.")
 
    g1, g2 = st.columns([1.2, 1])
    with g1:
        st.markdown(
            summary_card(max(baseline_unmet - flexgrid_unmet, 0), availability,
                         peak_demand, shifted_load, min_soc, max_soc),
            unsafe_allow_html=True,
        )
    with g2:
        show(gauge(availability, metric_value("Baseline supply availability (%)"),
                   "FlexGrid availability (black marker = baseline)"))
 
    section("Reliability impact")
 
    c1, c2 = st.columns(2)
 
    with c1:
        fig = go.Figure()
        line(fig, results["timestamp"], results["baseline_shortfall_kw"],
             "Baseline", GREY_LINE, width=2)
        line(fig, results["timestamp"], results["flexgrid_unmet_kw"],
             "FlexGrid", YELLOW, width=2.5)
        style_chart(fig, "Shortfall before vs after FlexGrid", 360, "Unmet power (kW)")
        show(fig)
 
    with c2:
        fig = go.Figure()
        line(fig, results["timestamp"], results["battery_soc"] * 100,
             "Battery SOC", INK, fill="tozeroy")
        style_chart(fig, "Community battery state of charge", 360, "SOC (%)", [0, 100])
        show(fig)
 
    insight(
        "FlexGrid intervention",
        f"The simulation reduced unmet energy by <b>{format_number(reduction)}%</b> "
        "compared with the baseline through coordinated battery dispatch "
        "and flexible-load shifting.",
    )
 
 
# ============================================================
# RELIABILITY
# ============================================================
 
elif page == "Reliability":
 
    section(
        "Reliability analysis",
        "How FlexGrid responds to renewable intermittency and reduces electricity shortfalls.",
    )
 
    baseline_availability = metric_value("Baseline supply availability (%)")
 
    r1, r2, r3 = st.columns(3)
    r1.metric("Baseline availability", f"{baseline_availability:.1f}%")
    r2.metric("FlexGrid availability", f"{availability:.1f}%")
    r3.metric("Unmet energy reduction", f"{reduction:.1f}%")
 
    st.write("")
 
    fig = go.Figure()
    line(fig, results["timestamp"], results["baseline_shortfall_kw"],
         "Baseline shortfall", GREY_LINE, width=2)
    line(fig, results["timestamp"], results["flexgrid_unmet_kw"],
         "FlexGrid unmet", YELLOW, width=2.5)
    style_chart(fig, height=500, y_title="Shortfall (kW)")
    show(fig)
 
    insight(
        "What this shows",
        "The grey line is unmet demand without coordinated flexibility. "
        "The yellow line is the unmet demand that remains after the controller "
        "uses flexible loads and community battery storage.",
    )
 
 
# ============================================================
# BATTERY
# ============================================================
 
elif page == "Battery":
 
    section(
        "Community battery",
        "Battery state of charge and dispatch decisions throughout the simulation.",
    )
 
    b1, b2, b3 = st.columns(3)
    b1.metric("Minimum SOC", f"{min_soc:.1f}%")
    b2.metric("Maximum SOC", f"{max_soc:.1f}%")
    b3.metric("Battery discharge", f"{metric_value('Total battery discharge (kWh)'):.1f} kWh")
 
    st.write("")
 
    fig = go.Figure()
    line(fig, results["timestamp"], results["battery_soc"] * 100,
         "Battery SOC", YELLOW, fill="tozeroy")
    style_chart(fig, "Battery state of charge", 420, "SOC (%)", [0, 100])
    show(fig)
 
    st.write("")
 
    fig = go.Figure()
    line(fig, results["timestamp"], results["battery_charge_kw"], "Charging", GREEN, width=2)
    line(fig, results["timestamp"], results["battery_discharge_kw"], "Discharging", INK, width=2)
    style_chart(fig, "Battery dispatch", 420, "Power (kW)")
    show(fig)
 
 
# ============================================================
# FLEXIBLE LOADS
# ============================================================
 
elif page == "Flexible Loads":
 
    section(
        "Flexible demand",
        "Flexible electricity demand can be shifted away from renewable "
        "shortfall periods while preserving critical loads.",
    )
 
    f1, f2 = st.columns(2)
    f1.metric("Total shifted load", f"{shifted_load:.1f} kWh")
    f2.metric("Peak demand", f"{peak_demand:.1f} kW")
 
    st.write("")
 
    fig = go.Figure()
    line(fig, results["timestamp"], results["load_shift_kw"],
         "Flexible load shifted", YELLOW, fill="tozeroy")
    style_chart(fig, "Flexible load shifting", 450, "Shifted power (kW)")
    show(fig)
 
    insight(
        "Demand-side flexibility",
        "FlexGrid temporarily shifts eligible electricity consumption during "
        "shortage periods. Examples include EV charging, water pumping and other "
        "deferrable loads. Critical loads are not intentionally shifted.",
    )
 
 
# ============================================================
# SIMULATION DATA
# ============================================================
 
elif page == "Simulation Data":
 
    section("Simulation data", "Raw simulation output used to generate the dashboard metrics.")
 
    st.dataframe(results, use_container_width=True, height=550)
 
    st.download_button(
        label="Download simulation CSV",
        data=results.to_csv(index=False).encode("utf-8"),
        file_name="flexgrid_simulation_results.csv",
        mime="text/csv",
    )
 
 
# ============================================================
# FOOTER
# ============================================================
 
st.markdown(
    '<div class="footer">FlexGrid · Neighbourhood Energy Flexibility · '
    'Simulation Prototype · Yuva Yodha 2026</div>',
    unsafe_allow_html=True,
)
 