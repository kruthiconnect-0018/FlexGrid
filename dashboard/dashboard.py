from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="FlexGrid | Energy Operations", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
:root{--bg:#f5f2ec;--surface:#fcfbf8;--line:#dfe3e5;--text:#18232d;--muted:#697681;--navy:#17232e;--green:#3f8f7a;--amber:#c58b3a;--red:#b85c5c;--blue:#557fa5}
html,body,[class*=css]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
.stApp{background:var(--bg)} .block-container{max-width:1540px;padding:1.35rem 2rem 3rem}
#MainMenu,footer,header{visibility:hidden}
[data-testid=stSidebar]{background:var(--navy);border-right:1px solid #202d39}
[data-testid=stSidebar] *{color:#e7edf3}
.brand{display:flex;align-items:center;gap:10px;padding:4px}.brand-mark{width:35px;height:35px;border-radius:9px;display:flex;align-items:center;justify-content:center;background:#f0ad2c;color:#111923;font-size:18px;font-weight:800}.brand-name{font-size:18px;font-weight:750;color:#fff}.brand-sub{color:#83909e;font-size:10px;line-height:1.45;margin:6px 5px 26px 49px}.side-label{color:#6f7e8d;font-size:9px;font-weight:750;letter-spacing:.14em;text-transform:uppercase;margin:20px 4px 7px}
div[data-testid=stSidebar] div.stButton>button{width:100%;min-height:35px;margin:2px 0;padding:0 11px;border:1px solid transparent;border-radius:7px;background:transparent!important;color:#aeb9c5!important;font-size:11px;font-weight:600;text-align:left;box-shadow:none}div[data-testid=stSidebar] div.stButton>button:hover{background:#20313e!important;color:#fff!important;border-color:#304553!important}div[data-testid=stSidebar] div.stButton>button[kind=primary]{background:#20313e!important;border-color:#304553!important;color:#fff!important}
.top-header{display:flex;justify-content:space-between;align-items:flex-start;gap:25px;margin:3px 0 20px}.eyebrow{color:#778493;font-size:9px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;margin-bottom:5px}.title{color:var(--text);font-size:30px;font-weight:760;letter-spacing:-.035em;line-height:1.08}.subtitle{color:var(--muted);font-size:12px;margin-top:7px}.status-pill{display:flex;align-items:center;gap:8px;white-space:nowrap;padding:8px 11px;border:1px solid #dfe5ea;background:var(--surface);border-radius:999px;color:#3e4a57;font-size:10px;font-weight:750}.status-dot{width:7px;height:7px;border-radius:50%;background:var(--green)}.status-dot.paused{background:var(--amber)}
.kpi{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:14px 15px;min-height:104px}.kpi-label{color:#778493;font-size:9px;font-weight:800;letter-spacing:.07em;text-transform:uppercase}.kpi-value{color:var(--text);font-size:25px;font-weight:760;letter-spacing:-.025em;margin-top:8px;line-height:1}.kpi-unit{color:#657180;font-size:11px;font-weight:650}.kpi-note{color:#929daa;font-size:9px;margin-top:9px}.good{color:var(--green);font-weight:700}.warn{color:var(--amber);font-weight:700}
.panel{background:var(--surface);border:1px solid var(--line);border-radius:9px;padding:16px}.panel-head{display:flex;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:8px}.panel-title{color:var(--text);font-size:14px;font-weight:750}.panel-note{color:#8a95a3;font-size:9px}.section-title{color:var(--text);font-size:17px;font-weight:750;letter-spacing:-.02em;margin:3px 0}.section-note{color:var(--muted);font-size:11px;margin-bottom:13px}.metric-big{color:var(--text);font-size:30px;font-weight:750}.metric-label{color:#7a8693;font-size:9px;text-transform:uppercase;letter-spacing:.06em;font-weight:700}
.flow-wrap{border:1px solid var(--line);background:#fbfcfd;border-radius:8px;padding:18px 12px}.flow-title{color:#7a8693;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:16px}.flow-row{display:grid;grid-template-columns:1fr 32px 1.15fr 32px 1fr;align-items:center;gap:5px}.flow-node{min-height:82px;border:1px solid #dfe5ea;border-radius:8px;background:#fff;padding:12px}.flow-node.core{background:var(--navy);border-color:var(--navy);color:#fff}.flow-name{font-size:10px;font-weight:750;color:#53606e;text-transform:uppercase;letter-spacing:.06em}.core .flow-name{color:#c7d1da}.flow-value{color:var(--text);font-size:19px;font-weight:760;margin-top:7px}.core .flow-value{color:#fff}.flow-unit{color:#7a8693;font-size:9px;font-weight:600}.core .flow-unit{color:#aeb9c5}.flow-arrow{text-align:center;color:#98a3ae;font-size:17px}.flow-foot{display:flex;justify-content:space-between;border-top:1px solid #e9edf0;margin-top:14px;padding-top:11px;color:#788492;font-size:9px}
.insight{background:var(--navy);border-radius:9px;padding:16px;color:#fff}.insight-label{color:#8997a5;font-size:9px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}.insight-title{font-size:16px;font-weight:750;margin-top:6px}.insight-text{color:#b8c3cd;font-size:10px;line-height:1.55;margin-top:5px}.control-row{display:flex;align-items:center;justify-content:space-between;gap:10px;border-top:1px solid #edf0f2;padding:12px 0}.control-name{color:var(--text);font-size:11px;font-weight:700}.control-note{color:#8a95a3;font-size:9px;margin-top:2px}.control-value{color:#465260;font-size:11px;font-weight:700;white-space:nowrap}.alert-card{border:1px solid #e1e6ea;border-radius:8px;padding:12px 13px;background:var(--surface);margin-bottom:8px}.alert-card.warn{border-left:3px solid var(--amber)}.alert-card.good{border-left:3px solid var(--green)}.alert-card.danger{border-left:3px solid var(--red)}.alert-label{color:#7a8693;font-size:9px;font-weight:800;letter-spacing:.07em;text-transform:uppercase}.alert-title{color:var(--text);font-size:11px;font-weight:700;margin-top:4px}.alert-text{color:var(--muted);font-size:9px;line-height:1.45;margin-top:3px}
div.stButton>button{border-radius:7px;border:1px solid #dce2e7;background:var(--surface);color:#364250;font-size:11px;font-weight:650;min-height:36px;box-shadow:none}div.stButton>button:hover{border-color:#aeb9c4;color:#17202b}div.stButton>button[kind=primary]{background:#172330;border-color:#172330;color:#fff}div[data-testid=stSelectbox] label,div[data-testid=stRadio] label,div[data-testid=stSlider] label{color:#7b8793!important;font-size:9px!important;font-weight:700!important;text-transform:uppercase;letter-spacing:.06em}div[data-baseweb=select]>div{border-radius:7px!important;border-color:#dce2e7!important;background:var(--surface)!important}.spacer{height:12px}
</style>
""", unsafe_allow_html=True)

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/"outputs"
RESULTS_FILE=OUT/"simulation_results.csv"
METRICS_FILE=OUT/"metrics.csv"

# Streamlit Cloud does not keep locally generated output files from your
# development machine. If they are missing, generate the simulation once
# inside the deployed app before trying to load the dashboard data.
def ensure_simulation_outputs():
    if RESULTS_FILE.exists() and METRICS_FILE.exists():
        return True

    import subprocess
    import sys

    OUT.mkdir(parents=True, exist_ok=True)

    with st.spinner("Preparing FlexGrid simulation data..."):
        try:
            completed = subprocess.run(
                [sys.executable, str(ROOT / "run_simulation.py")],
                cwd=str(ROOT),
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except subprocess.TimeoutExpired:
            st.error("The FlexGrid simulation took too long to finish on the deployed server.")
            return False
        except Exception as exc:
            st.error(f"Unable to start the FlexGrid simulation: {exc}")
            return False

    if completed.returncode != 0:
        details = (completed.stderr or completed.stdout or "No additional error details.").strip()
        st.error("FlexGrid could not generate the simulation data.")
        with st.expander("Simulation error details"):
            st.code(details)
        return False

    return RESULTS_FILE.exists() and METRICS_FILE.exists()


if not ensure_simulation_outputs():
    st.stop()

results=pd.read_csv(RESULTS_FILE)
metrics_df=pd.read_csv(METRICS_FILE)
metrics=dict(zip(metrics_df["Metric"],metrics_df["Value"]))
if "timestamp" in results.columns: results["timestamp"]=pd.to_datetime(results["timestamp"])

def metric(name,default=0.0):
    try:return float(metrics.get(name,default))
    except (TypeError,ValueError):return default

def fmt(v,d=1):return f"{float(v):,.{d}f}"

def chart_base(fig,height=360):
    fig.update_layout(height=height,margin=dict(l=8,r=8,t=22,b=8),paper_bgcolor="#fcfbf8",plot_bgcolor="#fcfbf8",font=dict(family="Inter,system-ui,sans-serif",color="#53606e"),hovermode="x unified",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0,font=dict(size=9)),xaxis=dict(showgrid=False,linecolor="#dfe3e5",tickfont=dict(size=9)),yaxis=dict(gridcolor="#e8ebed",zeroline=False,tickfont=dict(size=9)))
    return fig

def panel_head(title,note=None):
    st.markdown(f'<div class="panel-head"><div class="panel-title">{title}</div><div class="panel-note">{note or ""}</div></div>',unsafe_allow_html=True)

def apply_scenario(df,scenario,strategy):
    d=df.copy()
    if scenario=="High Demand": d["demand_kw"]*=1.18
    elif scenario=="Low Solar": d["solar_kw"]*=.65
    elif scenario=="Grid Shortage":
        if "baseline_shortfall_kw" in d:d["baseline_shortfall_kw"]*=1.25
        if "flexgrid_unmet_kw" in d:d["flexgrid_unmet_kw"]*=1.20
    if {"demand_kw","solar_kw","flexgrid_unmet_kw"}.issubset(d.columns):
        residual=(d["demand_kw"]-d["solar_kw"]).clip(lower=0)
        if strategy=="Battery First" and "battery_discharge_kw" in d:d["flexgrid_unmet_kw"]=(residual-d["battery_discharge_kw"]).clip(lower=0)
        elif strategy=="Load Shifting" and "load_shift_kw" in d:d["flexgrid_unmet_kw"]=(residual-d["load_shift_kw"]).clip(lower=0)
        elif strategy=="Grid First":d["flexgrid_unmet_kw"]=residual*.85
    return d

def current_values(d):
    r=d.iloc[-1]; demand=float(r.get("demand_kw",0)); solar=float(r.get("solar_kw",0)); soc=float(r.get("battery_soc",0))*100; discharge=float(r.get("battery_discharge_kw",0)); grid=max(demand-solar-discharge,0); return demand,solar,soc,grid

def add_line(fig,d,col,name,color,width=2.2,dash=None):
    if col not in d.columns:return
    line=dict(color=color,width=width)
    if dash:line["dash"]=dash
    fig.add_trace(go.Scatter(x=d["timestamp"],y=d[col],name=name,mode="lines",line=line))

for k,v in {"page":"Overview","running":True,"scenario":"Normal","strategy":"Automatic","window":24,"battery_command":"Automatic","load_applied":False}.items():
    if k not in st.session_state:st.session_state[k]=v

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">⚡</div><div class="brand-name">FlexGrid</div></div><div class="brand-sub">Neighbourhood Energy<br>Operations Platform</div>',unsafe_allow_html=True)
    st.markdown('<div class="side-label">Workspace</div>',unsafe_allow_html=True)
    for p in ["Overview","Live Control","Forecast","Battery","Flexible Loads","Alerts","Data"]:
        if st.button(p,key=f"nav_{p}",use_container_width=True,type="primary" if st.session_state.page==p else "secondary"):
            st.session_state.page=p;st.rerun()
    st.markdown('<div class="side-label">Simulation</div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("Pause" if st.session_state.running else "Run",use_container_width=True):st.session_state.running=not st.session_state.running;st.rerun()
    with c2:
        if st.button("Reset",use_container_width=True):
            st.session_state.running=True;st.session_state.scenario="Normal";st.session_state.strategy="Automatic";st.session_state.window=24;st.session_state.battery_command="Automatic";st.session_state.load_applied=False;st.rerun()
    st.markdown('<div class="side-label">Operating mode</div>',unsafe_allow_html=True)
    st.session_state.scenario=st.selectbox("Scenario",["Normal","High Demand","Low Solar","Grid Shortage"],index=["Normal","High Demand","Low Solar","Grid Shortage"].index(st.session_state.scenario),label_visibility="collapsed")
    st.session_state.strategy=st.selectbox("Strategy",["Automatic","Load Shifting","Battery First","Grid First"],index=["Automatic","Load Shifting","Battery First","Grid First"].index(st.session_state.strategy),label_visibility="collapsed")
    st.markdown('<div class="side-label">Time window</div>',unsafe_allow_html=True)
    st.session_state.window=st.select_slider("Window",options=[1,6,12,24,48,72],value=st.session_state.window,format_func=lambda x:f"{x} h",label_visibility="collapsed")
    st.markdown(f'<div style="border-top:1px solid #25323f;margin-top:20px;padding:15px 4px 0"><div class="side-label" style="margin:0">Dataset</div><div style="font-size:13px;font-weight:650">{len(results):,} intervals</div><div style="color:#74818e;font-size:9px">15-minute resolution</div><div class="side-label" style="margin:14px 0 0">Strategy</div><div style="font-size:13px;font-weight:650">{st.session_state.strategy}</div></div>',unsafe_allow_html=True)

view=apply_scenario(results.iloc[:st.session_state.window*4].copy(),st.session_state.scenario,st.session_state.strategy)
if view.empty:st.error("No simulation data is available.");st.stop()
demand_now,solar_now,battery_now,grid_now=current_values(view)
renewable_share=(solar_now/demand_now*100) if demand_now else 0
flexgrid_unmet=float(view.iloc[-1].get("flexgrid_unmet_kw",0))
baseline_unmet=float(view.iloc[-1].get("baseline_shortfall_kw",0))

st.markdown(f'<div class="top-header"><div><div class="eyebrow">Energy operations / simulation</div><div class="title">Neighbourhood Energy Control</div><div class="subtitle">Coordinate renewable supply, flexible demand, storage and grid dependency.</div></div><div class="status-pill"><span class="status-dot {"" if st.session_state.running else "paused"}"></span>{"SYSTEM ONLINE" if st.session_state.running else "SIMULATION PAUSED"}</div></div>',unsafe_allow_html=True)

if st.session_state.page=="Overview":
    k1,k2,k3,k4=st.columns(4)
    cards=[("Current demand",fmt(demand_now),"kW","Neighbourhood electrical load"),("Renewable supply",fmt(solar_now),"kW",f'<span class="good">{renewable_share:.0f}%</span> of current demand'),("Community battery",fmt(battery_now,0),"%",f'<span class="{"good" if battery_now>=40 else "warn"}">{"Healthy reserve" if battery_now>=40 else "Reserve getting low"}</span>'),("Grid dependency",fmt(grid_now),"kW",f'<span class="{"good" if grid_now<demand_now*.4 else "warn"}">{"Low dependency" if grid_now<demand_now*.4 else "Grid support active"}</span>')]
    for col,(lab,val,unit,note) in zip((k1,k2,k3,k4),cards):
        with col:st.markdown(f'<div class="kpi"><div class="kpi-label">{lab}</div><div class="kpi-value">{val} <span class="kpi-unit">{unit}</span></div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="spacer"></div>',unsafe_allow_html=True)
    left,right=st.columns([1.65,1])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Live energy flow",f"{st.session_state.window}-hour operating window")
        st.markdown(f'<div class="flow-wrap"><div class="flow-title">Current power balance</div><div class="flow-row"><div class="flow-node"><div class="flow-name">Solar</div><div class="flow-value">{fmt(solar_now)} <span class="flow-unit">kW</span></div></div><div class="flow-arrow">→</div><div class="flow-node core"><div class="flow-name">FlexGrid controller</div><div class="flow-value">ACTIVE</div><div class="flow-unit">{st.session_state.strategy} strategy</div></div><div class="flow-arrow">→</div><div class="flow-node"><div class="flow-name">Neighbourhood</div><div class="flow-value">{fmt(demand_now)} <span class="flow-unit">kW</span></div></div></div><div class="flow-foot"><span>Battery {fmt(battery_now,0)}% SOC</span><span>Grid {fmt(grid_now)} kW</span><span>Residual {fmt(flexgrid_unmet)} kW</span></div></div>',unsafe_allow_html=True)
        fig=go.Figure();add_line(fig,view,"solar_kw","Solar","#c58b3a",2.4);add_line(fig,view,"demand_kw","Demand","#334452",2.2);add_line(fig,view,"battery_discharge_kw","Battery discharge","#3f8f7a",1.7,"dot");add_line(fig,view,"flexgrid_unmet_kw","Residual shortfall","#b85c5c",1.6,"dash");chart_base(fig,330);fig.update_yaxes(title="Power (kW)");st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False});st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="insight"><div class="insight-label">Controller recommendation</div><div class="insight-title">Prioritise flexible demand before deeper battery discharge.</div><div class="insight-text">When renewable output is insufficient, FlexGrid can shift controllable demand first and preserve community storage for periods with a larger supply deficit.</div></div>',unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>',unsafe_allow_html=True);st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Operating state")
        states=[("Renewable supply","Available" if solar_now>0 else "Unavailable"),("Community battery","Healthy" if battery_now>=40 else "Reserve low"),("Flexible demand","Controllable"),("Grid connection","Supporting load" if grid_now>0 else "Not required")]
        for name,state in states:st.markdown(f'<div class="control-row"><div><div class="control-name">{name}</div><div class="control-note">Current operating condition</div></div><div class="control-value">{state}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="spacer"></div>',unsafe_allow_html=True);a,b,c=st.columns(3)
    vals=[("FlexGrid unmet energy",metric("FlexGrid unmet energy (kWh)"),"kWh","Total residual unmet energy."),("Shortfall reduction",metric("Unmet energy reduction (%)"),"%","Improvement against baseline."),("Flexible demand used",metric("Total shifted load (kWh)"),"kWh","Energy shifted by controllable loads.")]
    for col,(lab,val,unit,note) in zip((a,b,c),vals):
        with col:st.markdown(f'<div class="panel"><div class="panel-title">{lab}</div><div class="metric-big" style="margin-top:7px">{fmt(val)} <span class="kpi-unit">{unit}</span></div><div class="panel-note" style="margin-top:6px">{note}</div></div>',unsafe_allow_html=True)

elif st.session_state.page=="Live Control":
    st.markdown('<div class="section-title">Live control</div><div class="section-note">Operator controls for flexible demand and community storage.</div>',unsafe_allow_html=True)
    left,right=st.columns([1.15,1])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Flexible demand","Resources available to the controller")
        loads=[("EV charging",6,"Shiftable"),("Water heating",8,"Shiftable"),("HVAC",4,"Adjustable"),("Laundry",3,"Shiftable")];selected=0
        for name,power,mode in loads:
            if st.checkbox(f"{name}  ·  {power} kW  ·  {mode}",value=True,key=f"load_{name}"):selected+=1
        if st.button("Apply load strategy",type="primary",use_container_width=True):st.session_state.load_applied=True
        if st.session_state.load_applied:st.success(f"{selected} resources assigned to {st.session_state.strategy.lower()} control.")
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Battery dispatch","Community storage command")
        st.markdown(f'<div class="metric-label">State of charge</div><div class="metric-big">{battery_now:.0f}%</div>',unsafe_allow_html=True);st.progress(max(0,min(1,battery_now/100)))
        st.session_state.battery_command=st.radio("Dispatch",["Automatic","Charge","Discharge","Hold"],index=["Automatic","Charge","Discharge","Hold"].index(st.session_state.battery_command),horizontal=True)
        if st.button("Apply battery command",use_container_width=True):st.success(f"Battery command set to {st.session_state.battery_command.lower()}.")
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="spacer"></div>',unsafe_allow_html=True);st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Current measurements");m1,m2,m3,m4=st.columns(4);m1.metric("Demand",f"{demand_now:.1f} kW");m2.metric("Renewable",f"{solar_now:.1f} kW");m3.metric("Battery",f"{battery_now:.0f}%");m4.metric("Grid import",f"{grid_now:.1f} kW");st.markdown('</div>',unsafe_allow_html=True)

elif st.session_state.page=="Forecast":
    st.markdown('<div class="section-title">Forecast & supply risk</div><div class="section-note">Compare renewable supply, demand and residual shortfall.</div>',unsafe_allow_html=True);st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Supply vs demand",f"{st.session_state.window}-hour view");fig=go.Figure();add_line(fig,view,"solar_kw","Solar","#c58b3a",2.4);add_line(fig,view,"demand_kw","Demand","#334452",2.2);add_line(fig,view,"baseline_shortfall_kw","Baseline shortfall","#9aa5ad",1.5,"dot");add_line(fig,view,"flexgrid_unmet_kw","FlexGrid shortfall","#b85c5c",1.8,"dash");chart_base(fig,410);fig.update_yaxes(title="Power (kW)");st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False});st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="spacer"></div>',unsafe_allow_html=True);l,r=st.columns(2)
    with l:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Forecast indicators");gap=max(demand_now-solar_now,0)
        for n,v in [("Current supply gap",f"{gap:.1f} kW"),("Baseline shortfall",f"{baseline_unmet:.1f} kW"),("FlexGrid residual",f"{flexgrid_unmet:.1f} kW")]:st.markdown(f'<div class="control-row"><div class="control-name">{n}</div><div class="control-value">{v}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with r:st.markdown('<div class="insight"><div class="insight-label">Planning signal</div><div class="insight-title">Preserve storage for deeper renewable deficits.</div><div class="insight-text">Flexible demand is the first controllable resource in the selected strategy. Battery dispatch should respond when the remaining gap becomes material.</div></div>',unsafe_allow_html=True)

elif st.session_state.page=="Battery":
    st.markdown('<div class="section-title">Community battery</div><div class="section-note">Monitor state of charge and battery dispatch.</div>',unsafe_allow_html=True);l,r=st.columns([.85,1.7])
    with l:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Storage status");st.markdown(f'<div class="metric-label">Current SOC</div><div class="metric-big">{battery_now:.0f}%</div>',unsafe_allow_html=True);st.progress(max(0,min(1,battery_now/100)))
        for n,v in [("Minimum SOC",f"{metric('Battery minimum SOC (%)'):.0f}%"),("Maximum SOC",f"{metric('Battery maximum SOC (%)'):.0f}%"),("Total charge",f"{metric('Total battery charge (kWh)'):.1f} kWh"),("Total discharge",f"{metric('Total battery discharge (kWh)'):.1f} kWh")]:st.markdown(f'<div class="control-row"><div class="control-name">{n}</div><div class="control-value">{v}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with r:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Battery activity");d=view.assign(battery_soc_pct=view["battery_soc"]*100);fig=go.Figure();add_line(fig,d,"battery_soc_pct","SOC","#557fa5",2.3);chart_base(fig,300);fig.update_yaxes(title="SOC (%)",range=[0,100]);fig.add_hline(y=20,line_dash="dot",line_color="#b85c5c");st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        if {"battery_charge_kw","battery_discharge_kw"}.issubset(view.columns):
            fig2=go.Figure();add_line(fig2,view,"battery_charge_kw","Charge","#557fa5",1.8);add_line(fig2,view,"battery_discharge_kw","Discharge","#b85c5c",1.8);chart_base(fig2,250);fig2.update_yaxes(title="Power (kW)");st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        st.markdown('</div>',unsafe_allow_html=True)

elif st.session_state.page=="Flexible Loads":
    st.markdown('<div class="section-title">Flexible demand</div><div class="section-note">Resources that can be shifted or adjusted to reduce supply shortfalls.</div>',unsafe_allow_html=True)
    if "load_shift_kw" in view.columns:
        st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Load shifting profile");fig=go.Figure();add_line(fig,view,"load_shift_kw","Shifted load","#6f7891",2.2);chart_base(fig,320);fig.update_yaxes(title="Shifted load (kW)");st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False});st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="spacer"></div>',unsafe_allow_html=True);a,b,c=st.columns(3);a.metric("Total shifted",f"{metric('Total shifted load (kWh)'):.1f} kWh");b.metric("Peak demand",f"{metric('Peak demand (kW)'):.1f} kW");c.metric("Residual peak",f"{metric('Peak residual demand after FlexGrid (kW)'):.1f} kW");st.markdown('<div class="spacer"></div><div class="panel">',unsafe_allow_html=True);panel_head("Flexible resource register");st.dataframe(pd.DataFrame({"Resource":["EV charging","Water heating","HVAC","Laundry"],"Power":["6 kW","8 kW","4 kW","3 kW"],"Control":["Shift","Shift","Adjust","Shift"],"Availability":["Available"]*4}),use_container_width=True,hide_index=True);st.markdown('</div>',unsafe_allow_html=True)

elif st.session_state.page=="Alerts":
    st.markdown('<div class="section-title">System alerts</div><div class="section-note">Operational conditions derived from the selected simulation state.</div>',unsafe_allow_html=True)
    alerts=[]
    alerts.append(("Attention","Renewable supply is below current demand." if demand_now>solar_now else "Renewable supply is covering current demand.","FlexGrid can use flexible demand and battery support to reduce the remaining gap." if demand_now>solar_now else "No immediate supply-side intervention is required.","warn" if demand_now>solar_now else "good"))
    alerts.append(("Warning","Battery reserve is approaching its lower limit." if battery_now<25 else "Battery reserve is within operating range.","Preserve storage capacity for the next significant shortfall." if battery_now<25 else "No immediate battery constraint is detected.","danger" if battery_now<25 else "good"))
    alerts.append(("Grid support","External supply is currently supporting the neighbourhood." if grid_now>0 else "Grid support is not currently required.",f"Estimated grid contribution is {grid_now:.1f} kW." if grid_now>0 else "Local resources are covering the visible load.","warn" if grid_now>0 else "good"))
    for lab,title,text,level in alerts:st.markdown(f'<div class="alert-card {level}"><div class="alert-label">{lab}</div><div class="alert-title">{title}</div><div class="alert-text">{text}</div></div>',unsafe_allow_html=True)

elif st.session_state.page=="Data":
    st.markdown('<div class="section-title">Simulation data</div><div class="section-note">Raw model output and evaluation metrics.</div>',unsafe_allow_html=True);st.markdown('<div class="panel">',unsafe_allow_html=True);panel_head("Time-series output",f"{len(view):,} visible intervals");st.dataframe(view,use_container_width=True,height=520,hide_index=True);st.download_button("Download visible CSV",data=view.to_csv(index=False).encode("utf-8"),file_name="flexgrid_visible_data.csv",mime="text/csv");st.markdown('</div>',unsafe_allow_html=True);st.markdown('<div class="spacer"></div><div class="panel">',unsafe_allow_html=True);panel_head("Simulation metrics");st.dataframe(metrics_df,use_container_width=True,hide_index=True);st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div style="margin-top:28px;padding-top:12px;border-top:1px solid #e1e6ea;color:#8a95a3;font-size:9px">FlexGrid · Simulation prototype · Values shown are model outputs, not measured grid performance.</div>',unsafe_allow_html=True)
