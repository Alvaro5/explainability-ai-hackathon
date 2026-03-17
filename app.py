import warnings; warnings.filterwarnings("ignore")
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from model import load_all, C, styled_chart, risk_emoji

st.set_page_config(
    page_title="TalentGuard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"""
<style>
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: visible !important;}}
html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }}

/* Global Sidebar Overrides */
[data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(180deg, {C['bg']} 0%, {C['card_bg']} 100%);
    border-right: 1px solid {C['card_border']};
}}

/* Radio Navigation Styling */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label {{
    background-color: transparent;
    padding: 10px 16px;
    border-radius: 8px;
    margin-bottom: 4px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-left: 3px solid transparent;
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label:hover {{
    background-color: {C['hover_bg']};
    transform: translateX(4px);
    border-left: 3px solid {C['primary_hover_indicator'] if 'primary_hover_indicator' in C else 'rgba(59, 130, 246, 0.5)'};
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] {{
    background-color: {C['tab_act_bg']};
    border-left: 3px solid {C['primary']};
    box-shadow: inset 0 0 20px rgba(59, 130, 246, 0.05);
}}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] p {{
    font-weight: 600;
    color: {C['primary']};
}}

/* Base App Cards */
.card {{
    background: {C['card_bg']};
    border: 1px solid {C['card_border']};
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    transition: box-shadow 0.3s ease;
}}
.card:hover {{ box-shadow: 0 8px 24px rgba(0,0,0,0.1); }}
.card h3 {{ color: {C['text']}; margin: 0 0 8px 0; }}
.card p  {{ color: {C['text_muted']}; margin: 0; }}
.kpi {{
    background: {C['kpi_rgba']};
    border: 1px solid {C['card_border']};
    border-radius: 12px;
    padding: 22px 18px;
    text-align: center;
    border-top: 3px solid {C['primary']};
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.kpi:hover {{ transform: translateY(-4px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
.kpi-danger  {{ border-top-color: {C['danger']}; }}
.kpi-warning {{ border-top-color: {C['warning']}; }}
.kpi-success {{ border-top-color: {C['success']}; }}
.kpi h2  {{ margin:0; font-size:2.4rem; font-weight:700; color:{C['text']}; line-height:1.1; }}
.kpi p   {{ margin:4px 0 0 0; font-size:.85rem; color:{C['text_muted']}; }}
.kpi small {{ font-size:.78rem; color:{C['text_muted']}; }}
.section-title {{
    font-size:1.1rem; font-weight:700; color:{C['text']};
    border-left:4px solid {C['primary']}; padding-left:10px;
    margin: 22px 0 12px 0;
}}
.profile-header {{
    background: linear-gradient(90deg, {C['header_g1']} 0%, {C['header_g2']} 100%);
    border: 1px solid {C['card_border']};
    border-radius: 12px;
    color: {C['text']};
    padding: 22px 26px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}}
.badge {{
    display:inline-block; padding:5px 14px; border-radius:20px;
    font-weight:700; font-size:.9rem;
}}
.badge-high   {{ background:{C['badge_hi_bg2']}; color:{C['badge_hi_txt']}; border:1px solid {C['badge_hi_bd']}; box-shadow: 0 0 10px {C['badge_hi_bd']}40;}}
.badge-medium {{ background:{C['badge_me_bg2']}; color:{C['badge_me_txt']}; border:1px solid {C['badge_me_bd']}; box-shadow: 0 0 10px {C['badge_me_bd']}40;}}
.badge-low    {{ background:{C['badge_lo_bg2']}; color:{C['badge_lo_txt']}; border:1px solid {C['badge_lo_bd']}; box-shadow: 0 0 10px {C['badge_lo_bd']}40;}}
.action-row {{
    display:flex; align-items:flex-start; gap:12px;
    padding:10px 0; border-bottom:1px solid {C['card_border']};
    transition: background-color 0.2s ease;
}}
.action-row:hover {{ background-color: {C['hover_bg']}; border-radius: 6px; padding: 10px 8px; border-bottom-color: transparent;}}
.action-icon {{ font-size:1.0rem; font-weight:700; min-width:48px; color:{C['text_muted']}; }}
.priority-haute   {{ background:{C['prio_hi_bg']}; color:{C['prio_hi_txt']}; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; border:1px solid {C['prio_hi_bd']}; }}
.priority-moyenne {{ background:{C['prio_me_bg']}; color:{C['prio_me_txt']}; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; border:1px solid {C['prio_me_bd']}; }}
.priority-info    {{ background:{C['prio_in_bg']}; color:{C['prio_in_txt']}; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; border:1px solid {C['prio_in_bd']}; }}
.callout-green {{
    background:{C['call_gn_bg']}; border-left:4px solid {C['success']};
    padding:14px 18px; border-radius:0 10px 10px 0;
    color:{C['call_gn_txt']}; font-weight:500; margin:12px 0;
}}
.callout-blue {{
    background:{C['call_bl_bg']}; border-left:4px solid {C['primary']};
    padding:14px 18px; border-radius:0 10px 10px 0;
    color:{C['call_bl_txt']}; font-weight:500; margin:12px 0;
}}
.theme-badge {{
    display:inline-block; background:{C['thm_bg']}; color:{C['thm_txt']};
    border:1px solid {C['thm_bd']}; border-radius:20px;
    padding:3px 12px; font-size:.8rem; font-weight:600;
    margin: 2px;
}}

/* Sidebar Custom Cards */
.sidebar-title-container {{
    text-align: center;
    padding: 24px 0 32px 0;
    position: relative;
    overflow: hidden;
}}
.sidebar-title-container::before {{
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, {C['primary']}22 0%, transparent 60%);
    z-index: 0;
    pointer-events: none;
}}
.sidebar-title {{
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, {C['primary']} 0%, {C['mint']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    z-index: 1;
    margin-bottom: 6px;
}}
.sidebar-subtitle {{
    font-size: 0.8rem;
    color: {C['text_muted']};
    font-weight: 500;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    position: relative;
    z-index: 1;
}}

.sidebar-stats-card {{
    background: {C['card_rgba']};
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid {C['card_border']};
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.sidebar-stats-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}}
.stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid {C['card_border']}40;
}}
.stat-row:last-child {{
    border-bottom: none;
}}
.stat-label {{
    font-size: 0.85rem;
    color: {C['text_muted']};
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
}}
.stat-value {{
    font-size: 1.1rem;
    font-weight: 700;
}}
.stat-danger {{ color: {C['danger']}; text-shadow: 0 0 10px {C['danger']}40; }}
.stat-warning {{ color: {C['warning']}; text-shadow: 0 0 10px {C['warning']}40; }}

.tech-stack-indicator {{
    background: {C['card_rgba']};
    backdrop-filter: blur(8px);
    border: 1px solid {C['card_border']};
    border-radius: 8px;
    padding: 10px 12px;
    margin-top: 24px;
    font-size: 0.75rem;
    display: flex;
    flex-direction: column;
    gap: 6px;
}}
.tech-item {{
    display: flex;
    align-items: center;
    gap: 6px;
}}
.tech-dot {{
    width: 6px; height: 6px; border-radius: 50%;
}}
.dot-frugal {{ background-color: {C['success']}; box-shadow: 0 0 8px {C['success']}80; }}
.dot-explain {{ background-color: {C['primary']}; box-shadow: 0 0 8px {C['primary']}80; }}
</style>
""", unsafe_allow_html=True)

data = load_all()
emp  = data["emp"]

n_high = (emp["RiskScore"]>=0.70).sum()
n_med  = ((emp["RiskScore"]>=0.40)&(emp["RiskScore"]<0.70)).sum()

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-title-container">
      <div class="sidebar-title">TalentGuard</div>
      <div class="sidebar-subtitle">Retention Platform</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio(
        "Menu",
        ["Dashboard", "Employee Profile", "HR Analysis",
         "AI Approach", "Compliance & Ethics"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="sidebar-stats-card">
      <div class="stat-row">
        <span class="stat-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          High Risk
        </span>
        <span class="stat-value stat-danger">{n_high}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
          To Monitor
        </span>
        <span class="stat-value stat-warning">{n_med}</span>
      </div>
    </div>
    
    <div class="tech-stack-indicator">
      <div class="tech-item">
        <div class="tech-dot dot-frugal"></div>
        <span><b style="color:{C['text']}">Frugal AI</b>: Logistic Reg.</span>
      </div>
      <div class="tech-item">
        <div class="tech-dot dot-explain"></div>
        <span><b style="color:{C['text']}">Explainable AI</b>: SHAP</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

if page == "Dashboard":
    st.markdown(f"""
    <h1 style='color:{C['text']};margin-bottom:4px;'>TalentGuard</h1>
    <p style='color:{C['text_muted']};margin:0 0 24px 0;'>
    Talent Retention System — HR Risk Overview
    </p>""", unsafe_allow_html=True)

    n_actifs = (emp["Termd"]==0).sum()
    turnover = emp["Termd"].mean()
    n_low    = (emp["RiskScore"]<0.40).sum()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""<div class="kpi">
            <h2>{n_actifs}</h2><p>Active Employees</p>
            <small>out of {len(emp)} in the database</small></div>""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""<div class="kpi kpi-danger">
            <h2>{turnover:.1%}</h2><p>Turnover Rate</p>
            <small>{"Above" if turnover > 0.15 else "Below"} sector average (~15%)</small></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi kpi-danger">
            <h2>{n_high}</h2><p>High Risk</p>
            <small>Predicted score &gt; 70%</small></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi kpi-warning">
            <h2>{n_med}</h2><p>To Monitor</p>
            <small>Predicted score 40-70%</small></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">At-Risk Employees — Action Required</p>', unsafe_allow_html=True)

    col_dept_filter, col_risk_filter = st.columns(2)
    with col_dept_filter:
        all_depts = ["All Departments"] + sorted(emp["Department"].unique().tolist())
        sel_dept = st.selectbox("Filter by department", all_depts, key="dash_dept")
    with col_risk_filter:
        sel_risk = st.selectbox("Filter by risk level", ["All Levels", "HIGH", "MEDIUM", "LOW"], key="dash_risk")

    filtered = emp.copy()
    if sel_dept != "All Departments":
        filtered = filtered[filtered["Department"] == sel_dept]
    if sel_risk == "HIGH":
        filtered = filtered[filtered["RiskScore"] >= 0.70]
    elif sel_risk == "MEDIUM":
        filtered = filtered[(filtered["RiskScore"] >= 0.40) & (filtered["RiskScore"] < 0.70)]
    elif sel_risk == "LOW":
        filtered = filtered[filtered["RiskScore"] < 0.40]

    top15 = (filtered[["EmpID","Department","Tenure_Years","RiskScore",
                   "PerformanceScore","Salary","RaisonCourte","ActionCourte"]]
               .sort_values("RiskScore", ascending=False).head(15).copy())
    top15["Employee"]          = top15["EmpID"].apply(lambda x: f"Emp. #{x}")
    top15["Tenure"]            = top15["Tenure_Years"].apply(lambda x: f"{x:.1f} yrs")
    top15["Risk Score"]        = top15["RiskScore"].apply(lambda p: f"{p:.0%}")
    top15["Risk Level"]        = top15["RiskScore"].apply(
        lambda p: "HIGH" if p>=0.70 else "MEDIUM" if p>=0.40 else "LOW")
    top15["Primary Reason"]    = top15["RaisonCourte"]
    top15["Suggested Action"]  = top15["ActionCourte"]
    if len(top15) == 0:
        st.info("No employees match the selected filters.")
    else:
        st.dataframe(
            top15[["Employee","Department","Tenure","Risk Score","Risk Level","Primary Reason","Suggested Action"]]
                 .reset_index(drop=True),
            use_container_width=True, height=460,
        )
    st.caption("Click on a row, then use the Employee Profile page for the full profile.")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<p class="section-title">Risk Level Distribution</p>', unsafe_allow_html=True)
        fig_risk = go.Figure(go.Pie(
            labels=["High (\u2265 70%)", "Medium (40-70%)", "Low (< 40%)"],
            values=[n_high, n_med, n_low],
            marker=dict(colors=[C["danger"], C["warning"], C["success"]]),
            hole=0.45,
            textinfo="value+percent",
            textfont=dict(color=C["text"], size=13),
        ))
        fig_risk = styled_chart(fig_risk, height=320)
        fig_risk.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
            margin=dict(l=10, r=10, t=30, b=40),
        )
        st.plotly_chart(fig_risk, use_container_width=True)
        st.markdown(f"""
        <div style='font-size:.85rem;color:{C['text_muted']};margin-top:4px;'>
        Total employees: <b style='color:{C['text']};'>{len(emp)}</b> &nbsp;|&nbsp;
        High risk: <b style='color:{C['danger']};'>{n_high/len(emp):.1%}</b> &nbsp;|&nbsp;
        Medium risk: <b style='color:{C['warning']};'>{n_med/len(emp):.1%}</b>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<p class="section-title">Most Affected Departments</p>', unsafe_allow_html=True)
        dept_stats = (emp.groupby("Department")["Termd"]
                        .agg(["mean","count"])
                        .rename(columns={"mean":"Turnover Rate","count":"Headcount"})
                        .sort_values("Turnover Rate", ascending=True))
        avg = emp["Termd"].mean()
        bar_colors = [C["danger"] if r > avg else C["primary"] for r in dept_stats["Turnover Rate"]]
        fig_dept = go.Figure(go.Bar(
            x=dept_stats["Turnover Rate"] * 100,
            y=dept_stats.index,
            orientation="h",
            marker=dict(color=bar_colors),
            text=[f"{r:.1f}%" for r in dept_stats["Turnover Rate"] * 100],
            textposition="outside",
            textfont=dict(color=C["text"], size=12),
        ))
        fig_dept.add_vline(x=avg*100, line_dash="dash", line_color=C["text_muted"],
                           annotation_text=f"Avg {avg:.1%}", annotation_font_color=C["text_muted"])
        fig_dept = styled_chart(fig_dept, height=320)
        fig_dept.update_layout(
            xaxis_title="Turnover Rate (%)",
            margin=dict(l=10, r=40, t=30, b=40),
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        st.markdown(f"""
        <div style='font-size:.85rem;color:{C['text_muted']};margin-top:4px;'>
        Overall average turnover: <b style='color:{C['text']};'>{avg:.1%}</b>
        &nbsp;· Departments in red are above average
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="callout-green">
    <b>Frugal AI:</b> risk scores are computed by a Logistic Regression model with SHAP explanations —
    sub-millisecond inference, ~0g CO2 per update. Achieves comparable accuracy to heavier models
    on this data volume. See the AI Approach page for a full comparison.
    </div>""", unsafe_allow_html=True)

elif page == "Employee Profile":
    from pages_employees import render
    render(data)

elif page == "HR Analysis":
    from pages_analysis import render
    render(data)

elif page == "AI Approach":
    from pages_ia import render
    render(data)

elif page == "Compliance & Ethics":
    from pages_ia import render_compliance
    render_compliance(data)
