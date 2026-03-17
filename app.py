import warnings; warnings.filterwarnings("ignore")
import streamlit as st
import pandas as pd
import numpy as np
from model import load_all, C, styled_chart, risk_emoji

st.set_page_config(
    page_title="TalentGuard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
html, body, [class*="css"] { font-family: 'Segoe UI', system-ui, sans-serif; }
.card {
    background: #1B2332;
    border: 1px solid #2D3748;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
}
.card h3 { color: #F1F5F9; margin: 0 0 8px 0; }
.card p  { color: #94A3B8; margin: 0; }
.kpi {
    background: #1B2332;
    border: 1px solid #2D3748;
    border-radius: 12px;
    padding: 22px 18px;
    text-align: center;
    border-top: 3px solid #3B82F6;
}
.kpi-danger  { border-top-color: #EF4444; }
.kpi-warning { border-top-color: #F59E0B; }
.kpi-success { border-top-color: #10B981; }
.kpi h2  { margin:0; font-size:2.4rem; font-weight:700; color:#F1F5F9; line-height:1.1; }
.kpi p   { margin:4px 0 0 0; font-size:.85rem; color:#94A3B8; }
.kpi small { font-size:.78rem; color:#94A3B8; }
.section-title {
    font-size:1.1rem; font-weight:700; color:#F1F5F9;
    border-left:4px solid #3B82F6; padding-left:10px;
    margin: 22px 0 12px 0;
}
.profile-header {
    background: linear-gradient(90deg, #1B2332 0%, #1e3a5f 100%);
    border: 1px solid #2D3748;
    border-radius: 12px;
    color: #F1F5F9;
    padding: 22px 26px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 16px;
}
.badge {
    display:inline-block; padding:5px 14px; border-radius:20px;
    font-weight:700; font-size:.9rem;
}
.badge-high   { background:#450a0a; color:#fca5a5; border:1px solid #EF4444; }
.badge-medium { background:#451a03; color:#fcd34d; border:1px solid #F59E0B; }
.badge-low    { background:#052e16; color:#6ee7b7; border:1px solid #10B981; }
.action-row {
    display:flex; align-items:flex-start; gap:12px;
    padding:10px 0; border-bottom:1px solid #2D3748;
}
.action-icon { font-size:1.0rem; font-weight:700; min-width:48px; color:#94A3B8; }
.priority-haute   { background:#450a0a; color:#fca5a5; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; }
.priority-moyenne { background:#451a03; color:#fcd34d; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; }
.priority-info    { background:#1e3a5f; color:#93c5fd; padding:2px 8px; border-radius:8px; font-size:.75rem; font-weight:600; }
.callout-green {
    background:#052e16; border-left:4px solid #10B981;
    padding:14px 18px; border-radius:0 10px 10px 0;
    color:#6ee7b7; font-weight:500; margin:12px 0;
}
.callout-blue {
    background:#1e3a5f; border-left:4px solid #3B82F6;
    padding:14px 18px; border-radius:0 10px 10px 0;
    color:#93c5fd; font-weight:500; margin:12px 0;
}
.theme-badge {
    display:inline-block; background:#1e3a5f; color:#93c5fd;
    border:1px solid #3B82F6; border-radius:20px;
    padding:3px 12px; font-size:.8rem; font-weight:600;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

data = load_all()
emp  = data["emp"]

n_high = (emp["RiskScore"]>=0.70).sum()
n_med  = ((emp["RiskScore"]>=0.40)&(emp["RiskScore"]<0.70)).sum()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:18px 0 26px 0;'>
      <div style='font-size:1.5rem;font-weight:700;letter-spacing:1px;color:#F1F5F9;'>TalentGuard</div>
      <div style='font-size:.72rem;color:#94A3B8;margin-top:4px;'>Talent Retention Platform — Capgemini</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio(
        "Menu",
        ["Dashboard", "Employee Profile", "HR Analysis",
         "—",
         "AI Approach", "Compliance & Ethics"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:.83rem;line-height:1.9;color:#94A3B8;'>
      <b style='color:#EF4444;'>{n_high}</b> high-risk employees<br>
      <b style='color:#F59E0B;'>{n_med}</b> to monitor<br>
      <hr style='border-color:#2D3748;margin:8px 0;'>
      <span style='font-size:.7rem;'>
        <b style='color:#10B981;'>Frugal AI</b> — Logistic Regression<br>
        <b style='color:#3B82F6;'>Explainable AI</b> — SHAP active
      </span>
    </div>""", unsafe_allow_html=True)

if page == "—":
    st.info("Select a page from the menu.")
    st.stop()

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
            <small>Above sector average</small></div>""", unsafe_allow_html=True)
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

    top15 = (emp[["EmpID","Department","Tenure_Years","RiskScore",
                   "PerformanceScore","Salary","RaisonCourte","ActionCourte"]]
               .sort_values("RiskScore", ascending=False).head(15).copy())
    top15["Employee"]          = top15["EmpID"].apply(lambda x: f"Emp. #{x}")
    top15["Department"]        = top15["Department"]
    top15["Tenure"]            = top15["Tenure_Years"].apply(lambda x: f"{x:.1f} yrs")
    top15["Risk Score"]        = top15["RiskScore"].apply(lambda p: f"{p:.0%}")
    top15["Risk Level"]        = top15["RiskScore"].apply(
        lambda p: "HIGH" if p>=0.70 else "MEDIUM" if p>=0.40 else "LOW")
    top15["Primary Reason"]    = top15["RaisonCourte"]
    top15["Suggested Action"]  = top15["ActionCourte"]
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
        risk_summary = pd.DataFrame({
            "Risk Level": ["High (>= 70%)", "Medium (40-70%)", "Low (< 40%)"],
            "Count": [n_high, n_med, n_low],
            "% of Workforce": [f"{n_high/len(emp):.1%}", f"{n_med/len(emp):.1%}", f"{n_low/len(emp):.1%}"],
        })
        st.dataframe(risk_summary, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div style='font-size:.85rem;color:{C['text_muted']};margin-top:8px;'>
        Total employees: <b style='color:{C['text']};'>{len(emp)}</b> &nbsp;|&nbsp;
        High risk: <b style='color:#EF4444;'>{n_high/len(emp):.1%}</b> &nbsp;|&nbsp;
        Medium risk: <b style='color:#F59E0B;'>{n_med/len(emp):.1%}</b>
        </div>""", unsafe_allow_html=True)

    with col_r:
        st.markdown('<p class="section-title">Most Affected Departments</p>', unsafe_allow_html=True)
        dept_stats = (emp.groupby("Department")["Termd"]
                        .agg(["mean","count"])
                        .rename(columns={"mean":"Turnover Rate","count":"Headcount"})
                        .sort_values("Turnover Rate", ascending=False))
        avg = emp["Termd"].mean()
        dept_display = dept_stats.copy()
        dept_display["Turnover %"] = (dept_display["Turnover Rate"]*100).round(1).astype(str) + "%"
        dept_display["vs Average"] = dept_display["Turnover Rate"].apply(
            lambda r: f"+{(r-avg)*100:.1f}pp" if r > avg else f"{(r-avg)*100:.1f}pp")
        dept_display = dept_display.drop(columns=["Turnover Rate"]).reset_index()
        dept_display.columns = ["Department", "Headcount", "Turnover %", "vs Avg"]
        st.dataframe(dept_display, use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div style='font-size:.85rem;color:{C['text_muted']};margin-top:8px;'>
        Overall average turnover: <b style='color:{C['text']};'>{avg:.1%}</b>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="callout-green">
    <b>Frugal AI:</b> this dashboard is computed by a Logistic Regression model —
    0.001 second inference, ~0g CO2 per update. As accurate as a neural network
    on this data volume.
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
