import streamlit as st
import numpy as np
import pandas as pd
from model import C, feat_fr


def render(data):
    df          = data["df"]
    emp         = data["emp"]
    text_df     = data["text_df"]
    sv          = data["sv"]
    feat_names  = data["feat_names"]
    mean_abs_sv = data["mean_abs_sv"]

    st.markdown(f"""
    <h1 style='color:{C['text']};margin-bottom:4px;'>HR Analysis</h1>
    <p style='color:{C['text_muted']};margin:0 0 20px 0;'>
    Strategic overview — departments, risk factors and feedback
    </p>""", unsafe_allow_html=True)

    st.markdown('<p class="section-title">By Department</p>', unsafe_allow_html=True)
    avg = df["Termd"].mean()
    dept_df = (df.groupby("Department").agg(
        Headcount=("Termd","count"), Turnover=("Termd","mean"),
        AvgSalary=("Salary","mean"), AvgTenure=("Tenure_Years","mean"),
    ).reset_index())
    dept_df["Turnover %"]      = (dept_df["Turnover"]*100).round(1).astype(str) + "%"
    dept_df["Avg Salary"]      = dept_df["AvgSalary"].apply(lambda x: f"${x:,.0f}")
    dept_df["Avg Tenure (yrs)"]= dept_df["AvgTenure"].apply(lambda x: f"{x:.1f}")
    dept_df["vs Average"]      = dept_df["Turnover"].apply(
        lambda r: f"+{(r-avg)*100:.1f}pp" if r > avg else f"{(r-avg)*100:.1f}pp")
    dept_df["Status"]          = dept_df["Turnover"].apply(
        lambda r: "HIGH RISK" if r > avg*1.25 else "ELEVATED" if r > avg else "OK")

    st.dataframe(
        dept_df[["Department","Headcount","Turnover %","vs Average","Status","Avg Salary","Avg Tenure (yrs)"]]
          .sort_values("Turnover %", ascending=False).reset_index(drop=True),
        use_container_width=True,
    )
    st.caption(f"Company average turnover: {avg:.1%} | Departments above +25% of average are flagged HIGH RISK")

    st.markdown('<p class="section-title">Factors Influencing Turnover</p>', unsafe_allow_html=True)
    st.caption("Top 8 factors by mean absolute SHAP value — computed by the AI model across all employees")

    top8_idx  = np.argsort(mean_abs_sv)[::-1][:8]
    top8_feat = [feat_fr(feat_names[i]) for i in top8_idx]
    top8_vals = [mean_abs_sv[i] for i in top8_idx]
    top8_pct  = [v / sum(top8_vals) * 100 for v in top8_vals]

    factors_df = pd.DataFrame({
        "Rank": range(1, len(top8_feat)+1),
        "Factor": top8_feat,
        "SHAP Importance": [f"{v:.4f}" for v in top8_vals],
        "% of Top 8": [f"{p:.1f}%" for p in top8_pct],
    })
    st.dataframe(factors_df, use_container_width=True, hide_index=True)

    THEME_EN = {
        "compensation":     "Compensation",
        "management":       "Management",
        "career_growth":    "Career Growth",
        "work_life_balance":"Work-Life Balance",
        "culture":          "Company Culture",
        "job_fit":          "Job Fit",
        "external":         "External Reasons",
        "team_dynamics":    "Team Dynamics",
    }
    exit_texts = text_df[text_df["Type"]=="exit"].copy()
    exit_texts["Theme EN"] = exit_texts["Theme"].map(THEME_EN).fillna("Other")
    theme_counts = exit_texts["Theme EN"].value_counts().reset_index()
    theme_counts.columns = ["Theme", "Mentions"]
    theme_counts["% of Exit Interviews"] = (theme_counts["Mentions"] / theme_counts["Mentions"].sum() * 100).round(1).astype(str) + "%"

    st.markdown('<p class="section-title">Exit Interview Themes</p>', unsafe_allow_html=True)
    st.dataframe(theme_counts, use_container_width=True, hide_index=True)

    rev_en    = {v:k for k,v in THEME_EN.items()}
    sel_theme = st.selectbox("View examples for theme:", theme_counts["Theme"].tolist(), key="th_ex")
    raw_theme = rev_en.get(sel_theme, sel_theme)
    examples  = exit_texts[exit_texts["Theme"]==raw_theme]["Text"].head(3)
    for ex in examples:
        st.markdown(f"""
        <div style="background:{C['card_bg']};border:1px solid {C['card_border']};
                    border-left:3px solid {C['danger']};
                    padding:10px 14px;border-radius:0 8px 8px 0;margin:5px 0;
                    font-style:italic;color:{C['text']};font-size:.9rem;">"{ex}"</div>""",
                    unsafe_allow_html=True)

    st.markdown('<p class="section-title">Salary: Leavers vs. Active Employees</p>', unsafe_allow_html=True)
    salary_stats = df.groupby("Termd")["Salary"].agg(["mean","median","min","max","count"]).reset_index()
    salary_stats["Group"] = salary_stats["Termd"].map({0:"Active Employees", 1:"Leavers"})
    salary_stats["Avg Salary"]    = salary_stats["mean"].apply(lambda x: f"${x:,.0f}")
    salary_stats["Median Salary"] = salary_stats["median"].apply(lambda x: f"${x:,.0f}")
    salary_stats["Min Salary"]    = salary_stats["min"].apply(lambda x: f"${x:,.0f}")
    salary_stats["Max Salary"]    = salary_stats["max"].apply(lambda x: f"${x:,.0f}")
    salary_stats["Count"]         = salary_stats["count"].astype(int)
    st.dataframe(
        salary_stats[["Group","Count","Avg Salary","Median Salary","Min Salary","Max Salary"]]
            .reset_index(drop=True),
        use_container_width=True, hide_index=True
    )
    avg_active  = df[df["Termd"]==0]["Salary"].mean()
    avg_leaver  = df[df["Termd"]==1]["Salary"].mean()
    diff        = avg_leaver - avg_active
    st.markdown(f"""
    <div style='font-size:.85rem;color:{C['text_muted']};margin-top:8px;'>
    Average salary of leavers is <b style='color:{C['text']};'>${abs(diff):,.0f}</b>
    {"less" if diff < 0 else "more"} than active employees ({diff/avg_active*100:+.1f}%).
    </div>""", unsafe_allow_html=True)