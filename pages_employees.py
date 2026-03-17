import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from model import (C, styled_chart, feat_fr, get_top_shap, risk_emoji,
                   risk_badge_html, generate_explanation_fr, generate_actions_fr)


def render(data):
    emp        = data["emp"]
    sv         = data["sv"]
    feat_names = data["feat_names"]
    df         = data["df"]
    text_df    = data["text_df"]

    st.markdown(f"""
    <h1 style='color:{C['text']};margin-bottom:4px;'>Employee Profile</h1>
    <p style='color:{C['text_muted']};margin:0 0 20px 0;'>
    Detailed risk profile, explanation and recommended action plan
    </p>""", unsafe_allow_html=True)

    col_filt, col_sel = st.columns([1,3])
    with col_filt:
        filtre = st.radio("Filter", ["All","High","Medium","Low"],
                          label_visibility="collapsed")
    with col_sel:
        if filtre == "High":
            pool = emp[emp["RiskScore"]>=0.70]
        elif filtre == "Medium":
            pool = emp[(emp["RiskScore"]>=0.40)&(emp["RiskScore"]<0.70)]
        elif filtre == "Low":
            pool = emp[emp["RiskScore"]<0.40]
        else:
            pool = emp
        pool_sorted = pool.sort_values("RiskScore", ascending=False)
        options = [(idx, f"Emp. #{pool_sorted.loc[idx,'EmpID']} — "
                         f"{pool_sorted.loc[idx,'Department']} — "
                         f"{pool_sorted.loc[idx,'RiskScore']:.0%} ({risk_emoji(pool_sorted.loc[idx,'RiskScore'])})")
                   for idx in pool_sorted.index]
        if not options:
            st.warning("No employees in this category.")
            st.stop()
        labels    = [o[1] for o in options]
        sel_label = st.selectbox("Select an employee", labels, label_visibility="collapsed")
        sel_idx   = options[labels.index(sel_label)][0]

    e        = emp.loc[sel_idx]
    risk     = e["RiskScore"]
    sv_emp   = sv[sel_idx]
    badge_cls = "badge-high" if risk>=0.70 else "badge-medium" if risk>=0.40 else "badge-low"

    st.markdown(f"""
    <div class="profile-header">
      <div>
        <div style='font-size:1.4rem;font-weight:700;color:{C['text']};'>
          Employee #{int(e['EmpID'])}
        </div>
        <div style='color:{C['text_muted']};margin-top:5px;font-size:.93rem;'>
          {e['Department']} · {e['Position']}
        </div>
        <div style='color:{C['text_muted']};margin-top:3px;font-size:.88rem;'>
          Tenure: <b style='color:{C['text']};'>{e['Tenure_Years']:.1f} yrs</b> &nbsp;·&nbsp;
          Salary: <b style='color:{C['text']};'>${e['Salary']:,}</b> &nbsp;·&nbsp;
          Performance: <b style='color:{C['text']};'>{e['PerformanceScore']}</b>
        </div>
        <div style='color:{C['text_muted']};margin-top:3px;font-size:.88rem;'>
          Engagement: <b style='color:{C['text']};'>{e['EngagementSurvey']:.1f}/5</b> &nbsp;·&nbsp;
          Satisfaction: <b style='color:{C['text']};'>{int(e['EmpSatisfaction'])}/5</b> &nbsp;·&nbsp;
          Absences: <b style='color:{C['text']};'>{int(e['Absences'])} days</b>
        </div>
      </div>
      <div>
        <span class="badge {badge_cls}">RISK {risk:.0%} — {risk_emoji(risk)}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <p class="section-title">
      Why this risk level?
      <span class="theme-badge">Explainable AI</span>
    </p>""", unsafe_allow_html=True)

    top_n      = 7
    top_pairs  = sorted(zip(sv_emp, feat_names), key=lambda x: abs(x[0]), reverse=True)[:top_n]
    shap_vals  = [v for v,_ in top_pairs]
    shap_feats = [feat_fr(f) for _,f in top_pairs]

    col_chart, col_expl = st.columns([3,2])
    with col_chart:
        bar_colors = [C["danger"] if v > 0 else C["success"] for v in shap_vals]
        fig_shap = go.Figure(go.Bar(
            x=shap_vals[::-1],
            y=shap_feats[::-1],
            orientation="h",
            marker=dict(color=bar_colors[::-1]),
            text=[f"{v:+.4f}" for v in shap_vals[::-1]],
            textposition="outside",
            textfont=dict(color=C["text"], size=11),
        ))
        fig_shap = styled_chart(fig_shap, height=300)
        fig_shap.update_layout(
            xaxis_title="SHAP Value",
            margin=dict(l=10, r=50, t=20, b=30),
        )
        fig_shap.add_vline(x=0, line_color=C["card_border"])
        st.plotly_chart(fig_shap, use_container_width=True)
        st.caption("Red = increases departure risk | Green = reduces departure risk | Bar length = intensity")

    with col_expl:
        st.markdown("<br>", unsafe_allow_html=True)
        expl = generate_explanation_fr(e, sv_emp, feat_names, df)
        st.markdown(f"""
        <div style="background:{C['card_bg']};border:1px solid {C['card_border']};
                    border-left:4px solid {C['primary']};
                    padding:16px 18px;border-radius:0 10px 10px 0;
                    font-size:.93rem;line-height:1.6;color:{C['text']};">
          <b style='color:{C['primary']};'>Explanation:</b><br><br>{expl}
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    emp_texts   = text_df[text_df["EmpIndex"]==sel_idx]
    exit_rows   = emp_texts[emp_texts["Type"]=="exit"]
    survey_rows = emp_texts[emp_texts["Type"]=="survey"]
    transf_rows = emp_texts[emp_texts["Type"]=="transfer"]

    total_fb = len(exit_rows)+len(survey_rows)+len(transf_rows)
    if total_fb > 0:
        st.markdown('<p class="section-title">Latest Feedback</p>', unsafe_allow_html=True)
        n_cols  = min(3, total_fb)
        cols_fb = st.columns(n_cols)
        ci = 0
        if len(exit_rows) > 0:
            with cols_fb[ci % n_cols]:
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {C['danger']}; padding: 18px;">
                  <div style="font-size:.75rem;font-weight:700;color:{C['danger']};margin-bottom:12px;letter-spacing:0.5px;">
                    <i class="fas fa-sign-out-alt"></i> EXIT INTERVIEW</div>
                  <div style="font-style:italic;font-size:.95rem;color:{C['text']};line-height:1.6;">
                    "{exit_rows.iloc[0]['Text']}"</div>
                </div>""", unsafe_allow_html=True)
            ci += 1
        if len(survey_rows) > 0:
            is_neg  = survey_rows.iloc[0]["Theme"]=="survey_neg"
            col_bd  = C["danger"] if is_neg else C["success"]
            with cols_fb[ci % n_cols]:
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {col_bd}; padding: 18px;">
                  <div style="font-size:.75rem;font-weight:700;color:{col_bd};margin-bottom:12px;letter-spacing:0.5px;">
                    <i class="fas fa-poll"></i> SATISFACTION SURVEY</div>
                  <div style="font-style:italic;font-size:.95rem;color:{C['text']};line-height:1.6;">
                    "{survey_rows.iloc[0]['Text']}"</div>
                </div>""", unsafe_allow_html=True)
            ci += 1
        if len(transf_rows) > 0:
            with cols_fb[ci % n_cols]:
                st.markdown(f"""
                <div class="card" style="border-left:4px solid {C['primary']}; padding: 18px;">
                  <div style="font-size:.75rem;font-weight:700;color:{C['primary']};margin-bottom:12px;letter-spacing:0.5px;">
                    <i class="fas fa-exchange-alt"></i> INTERNAL MOBILITY REQUEST</div>
                  <div style="font-style:italic;font-size:.95rem;color:{C['text']};line-height:1.6;">
                    "{transf_rows.iloc[0]['Text']}"</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p class="section-title">Recommended Action Plan</p>', unsafe_allow_html=True)

    actions = generate_actions_fr(sv_emp, feat_names, e, text_df)
    for i, (icon, text_action, priority, delai) in enumerate(actions, 1):
        if priority == "HIGH":
            pbadge = '<span class="priority-haute">HIGH</span>'
        elif priority == "MEDIUM":
            pbadge = '<span class="priority-moyenne">MEDIUM</span>'
        else:
            pbadge = '<span class="priority-info">INFO</span>'
        st.markdown(f"""
        <div class="action-row">
          <div class="action-icon">[{icon}]</div>
          <div style="flex:1;">
            <span style="font-weight:600;color:{C['text']};">{i}. {text_action}</span><br>
            <span style="font-size:.82rem;color:{C['text_muted']};">
              Priority: {pbadge} &nbsp;·&nbsp; Suggested timeline: {delai}
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("View all high-risk employees"):
        high_risk = (emp[emp["RiskScore"]>=0.60]
                     [["EmpID","Department","Tenure_Years","RiskScore","PerformanceScore","Salary","RaisonCourte"]]
                     .sort_values("RiskScore", ascending=False).head(20).copy())
        high_risk["Risk Score"]  = high_risk["RiskScore"].apply(lambda p: f"{p:.0%}")
        high_risk["Risk Level"]  = high_risk["RiskScore"].apply(
            lambda p: "HIGH" if p>=0.70 else "MEDIUM")
        high_risk["Tenure"]      = high_risk["Tenure_Years"].apply(lambda x: f"{x:.1f} yrs")
        high_risk["Salary"]      = high_risk["Salary"].apply(lambda x: f"${x:,}")
        high_risk.rename(columns={"EmpID":"ID","Department":"Department",
                                   "PerformanceScore":"Performance",
                                   "RaisonCourte":"Primary Reason"}, inplace=True)
        st.dataframe(
            high_risk[["ID","Department","Risk Score","Risk Level","Tenure","Performance","Salary","Primary Reason"]]
                     .reset_index(drop=True),
            use_container_width=True, height=340,
        )