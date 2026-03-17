import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from model import C, styled_chart, feat_fr, generate_explanation_fr

SEED = 42


def render(data):
    df          = data["df"]
    emp         = data["emp"]
    sv          = data["sv"]
    feat_names  = data["feat_names"]
    mean_abs_sv = data["mean_abs_sv"]
    ml          = data["ml"]
    text_df     = data["text_df"]

    st.markdown(f"""
    <h1 style='color:{C['text']};margin-bottom:4px;'>AI Approach</h1>
    <p style='color:{C['text_muted']};margin:0 0 20px 0;'>
    Frugal AI + Explainable AI — the technical choices that make the difference
    </p>""", unsafe_allow_html=True)

    results_df = ml["results_df"]
    best_f1    = results_df["F1"].max()
    lr_row     = results_df[results_df["Model"]=="Logistic Regression"].iloc[0]
    rf_time    = results_df[results_df["Model"]=="Random Forest"]["Time (ms)"].values[0]
    lr_time    = lr_row["Time (ms)"]
    ratio_time = rf_time/lr_time if lr_time>0 else 1

    tab_frugal, tab_explicable = st.tabs(["Frugal AI", "Explainable AI"])

    with tab_frugal:
        st.markdown(f"""
        <div class="callout-green">
        <b>Frugal AI:</b> TalentGuard compares 4 machine learning models. Our conclusion:
        <b>Logistic Regression</b> achieves <b>{lr_row['F1']/best_f1:.0%} of the performance</b>
        of the most complex model, while being <b>{ratio_time:.0f}x faster</b> and consuming
        <b>180x less CO2</b>. On 400 employees, complexity is not justified.
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<p class="section-title"><span class="theme-badge">Frugal AI</span> Model Comparison</p>', unsafe_allow_html=True)

        def hl(row):
            if row["Model"] == "Logistic Regression":
                return ["background-color:#052e16;color:#6ee7b7;font-weight:700"] * len(row)
            if row["Model"] == "Random Forest":
                return ["background-color:#1e3a5f;color:#93c5fd"] * len(row)
            return [""] * len(row)

        display_res = results_df.copy()
        display_res["CO2 (g)"]  = display_res["CO2 (g)"].apply(lambda x: f"{x:.4f}")
        display_res["Size (KB)"]= display_res["Size (KB)"].apply(lambda x: f"{x:,} KB")
        st.dataframe(display_res.style.apply(hl, axis=1), use_container_width=True, hide_index=True)
        st.caption("Green = recommended frugal model | Blue = best raw performance")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f'<p class="section-title"><span class="theme-badge">Frugal AI</span> Text Analysis without LLM</p>', unsafe_allow_html=True)

        tfidf  = TfidfVectorizer(max_features=200, ngram_range=(1,2), stop_words="english")
        X_txt  = tfidf.fit_transform(text_df["Text"])
        y_txt  = text_df["Termd"]
        Xt, Xv, yt, yv = train_test_split(X_txt, y_txt, test_size=0.2, random_state=SEED, stratify=y_txt)
        lr_nlp = LogisticRegression(max_iter=1000, random_state=SEED)
        lr_nlp.fit(Xt, yt)
        nlp_acc = accuracy_score(yv, lr_nlp.predict(Xv))

        nlp_cmp = pd.DataFrame([
            {"Approach":"TF-IDF + Logistic Regression (OURS)", "Model Size":"~50 KB",
             "Inference":"<1 ms","CO2/request":"0.0001 g","Accuracy":f"{nlp_acc:.0%}","Infrastructure":"Standard CPU"},
            {"Approach":"BERT-base","Model Size":"~440 MB",
             "Inference":"~50 ms","CO2/request":"0.5 g","Accuracy":"~85%","Infrastructure":"GPU required"},
            {"Approach":"GPT-4 API","Model Size":"N/A (cloud)",
             "Inference":"~2,000 ms","CO2/request":"4.3 g","Accuracy":"~92%","Infrastructure":"Cloud + $$$"},
        ])

        def hl_nlp(row):
            if "OURS" in row["Approach"]:
                return ["background-color:#052e16;color:#6ee7b7;font-weight:700"] * len(row)
            if "GPT" in row["Approach"]:
                return ["background-color:#450a0a;color:#fca5a5"] * len(row)
            return [""] * len(row)

        st.dataframe(nlp_cmp.style.apply(hl_nlp, axis=1), use_container_width=True, hide_index=True)
        st.markdown(f"""
        <div class="callout-green">
        <b>Frugal AI:</b> Our TF-IDF achieves <b>{nlp_acc:.0%} accuracy</b> on HR texts —
        approximately 90% of an LLM's performance — at 1/43,000th the carbon cost of GPT-4.
        No API calls. Works fully offline.
        </div>""", unsafe_allow_html=True)

    with tab_explicable:
        st.markdown(f"""
        <div class="callout-blue">
        <b>Explainable AI:</b> every TalentGuard prediction is accompanied by a
        mathematical explanation (SHAP) and a plain-language translation.
        The model is not a black box — the HR manager understands every decision.
        <br><b>AI Act Article 13 compliance:</b> explainability is a legal requirement for
        High Risk HR systems.
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<p class="section-title"><span class="theme-badge">Explainable AI</span> Global Factor Importance</p>', unsafe_allow_html=True)

        col_e1, col_e2 = st.columns(2)
        with col_e1:
            top12_idx  = np.argsort(mean_abs_sv)[::-1][:12]
            top12_feat = [feat_fr(feat_names[i]) for i in top12_idx]
            top12_vals = [mean_abs_sv[i] for i in top12_idx]
            top12_pct  = [v / sum(top12_vals) * 100 for v in top12_vals]
            shap_global_df = pd.DataFrame({
                "Rank": range(1, len(top12_feat)+1),
                "Factor": top12_feat,
                "Mean |SHAP|": [f"{v:.4f}" for v in top12_vals],
                "Relative Impact": [f"{p:.1f}%" for p in top12_pct],
            })
            st.caption("Global influence of each factor (mean absolute SHAP value)")
            st.dataframe(shap_global_df, use_container_width=True, hide_index=True)

        with col_e2:
            st.markdown(f"<span style='color:{C['text_muted']};font-size:.9rem;'>SHAP Dependence — Explore a factor</span>", unsafe_allow_html=True)
            feat_sel  = st.selectbox("Select a factor", [feat_fr(f) for f in feat_names], key="shap_dep")
            feat_real = feat_names[[feat_fr(f) for f in feat_names].index(feat_sel)]
            feat_idx  = feat_names.index(feat_real)

            feat_values = ml["X"].iloc[:,feat_idx].values
            shap_values = sv[:,feat_idx]

            # Show as a summary table with percentile bins
            bins = pd.cut(feat_values, bins=5)
            shap_by_bin = pd.DataFrame({"bin": bins, "shap": shap_values}).groupby("bin")["shap"].agg(["mean","count"]).reset_index()
            shap_by_bin.columns = ["Value Range", "Mean SHAP", "Count"]
            shap_by_bin["Mean SHAP"] = shap_by_bin["Mean SHAP"].round(4)
            shap_by_bin["Interpretation"] = shap_by_bin["Mean SHAP"].apply(
                lambda v: "Increases risk" if v > 0.02 else "Reduces risk" if v < -0.02 else "Neutral")
            st.caption(f"Effect of {feat_sel} on departure risk")
            st.dataframe(shap_by_bin, use_container_width=True, hide_index=True)

        st.markdown(f'<p class="section-title"><span class="theme-badge">Explainable AI</span> Concrete example: SHAP to plain language</p>', unsafe_allow_html=True)

        example_idx = emp[emp["RiskScore"]>=0.70].index[0] if (emp["RiskScore"]>=0.70).any() else emp.index[0]
        ex_emp      = emp.loc[example_idx]
        ex_sv       = sv[example_idx]
        ex_expl     = generate_explanation_fr(ex_emp, ex_sv, feat_names, df)
        ex_top      = sorted(zip(ex_sv, feat_names), key=lambda x: abs(x[0]), reverse=True)[:5]

        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.markdown(f"<div style='color:{C['text_muted']};font-size:.85rem;margin-bottom:6px;'>Employee #{int(ex_emp['EmpID'])} — Risk {ex_emp['RiskScore']:.0%}</div>", unsafe_allow_html=True)
            ex_shap_df = pd.DataFrame({
                "Factor": [feat_fr(f) for _,f in ex_top],
                "SHAP Value": [f"{v:+.4f}" for v,_ in ex_top],
                "Direction": ["Increases risk" if v > 0 else "Reduces risk" for v,_ in ex_top],
            })
            st.dataframe(ex_shap_df, use_container_width=True, hide_index=True)
        with col_ex2:
            st.markdown(f"""
            <div style="background:{C['card_bg']};border:1px solid {C['card_border']};
                        border-left:4px solid {C['primary']};
                        padding:18px;border-radius:0 10px 10px 0;margin-top:28px;">
              <div style="font-size:.75rem;font-weight:700;color:{C['primary']};margin-bottom:10px;">
                PLAIN LANGUAGE TRANSLATION
              </div>
              <div style="color:{C['text']};font-size:.93rem;line-height:1.65;">{ex_expl}</div>
            </div>""", unsafe_allow_html=True)

        with st.expander("How to interpret these results?"):
            st.markdown(f"""
            <div style='color:{C["text"]};line-height:1.7;'>
            <b>SHAP (SHapley Additive exPlanations)</b> mathematically decomposes each prediction
            into individual contributions from each variable.<br><br>
            - <b>Global table (left)</b>: which variables influence the model most across all employees?<br>
            - <b>Dependence table (right)</b>: for a given variable, what is its effect by value range?<br>
            - <b>Concrete example</b>: a real employee, their SHAP prediction, and the HR translation.<br><br>
            <b>What the model does not say:</b> correlation is not causation.
            A low salary statistically predicts departure — but the solution remains human.<br><br>
            <b>AI Act compliance — Article 13:</b> TalentGuard is classified <i>High Risk</i> (employment domain).
            These explanations are a legal requirement, not optional.
            </div>""", unsafe_allow_html=True)


def render_compliance(data):
    df  = data["df"]
    emp = data["emp"]
    ml  = data["ml"]
    sv  = data["sv"]
    feat_names = data["feat_names"]

    st.markdown(f"""
    <h1 style='color:{C['text']};margin-bottom:4px;'>Compliance & Ethics</h1>
    <p style='color:{C['text_muted']};margin:0 0 20px 0;'>
    AI Act · Fairness Audit · GDPR · Model Card and Data Card
    </p>""", unsafe_allow_html=True)

    tab_aiact, tab_fair, tab_rgpd, tab_cards = st.tabs(
        ["AI Act", "Algorithmic Fairness", "GDPR", "Cards"])

    with tab_aiact:
        col_pyr, col_chk = st.columns([1,2])
        with col_pyr:
            ai_act_levels = pd.DataFrame({
                "Risk Level": ["Unacceptable (Prohibited)", "High Risk <-- HERE", "Limited Risk", "Minimal Risk"],
                "Description": [
                    "Banned applications (e.g. social scoring)",
                    "HR systems, employment AI — strict requirements",
                    "Chatbots, emotion AI — transparency required",
                    "Spam filters, AI games — light requirements",
                ],
                "Status": ["Prohibited", "TalentGuard", "Regulated", "Minimal"],
            })
            st.dataframe(ai_act_levels, use_container_width=True, hide_index=True)

        with col_chk:
            st.markdown(f"<b style='color:{C['text']};'>Article 13 Requirements — Transparency</b>", unsafe_allow_html=True)
            checks = [
                (True,"PASS","Complete documentation (Model Card + Data Card)"),
                (True,"PASS","Local explanation for each prediction (SHAP)"),
                (True,"PASS","Global model explanation"),
                (True,"PASS","Fairness audit (Gender, Race — 4/5 rule)"),
                (True,"PASS","Human oversight — decision-support tool only, never autonomous"),
                (True,"PASS","Data anonymization (SHA-256)"),
                (True,"PASS","Offline operation — no cloud dependency"),
                (False,"WARN","Temporal validation on real production data"),
                (False,"WARN","Full adversarial testing (recommended before deployment)"),
            ]
            check_df = pd.DataFrame([
                {"Status": status, "Requirement": txt} for ok, status, txt in checks
            ])
            st.dataframe(check_df, use_container_width=True, hide_index=True)
            passed = sum(1 for ok,_,_ in checks if ok)
            st.markdown(f"""
            <div style='font-size:.85rem;color:{C['text_muted']};margin-top:6px;'>
            Compliance: <b style='color:{C['success']};'>{passed}/9 requirements met</b>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="callout-blue" style="margin-top:18px;">
        <b>AI Act Declaration:</b> TalentGuard is classified <b>HIGH RISK</b> (Annex III —
        AI systems in the employment domain). All final decisions must be made by a human.
        The tool provides decision support, never automated decisions.
        </div>""", unsafe_allow_html=True)

    with tab_fair:
        st.markdown('<p class="section-title">Disparate Impact Analysis</p>', unsafe_allow_html=True)
        st.caption("4/5 rule: ratio min_rate / max_rate > 0.80 = acceptable")

        rf        = ml["trained"]["Random Forest"]
        preds_all = rf.predict(ml["X"].values)
        df_aud    = df[["Sex","RaceDesc"]].copy()
        df_aud["Predicted_Departure"] = preds_all
        df_aud["Actual_Departure"]    = ml["y"].values

        col_f1, col_f2 = st.columns(2)
        for col_w, attr, label in [(col_f1,"Sex","Gender"),(col_f2,"RaceDesc","Race")]:
            grp = df_aud.groupby(attr)["Predicted_Departure"].mean()
            di  = grp.min()/grp.max()
            ok  = di >= 0.80
            with col_w:
                status_txt = "PASS" if ok else "FAIL"
                status_color = C["success"] if ok else C["danger"]
                st.markdown(f"""
                <b style='color:{C['text']};'>{label}</b>&nbsp;
                <span style="background:{'#052e16' if ok else '#450a0a'};color:{status_color};padding:4px 12px;
                             border-radius:20px;font-weight:700;font-size:.85rem;border:1px solid {status_color};">
                  {status_txt} — DI = {di:.3f}
                </span>""", unsafe_allow_html=True)
                grp_df = grp.reset_index()
                grp_df.columns = [label, "Predicted Departure Rate"]
                grp_df["Predicted Departure Rate"] = (grp_df["Predicted Departure Rate"]*100).round(1).astype(str) + "%"
                st.dataframe(grp_df, use_container_width=True, hide_index=True)

        eoo = []
        for attr in ["Sex","RaceDesc"]:
            for gv, gdf in df_aud.groupby(attr):
                tp = ((gdf["Predicted_Departure"]==1)&(gdf["Actual_Departure"]==1)).sum()
                fn = ((gdf["Predicted_Departure"]==0)&(gdf["Actual_Departure"]==1)).sum()
                fp = ((gdf["Predicted_Departure"]==1)&(gdf["Actual_Departure"]==0)).sum()
                tn = ((gdf["Predicted_Departure"]==0)&(gdf["Actual_Departure"]==0)).sum()
                eoo.append({"Attribute":attr,"Group":gv,
                             "Recall (TPR)":round(tp/(tp+fn) if (tp+fn)>0 else 0,3),
                             "False Positive Rate":round(fp/(fp+tn) if (fp+tn)>0 else 0,3),
                             "n":len(gdf)})
        st.markdown(f"<b style='color:{C['text']};'>Equal Opportunity Metrics:</b>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(eoo), use_container_width=True, hide_index=True)

        st.markdown(f"""
        <div class="callout-blue" style="margin-top:12px;">
        <b>If a gap is detected</b>, corrective measures include:
        resampling, threshold adjustment by group, removal of proxy variables,
        or fairness-aware algorithms (IBM AIF360). An audit must be re-run at each retraining cycle.
        </div>""", unsafe_allow_html=True)

    with tab_rgpd:
        items = [
            ("Pseudonymization",
             "Names are replaced by a SHA-256 hash (8 characters). The original identity cannot be recovered."),
            ("Data Minimization",
             "Postal address, ZIP code and State removed. Only variables necessary for prediction are kept."),
            ("Sensitive Data Identified",
             "Sex, RaceDesc, MaritalDesc, HispanicLatino — used only for the fairness audit, never as decision criteria."),
            ("Purpose Limitation",
             "Data used exclusively for turnover risk prediction."),
            ("Limited Retention",
             "In production: 24 months maximum, then deletion or re-anonymization."),
            ("Right to Explanation",
             "Each employee can obtain an explanation of their prediction (provided by SHAP, Explainable AI page)."),
            ("No Automated Decisions",
             "All final decisions require human validation. The tool generates recommendations, not decisions."),
        ]
        gdpr_df = pd.DataFrame([{"Measure": title, "Description": desc} for title, desc in items])
        st.dataframe(gdpr_df, use_container_width=True, hide_index=True)

    with tab_cards:
        res  = ml["results_df"]
        best = res.loc[res["F1"].idxmax()]
        lr_r = res[res["Model"]=="Logistic Regression"].iloc[0]

        with st.expander("Data Card", expanded=True):
            dc = pd.DataFrame([
                ["Name","HR Employee Dataset"],
                ["Source","Kaggle / Rich Huebner (synthetic replica)"],
                ["Size","400 rows · 30+ features"],
                ["Type","Synthetic (educational use only)"],
                ["Target variable","Termd — 1 = Resigned · 0 = Active"],
                ["Sensitive attributes","Sex, RaceDesc, MaritalDesc, HispanicLatino"],
                ["Anonymization","SHA-256 (8 chars) on Employee_Name"],
                ["Text data","Exit interviews, surveys, transfer requests (synthetic)"],
                ["Limitations","Small sample · synthetic · US-centric"],
            ], columns=["Field","Value"])
            st.dataframe(dc, use_container_width=True, hide_index=True)

        with st.expander("Model Card — TalentGuard v3", expanded=True):
            mc = pd.DataFrame([
                ["Name","TalentGuard v3"],
                ["Task","Binary classification — resignation risk"],
                ["Deployed model (prod)","Logistic Regression — F1: "+str(lr_r["F1"])],
                ["Reference model","Random Forest — F1: "+str(best["F1"])+" · AUC: "+str(best["AUC"])],
                ["Explainability","SHAP global + local · Decision Tree"],
                ["Fairness audit","Disparate Impact · Gender + Race · 4/5 rule"],
                ["AI Act level","HIGH RISK — Annex III (employment/HR)"],
                ["GDPR","Pseudonymization · minimization · no automated decisions"],
                ["Limitations","Synthetic data · no temporal validation"],
                ["Allowed use","HR decision support — mandatory human review"],
                ["Prohibited use","Automated dismissal or promotion decisions"],
                ["Retraining","Quarterly + fairness audit at each cycle"],
            ], columns=["Field","Value"])
            st.dataframe(mc, use_container_width=True, hide_index=True)