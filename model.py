import warnings; warnings.filterwarnings("ignore")
import hashlib, time, random, re
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
import xgboost as xgb
import shap

SEED = 42
random.seed(SEED); np.random.seed(SEED)

C = {}

def set_theme(is_dark):
    global C
    if is_dark:
        C.update({
            "bg":           "#070b14",
            "card_bg":      "#0f172a",
            "card_border":  "#1e293b",
            "primary":      "#3b82f6",
            "success":      "#10b981",
            "danger":       "#f43f5e",
            "warning":      "#f59e0b",
            "text":         "#f8fafc",
            "text_muted":   "#94a3b8",
            "mint":         "#02c39a",
            "sb_bg":        "rgba(15, 23, 42, 0.6)",
            "sb_border":    "rgba(30, 41, 59, 0.8)",
            "card_rgba":    "rgba(15, 23, 42, 0.7)",
            "card_hover":   "rgba(59, 130, 246, 0.3)",
            "kpi_rgba":     "rgba(15, 23, 42, 0.85)",
            "header_g1":    "rgba(15, 23, 42, 0.9)",
            "header_g2":    "rgba(30, 58, 138, 0.4)",
            "hover_bg":     "rgba(30, 41, 59, 0.5)",
            "tab_act_bg":   "rgba(59, 130, 246, 0.15)",
            "badge_hi_bg1": "#7f1d1d", "badge_hi_bg2": "#450a0a", "badge_hi_txt": "#fecaca", "badge_hi_bd": "#dc2626",
            "badge_me_bg1": "#78350f", "badge_me_bg2": "#451a03", "badge_me_txt": "#fde68a", "badge_me_bd": "#d97706",
            "badge_lo_bg1": "#064e3b", "badge_lo_bg2": "#022c22", "badge_lo_txt": "#a7f3d0", "badge_lo_bd": "#059669",
            "prio_hi_bg":   "rgba(239, 68, 68, 0.15)", "prio_hi_txt": "#fca5a5", "prio_hi_bd": "rgba(239, 68, 68, 0.3)",
            "prio_me_bg":   "rgba(245, 158, 11, 0.15)", "prio_me_txt": "#fcd34d", "prio_me_bd": "rgba(245, 158, 11, 0.3)",
            "prio_in_bg":   "rgba(59, 130, 246, 0.15)", "prio_in_txt": "#93c5fd", "prio_in_bd": "rgba(59, 130, 246, 0.3)",
            "call_gn_bg":   "rgba(16, 185, 129, 0.1)", "call_gn_txt": "#a7f3d0", "call_gn_bd": "rgba(16, 185, 129, 0.1)",
            "call_bl_bg":   "rgba(59, 130, 246, 0.1)", "call_bl_txt": "#bfdbfe", "call_bl_bd": "rgba(59, 130, 246, 0.1)",
            "thm_bg":       "rgba(30, 58, 138, 0.5)", "thm_txt": "#93c5fd", "thm_bd": "rgba(59, 130, 246, 0.5)",
            "select_bg":    "rgba(15, 23, 42, 0.5)",
            "svg_fill":     "#3b82f6",
        })
    else:
        C.update({
            "bg":           "#f1f5f9",
            "card_bg":      "#ffffff",
            "card_border":  "#cbd5e1",
            "primary":      "#2563eb",
            "success":      "#059669",
            "danger":       "#e11d48",
            "warning":      "#d97706",
            "text":         "#0f172a",
            "text_muted":   "#475569",
            "mint":         "#059669",
            "sb_bg":        "rgba(255, 255, 255, 0.65)",
            "sb_border":    "rgba(203, 213, 225, 0.8)",
            "card_rgba":    "rgba(255, 255, 255, 0.8)",
            "card_hover":   "rgba(37, 99, 235, 0.3)",
            "kpi_rgba":     "rgba(255, 255, 255, 0.9)",
            "header_g1":    "rgba(255, 255, 255, 0.9)",
            "header_g2":    "rgba(219, 234, 254, 0.8)",
            "hover_bg":     "rgba(226, 232, 240, 0.5)",
            "tab_act_bg":   "rgba(59, 130, 246, 0.1)",
            "badge_hi_bg1": "#fee2e2", "badge_hi_bg2": "#fecaca", "badge_hi_txt": "#991b1b", "badge_hi_bd": "#f87171",
            "badge_me_bg1": "#fef3c7", "badge_me_bg2": "#fde68a", "badge_me_txt": "#92400e", "badge_me_bd": "#fbbf24",
            "badge_lo_bg1": "#d1fae5", "badge_lo_bg2": "#a7f3d0", "badge_lo_txt": "#065f46", "badge_lo_bd": "#34d399",
            "prio_hi_bg":   "rgba(225, 29, 72, 0.1)", "prio_hi_txt": "#e11d48", "prio_hi_bd": "rgba(225, 29, 72, 0.2)",
            "prio_me_bg":   "rgba(217, 119, 6, 0.1)", "prio_me_txt": "#d97706", "prio_me_bd": "rgba(217, 119, 6, 0.2)",
            "prio_in_bg":   "rgba(37, 99, 235, 0.1)", "prio_in_txt": "#2563eb", "prio_in_bd": "rgba(37, 99, 235, 0.2)",
            "call_gn_bg":   "rgba(5, 150, 105, 0.05)", "call_gn_txt": "#059669", "call_gn_bd": "rgba(5, 150, 105, 0.1)",
            "call_bl_bg":   "rgba(37, 99, 235, 0.05)", "call_bl_txt": "#2563eb", "call_bl_bd": "rgba(37, 99, 235, 0.1)",
            "thm_bg":       "rgba(219, 234, 254, 0.7)", "thm_txt": "#1d4ed8", "thm_bd": "rgba(37, 99, 235, 0.3)",
            "select_bg":    "rgba(255, 255, 255, 0.8)",
            "svg_fill":     "#2563eb",
        })

set_theme(True)

CO2_G = {"Logistic Regression":0.0001, "Decision Tree":0.0002,
          "Random Forest":0.018, "XGBoost":0.009}
SIZE_KB = {"Logistic Regression":12, "Decision Tree":45,
           "Random Forest":8200, "XGBoost":1100}

EXIT_POOL = [
    ("I've been stuck at $22/hr for three years while the market rate for my role is $28-32. When I brought data to my manager, I was told the budget was frozen. A week later they hired two new people at $30/hr.", "compensation"),
    ("The salary reviews are a joke. 2% merit increase when inflation is 5%. That's a pay cut with extra steps.", "compensation"),
    ("Good benefits, bad base pay. I can't pay rent with health insurance.", "compensation"),
    ("I negotiated hard at hire and got a fair offer. Three years later, new hires in the same role make more than me. No adjustment was offered.", "compensation"),
    ("The bonus structure changes every year. This year they moved the goalposts after Q3. Nobody hit their targets.", "compensation"),
    ("I exceeded every KPI for two consecutive years. My raise was 1.8%. My colleague who missed half his targets got 1.6%. What's the point?", "compensation"),
    ("After three years without a meaningful raise, I started looking. The market pays 30% more for my role.", "compensation"),
    ("I love my team. I love the mission. But I have a mortgage, and the salary hasn't moved in two years.", "compensation"),
    ("The pay structure is completely opaque. Nobody knows why two people doing the same job earn $8,000 apart.", "compensation"),
    ("Benefits are good, but take-home pay is well below what I can earn elsewhere. I have two kids in school.", "compensation"),
    ("I asked for a raise three times. Each time: budget constraints. I stopped asking and started interviewing.", "compensation"),
    ("Market surveys show my role pays $25k more elsewhere. After 4 years of service, I expected better.", "compensation"),
    ("Annual raises of 1-2% don't keep up with inflation. In real terms I was taking a pay cut every year.", "compensation"),
    ("I was doing the work of two people after my colleague left, with no additional compensation for six months.", "compensation"),
    ("I discovered a colleague with less experience in a nearly identical role earning $12k more. HR said salary bands are confidential.", "compensation"),
    ("My manager is a good technician but a terrible people manager. Zero emotional intelligence. Feedback is either silence or criticism in a group setting.", "management"),
    ("I had a great manager for 2 years. She left. Her replacement micromanages everything and takes credit for our work.", "management"),
    ("Three skip-level meetings in a row where I raised the same issue. Nothing changed. I learned my voice doesn't matter here.", "management"),
    ("The problem isn't my direct manager - he tries. It's the VP above him who blocks everything. Innovation dies at the director level.", "management"),
    ("I was put on a PIP after disagreeing with my manager in a meeting. It felt retaliatory. HR sided with management without investigation.", "management"),
    ("My manager took credit for my work twice in the last quarter. I raised it with HR and nothing changed.", "management"),
    ("I had three different managers in 18 months. No continuity, no relationship, no real support.", "management"),
    ("Leadership communicated a major strategy change via a company-wide email at 5pm on a Friday. No context, no Q&A.", "management"),
    ("Our director makes decisions affecting our team without consulting us once. Morale was at rock bottom by month three.", "management"),
    ("My manager never gives feedback - positive or negative. I had no idea where I stood until the annual review.", "management"),
    ("Favoritism was rampant. Projects and credit consistently went to the same two people regardless of merit.", "management"),
    ("My manager actively discouraged me from pursuing development opportunities, saying the team can't afford to lose me right now.", "management"),
    ("I raised an ethical concern about a project. My manager dismissed it in front of the group. I was quietly sidelined afterward.", "management"),
    ("The management layer between execs and employees is enormous. Good ideas never reach anyone with authority to act.", "management"),
    ("I asked what the promotion criteria are. My manager said it depends. Depends on what? Nobody knows.", "career_growth"),
    ("Applied for a senior role internally. Was told I lacked visibility. The person who got it has less experience but plays golf with the VP.", "career_growth"),
    ("No training budget, no conference budget, no certification support. But they expect us to stay cutting edge.", "career_growth"),
    ("I've been doing senior-level work for 18 months at a junior title and salary. When I asked for the promotion, I was told maybe next cycle.", "career_growth"),
    ("After 5 years I'm still in the same role with the same title. There's no ladder to climb here.", "career_growth"),
    ("My request for a transfer to a more strategic team was denied twice. I had to go elsewhere to grow.", "career_growth"),
    ("Every development conversation ended with we'll revisit this next quarter. Always the answer.", "career_growth"),
    ("The company's training program is 5 years out of date. I was studying technologies we'll never use in production.", "career_growth"),
    ("I came here to learn and challenge myself. After 2 years I feel like I haven't grown at all.", "career_growth"),
    ("Promised a senior role within a year. Two years later, still waiting. I stopped believing it.", "career_growth"),
    ("My project proposals were consistently shelved. I had ideas and energy but no platform to use them.", "career_growth"),
    ("I was repeatedly told I wasn't ready for promotion despite positive performance reviews. The criteria were never clear.", "career_growth"),
    ("I applied internally for two open roles and heard nothing back. Not even a rejection. Completely demoralizing.", "career_growth"),
    ("I was in the hospital and my manager texted asking about a deliverable. That's when I knew I needed to leave.", "work_life_balance"),
    ("Flexible hours means you can choose which 12 hours of the day you work.", "work_life_balance"),
    ("After the birth of my second child, I requested 4 days per week for 6 months. Denied. I resigned the next week.", "work_life_balance"),
    ("The workload is designed for 1.5 people but allocated to 1. When you raise it, they say prioritize. Everything is priority 1.", "work_life_balance"),
    ("I was answering Slack at 11pm on Saturday. When I stopped, my manager asked if everything was OK. That's the culture.", "work_life_balance"),
    ("I burned out completely in Q3. The company knows it's a systemic problem but calls it high performance culture.", "work_life_balance"),
    ("The office is 90 minutes from my home. Remote work was removed suddenly with no discussion. I cannot do that commute.", "work_life_balance"),
    ("We were asked to travel 3 weeks per month for 8 consecutive months. I missed too much of my life.", "work_life_balance"),
    ("Vacation requests were denied during the exact months my family can travel. In two years I used less than half my PTO.", "work_life_balance"),
    ("I missed my daughter's school play for a mandatory all-hands. It was a slide deck that could have been an email.", "work_life_balance"),
    ("Mental health support is non-existent. When I flagged burnout, I was told to take a long weekend.", "work_life_balance"),
    ("After burnout last year, I asked to go to 4 days per week. Request denied. So I went to 0 days per week.", "work_life_balance"),
    ("Diversity is a poster on the wall, not a practice. Look at the leadership team - it speaks for itself.", "culture"),
    ("The values say trust and autonomy. The reality is surveillance and control. We got a screen monitoring tool last month.", "culture"),
    ("I shipped a feature that reduced customer churn by 12%. My reward was a $25 Amazon gift card. I'm not joking.", "culture"),
    ("The company celebrates innovation but punishes failure. So nobody takes risks. We ship the same mediocre product every year.", "culture"),
    ("The constant restructuring made everyone anxious. Three reorgs in two years is too much.", "culture"),
    ("Communication from the top is poor. We found out about a major strategy shift from a LinkedIn post before our own managers told us.", "culture"),
    ("There's a strong culture of presenteeism. Being seen at your desk matters more than what you deliver.", "culture"),
    ("My contributions were regularly minimized in meetings. When I raised this, I was told to be more assertive.", "culture"),
    ("Recognition is hollow. Employee of the Month is meaningless when the rest of the year you're invisible.", "culture"),
    ("The exit interview is the most attention the company has paid me since onboarding.", "culture"),
    ("Cliques in senior leadership mean that if you're not in the right circle, your career stalls.", "culture"),
    ("Hired for data analysis, ended up doing manual reporting in Excel. I have a master's in ML. Complete waste.", "job_fit"),
    ("The role description was 70% strategic, 30% operational. Reality is the opposite. I'm a glorified admin.", "job_fit"),
    ("I love the company but hate my role. Asked for an internal transfer twice. Both times blocked by my manager.", "job_fit"),
    ("I was hired as a data analyst but ended up doing manual reporting 80% of the time. Not what I signed up for.", "job_fit"),
    ("The role evolved away from what I enjoy. I want to build things, not manage vendors.", "job_fit"),
    ("I'm overqualified for this position but there's nowhere to move internally.", "job_fit"),
    ("After my role was redefined post-merger, I no longer recognised the job description.", "job_fit"),
    ("I need more creative freedom. Every decision requires extensive sign-off. Nothing ships.", "job_fit"),
    ("I joined for a specific project. When it was cancelled, my role became undefined and nobody cared.", "job_fit"),
    ("Got a fully remote offer at 40% more. I like this company but I'm not a charity.", "external"),
    ("Relocating for family reasons. If remote work had been an option, I would have stayed.", "external"),
    ("Startup opportunity I couldn't pass up. This company moves too slow for where I am in my career.", "external"),
    ("My partner was relocated to another city. Long-distance wasn't feasible, so I resigned.", "external"),
    ("I'm returning to school full-time to complete my MBA. Plan to return to the workforce in 18 months.", "external"),
    ("A health issue required me to reduce my workload. The company couldn't accommodate any reduced-hours arrangement.", "external"),
    ("I've decided to launch my own consultancy. This role helped me realize that's what I want to do.", "external"),
    ("Received an offer I couldn't refuse - same role, 45% raise, full remote.", "external"),
    ("Two senior devs have been in a cold war for a year. Management knows but does nothing. The rest of us just survive.", "team_dynamics"),
    ("I'm the only woman on a 12-person team. The jokes got old fast. When I reported it, I was told to not take it personally.", "team_dynamics"),
    ("Great people, terrible process. We spend more time in standups talking about what we'll do than actually doing it.", "team_dynamics"),
    ("I was the only junior in a team of seniors who had no patience for questions. I felt stupid every day.", "team_dynamics"),
    ("After several team members left, the knowledge and culture that made this place great left with them.", "team_dynamics"),
    ("A persistent conflict with one colleague made the environment very uncomfortable. HR mediation didn't resolve it.", "team_dynamics"),
    ("Collaboration is given lip service but in practice everyone protects their silo.", "team_dynamics"),
    ("I came here from a start-up environment and the pace difference was jarring. I never adapted.", "team_dynamics"),
]

SURVEY_POOL = [
    ("8/10 - My manager is exceptional. The team is cohesive and projects are stimulating. The only downside: visibility on promotions lacks clarity.", "positive"),
    ("7/10 - Good work-life balance since the remote policy. Office days could be better organized.", "positive"),
    ("9/10 - Best team I've ever worked with. The projects are interesting and I feel like I'm growing.", "positive"),
    ("8/10 - Flexibility is excellent. Salary could be more competitive but the atmosphere more than compensates.", "positive"),
    ("7/10 - Decent company. Nothing exceptional, but stable and respectful. Content for now.", "positive"),
    ("9/10 - My manager fights for his team. That's rare and I truly appreciate it.", "positive"),
    ("8/10 - Strong parental leave policy made a stressful period much more manageable.", "positive"),
    ("7/10 - Projects are varied and challenging. The culture of continuous improvement is real.", "positive"),
    ("8/10 - Good equity plan, clear salary bands. I know where I stand.", "positive"),
    ("7/10 - I've been promoted twice in three years. Progression is possible if you put in the effort.", "positive"),
    ("8/10 - The mentorship program has genuinely accelerated my career. I feel invested in.", "positive"),
    ("9/10 - Leadership is transparent and communicates well. I feel like I'm part of something.", "positive"),
    ("7/10 - Good benefits package, especially health coverage. Team culture is solid.", "positive"),
    ("8/10 - I recommended this company to three friends. The culture is genuinely good.", "positive"),
    ("7/10 - Good work-life balance. Colleagues are competent and supportive.", "positive"),
    ("8/10 - Flexible hours policy is real, not just on paper. Trust goes a long way.", "positive"),
    ("7/10 - Projects are challenging in a good way. I learn something new every week.", "positive"),
    ("8/10 - The training program is serious. The company genuinely invests in its employees.", "positive"),
    ("6/10 - Tools are outdated. I spend more time working around bugs than actually working.", "mixed"),
    ("5/10 - Average. Not terrible, not great. But average isn't what gets me out of bed anymore.", "mixed"),
    ("6/10 - Good team, disorganized middle management.", "mixed"),
    ("5/10 - The mission is meaningful. Execution is sometimes frustrating.", "mixed"),
    ("6/10 - Happy here for now, watching to see if the promised changes actually happen.", "mixed"),
    ("5/10 - Nice culture overall, a bit too many meetings for my taste.", "mixed"),
    ("6/10 - Learning a lot but could use more support from senior leadership.", "mixed"),
    ("5/10 - Decent salary, limited growth. Fine for now, not forever.", "mixed"),
    ("6/10 - The product is exciting but internal processes are slow and bureaucratic.", "mixed"),
    ("5/10 - Some great colleagues, some real frustrations. Undecided.", "mixed"),
    ("4/10 - Too many meetings, not enough action. I lose 3 hours a day in pointless calls.", "negative"),
    ("3/10 - The reorg destroyed our team. New manager has no idea what we do.", "negative"),
    ("2/10 - I feel invisible. No feedback, no recognition, no path forward. Just a number.", "negative"),
    ("4/10 - Management communicates nothing. We learn about important decisions through rumor.", "negative"),
    ("3/10 - I'm underpaid for what I do. I've raised it twice with no result.", "negative"),
    ("2/10 - My manager is difficult to work with and HR has not helped.", "negative"),
    ("4/10 - I feel invisible in this organisation. My work goes unrecognized.", "negative"),
    ("3/10 - I dread Monday mornings. That's not how work should feel.", "negative"),
    ("2/10 - Burning out and the organisation hasn't noticed or offered support.", "negative"),
    ("4/10 - Team dynamics are poor. There's open conflict that management ignores.", "negative"),
    ("3/10 - Told there would be advancement opportunities. Haven't seen any evidence.", "negative"),
    ("2/10 - The culture of presenteeism is exhausting. Presence is valued, not results.", "negative"),
    ("3/10 - Three managers in 18 months. I've stopped investing in the relationship.", "negative"),
    ("4/10 - The project was cancelled without explanation. My role is now unclear.", "negative"),
    ("3/10 - I've been doing the same job for 3 years. No challenge, no growth, no reason to stay.", "negative"),
]

TRANSFER_POOL = [
    "I would like to join the Data Engineering team. My current position in IT Support does not make use of my Python and SQL skills.",
    "Transfer request from Production to Quality. After 3 years in Production, I have developed expertise in quality control.",
    "Following my project management certification, I would like to move into a coordination role within the PMO.",
    "I am requesting a transfer to the Sales team. My regular client interactions have convinced me that is where I can have the most impact.",
    "Internal mobility request to the Digital Marketing department. My data analysis skills would be directly applicable.",
    "I would like to join the Innovation Lab team. The cross-functional projects I have led have made me want to work on more forward-looking topics.",
    "Transfer request to the Paris office. My family situation has changed and the commute from Lyon is no longer sustainable.",
    "I am applying for the internal opening in Software Engineering. I have completed 3 internal training modules.",
    "I would like to move into an HR role. My 4 years of experience working with teams gives me a strong ground-level perspective.",
    "Internal mobility request to the IT Security team. I obtained my CISSP certification outside of working hours.",
    "I would like to join the Product team. My development experience has given me a clear understanding of user needs.",
    "Transfer request to a night-shift team for personal reasons.",
    "I am applying for the Team Lead position in my department. Five years of experience and an informal technical lead role justify this application.",
    "International rotation request to the Singapore office. I speak Mandarin fluently.",
    "I would like to join the ESG team. Sustainability is central to my personal and professional commitments.",
    "Transfer request to the Financial Analysis team. I have completed my accounting degree.",
    "I am requesting reassignment to a different manager within the same department.",
    "Request for part-time transition with transfer to a less operational role. My health situation has changed.",
    "I would like to join the Training team. Feedback from my work as an internal mentor has convinced me this is my calling.",
    "Internal mobility request to the Client Relations department. My communication skills are underutilized in my current role.",
]

FEAT_EN = {
    "Salary":"Salary", "EngagementSurvey":"Engagement", "EmpSatisfaction":"Satisfaction",
    "PerformanceScore":"Performance", "Absences":"Absences", "Tenure_Years":"Tenure",
    "Age":"Age", "Department":"Department", "ManagerName":"Manager", "ManagerID":"Manager",
    "RecruitmentSource":"Recruitment Source", "Position":"Position", "PositionID":"Position",
    "DaysLateLast30":"Recent Late Days", "SpecialProjectsCount":"Special Projects",
    "SentimentScore":"Qualitative Feedback", "MaritalDesc":"Marital Status",
    "Sex":"Gender", "RaceDesc":"Race", "HispanicLatino":"Hispanic/Latino",
    "CitizenDesc":"Citizenship Status", "PerfScoreID":"Performance Score",
    "FromDiversityJobFairID":"Diversity Fair Recruit",
}

REASON_MAP = {
    "Salary":           ("Salary below average",          "Review compensation"),
    "EngagementSurvey": ("Declining engagement",          "Urgent 1-on-1 meeting"),
    "EmpSatisfaction":  ("Low satisfaction",              "Urgent 1-on-1 meeting"),
    "PerformanceScore": ("Performance concerns",          "Managerial support"),
    "PerfScoreID":      ("Performance concerns",          "Managerial support"),
    "Absences":         ("High absenteeism",              "Follow-up meeting"),
    "Tenure_Years":     ("Tenure without progression",    "Career development plan"),
    "Department":       ("High-risk department",          "Team climate audit"),
    "SentimentScore":   ("Concerning feedback",           "Confidential HR meeting"),
    "DaysLateLast30":   ("Declining punctuality",         "Follow-up meeting"),
    "Age":              ("At-risk demographic profile",   "Individual assessment"),
    "ManagerID":        ("Managerial tension detected",   "HR mediation"),
    "ManagerName":      ("Managerial tension detected",   "HR mediation"),
}


def feat_fr(name):
    return FEAT_EN.get(name, name.replace("_"," ").title())


def get_top_shap(sv_row, feat_names, n=5, only_positive=True):
    pairs = list(zip(sv_row, feat_names))
    if only_positive:
        pairs = [(v,f) for v,f in pairs if v > 0]
    return sorted(pairs, key=lambda x: abs(x[0]), reverse=True)[:n]


def get_risk_summary(sv_row, feat_names):
    top = get_top_shap(sv_row, feat_names, n=1)
    if not top:
        top = sorted(zip(sv_row, feat_names), key=lambda x: abs(x[0]), reverse=True)[:1]
    feat = top[0][1] if top else feat_names[0]
    raison, action = REASON_MAP.get(feat, (feat_fr(feat), "Individual assessment"))
    return raison, action


def generate_explanation_fr(emp_row, sv_row, feat_names, df_full):
    top3 = get_top_shap(sv_row, feat_names, n=3)
    if not top3:
        return "Combination of several moderate factors contributing to the risk."
    parts = []
    for shap_val, feat in top3:
        val = emp_row.get(feat, "N/A")
        if feat == "Salary":
            dept = emp_row.get("Department","")
            dept_avg = df_full[df_full["Department"]==dept]["Salary"].mean()
            diff_pct = (val - dept_avg)/dept_avg*100 if dept_avg else 0
            if diff_pct < -5:
                parts.append(f"salary (${val:,.0f}) is {abs(diff_pct):.0f}% "
                              f"below the {dept} department average (${dept_avg:,.0f})")
            else:
                parts.append(f"salary (${val:,.0f}) is a risk factor")
        elif feat in ("EngagementSurvey","EmpSatisfaction"):
            label = "engagement" if feat=="EngagementSurvey" else "satisfaction"
            parts.append(f"{label} score is low ({val:.1f}/5)")
        elif feat in ("PerformanceScore","PerfScoreID"):
            parts.append(f"performance level is a concern ({emp_row.get('PerformanceScore','N/A')})")
        elif feat == "Tenure_Years":
            parts.append(f"no visible progression after {val:.1f} year(s) of tenure")
        elif feat == "Absences":
            parts.append(f"absenteeism rate is high ({int(val)} days)")
        elif feat == "SentimentScore":
            if val < 0:
                parts.append("recent qualitative feedback is negative")
            else:
                parts.append("profile shows several cumulative weak signals")
        elif feat == "Department":
            parts.append("department has a structurally high turnover rate")
        else:
            parts.append(f"{feat_fr(feat)} is a risk factor")

    if len(parts) == 1:
        return f"This employee is at risk because {parts[0]}."
    joined = ", ".join(parts[:-1])
    return f"This employee is primarily at risk because {joined}, and {parts[-1]}."


def generate_actions_fr(sv_row, feat_names, emp_row, text_df):
    top5 = get_top_shap(sv_row, feat_names, n=5)
    feats_top = [f for _,f in top5]
    actions = []
    has_transfer = len(text_df[(text_df["EmpIndex"]==emp_row.name)&(text_df["Type"]=="transfer")]) > 0
    neg_survey   = text_df[(text_df["EmpIndex"]==emp_row.name)&
                            (text_df["Type"]=="survey")&(text_df["Theme"]=="survey_neg")]

    if "Salary" in feats_top:
        actions.append(("$","Review compensation - benchmark vs. market and department average","HIGH","30 days"))
    if any(f in feats_top for f in ("EngagementSurvey","EmpSatisfaction")):
        actions.append(("1:1","Schedule a 1-on-1 meeting to identify engagement levers","HIGH","2 weeks"))
    if "Tenure_Years" in feats_top:
        actions.append(("DEV","Build a career development plan with concrete objectives","HIGH","1 month"))
    if any(f in feats_top for f in ("PerformanceScore","PerfScoreID")):
        actions.append(("MGT","Initiate managerial support - clarify expectations and resources","MEDIUM","1 month"))
    if "Department" in feats_top:
        actions.append(("AUDIT","Launch a team climate audit in the department","MEDIUM","2 months"))
    if any(f in feats_top for f in ("Absences","DaysLateLast30")):
        actions.append(("FU","Conduct a follow-up meeting on well-being and working conditions","MEDIUM","2 weeks"))
    if len(neg_survey) > 0:
        actions.append(("HR","Confidential HR meeting - recent concerning feedback to address","HIGH","1 week"))
    if has_transfer:
        actions.append(("MOB","Review the internal mobility request submitted by this employee","HIGH","2 weeks"))
    if "SentimentScore" in feats_top:
        actions.append(("FB","In-depth analysis of recent qualitative feedback","MEDIUM","1 month"))
    if not actions:
        actions.append(("FU","Personalized monitoring - schedule regular check-ins with manager","MEDIUM","1 month"))
    actions.append(("RET","Include in targeted retention program if risk > 70%","INFO","Ongoing"))
    return actions[:5]


def simple_sentiment(txt):
    pos = ["good","great","excellent","happy","love","best","enjoy","positive",
           "growth","support","flexible","appreciate","proud","trust"]
    neg = ["bad","terrible","awful","hate","worst","leave","quit","resign",
           "underpaid","ignored","invisible","burnout","frustrated","blocked",
           "micromanage","micromanaging","micromanages","micromanager",
           "denied","never","nothing","toxic","dread"]
    t = txt.lower()
    words = set(re.findall(r'[a-z]+', t))
    score = (sum(1 for w in pos if w in words)
             - sum(1 for w in neg if w in words))
    return round(score / max(len(txt.split())/10, 1), 2)


def risk_emoji(p):
    if p >= 0.70:
        return "HIGH"
    elif p >= 0.40:
        return "MEDIUM"
    return "LOW"


def risk_badge_html(p):
    if p >= 0.70:
        return f'<span class="badge badge-high">{p:.0%}</span>'
    elif p >= 0.40:
        return f'<span class="badge badge-medium">{p:.0%}</span>'
    return f'<span class="badge badge-low">{p:.0%}</span>'


def styled_chart(fig, height=None):
    upd = dict(
        font=dict(family="Inter, sans-serif", color=C["text"], size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(gridcolor=C["card_border"], zerolinecolor=C["card_border"], showline=False, tickfont=dict(color=C["text_muted"])),
        yaxis=dict(gridcolor=C["card_border"], zerolinecolor=C["card_border"], showline=False, tickfont=dict(color=C["text_muted"])),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["text_muted"])),
        hoverlabel=dict(bgcolor=C["card_bg"], font_size=13, font_family="Inter", bordercolor=C["card_border"])
    )
    if height:
        upd["height"] = height
    fig.update_layout(**upd)
    return fig


@st.cache_data(show_spinner="Loading data...")
def load_data():
    df = pd.read_csv("data/raw/HRDataset_v14.csv")
    df["Employee_Name"] = df["Employee_Name"].apply(
        lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:8].upper()
    )
    ref = pd.Timestamp("2018-12-31")
    df["_hire_dt"]     = pd.to_datetime(df["DateofHire"], format="%m/%d/%Y", errors="coerce")
    df["_dob_dt"]      = pd.to_datetime(df["DOB"],        format="%m/%d/%Y", errors="coerce")
    df["Tenure_Years"] = ((ref - df["_hire_dt"]).dt.days / 365.25).clip(0)
    df["Age"]          = ((ref - df["_dob_dt"]).dt.days  / 365.25).clip(18, 70)

    rng     = np.random.default_rng(SEED)
    leavers = df[df["Termd"]==1].index.tolist()
    stayers = df[df["Termd"]==0].index.tolist()

    texts = []
    for idx in leavers:
        txt, theme = EXIT_POOL[int(rng.integers(0, len(EXIT_POOL)))]
        texts.append({"EmpIndex": idx, "Type": "exit", "Text": txt, "Theme": theme, "Termd": 1})
        neg_pool = [s for s, t in SURVEY_POOL if t=="negative"]
        texts.append({"EmpIndex": idx, "Type": "survey",
                       "Text": neg_pool[int(rng.integers(0, len(neg_pool)))],
                       "Theme": "survey_neg", "Termd": 1})
    for idx in rng.choice(stayers, size=int(0.75*len(stayers)), replace=False):
        pos_mix = [s for s, t in SURVEY_POOL if t in ("positive","mixed")]
        texts.append({"EmpIndex": int(idx), "Type": "survey",
                       "Text": pos_mix[int(rng.integers(0, len(pos_mix)))],
                       "Theme": "survey_pos", "Termd": 0})
    for idx in rng.choice(df.index.tolist(), size=int(0.15*len(df)), replace=False):
        texts.append({"EmpIndex": int(idx), "Type": "transfer",
                       "Text": TRANSFER_POOL[int(rng.integers(0, len(TRANSFER_POOL)))],
                       "Theme": "transfer", "Termd": int(df.loc[int(idx),"Termd"])})

    text_df = pd.DataFrame(texts)

    sent_map = {}
    for _, row in text_df.iterrows():
        s = simple_sentiment(row["Text"])
        sent_map.setdefault(row["EmpIndex"], []).append(s)
    df["SentimentScore"] = df.index.map(lambda i: np.mean(sent_map.get(i, [0.0])))

    return df, text_df


@st.cache_resource(show_spinner="Training models...")
def train_models(_df):
    df = _df.copy()
    LEAKAGE = ["DateofTermination","TermReason","EmploymentStatus","EmpStatusID"]
    SENSITIVE = ["Sex","RaceDesc","HispanicLatino","MaritalDesc","CitizenDesc",
                 "GenderID","MarriedID","MaritalStatusID"]
    DROP    = ["EmpID","Zip","State","Employee_Name","DateofHire","DOB",
               "_hire_dt","_dob_dt","LastPerformanceReview_Date",
               "SentimentScore"]
    df_fe = df.drop(columns=[c for c in LEAKAGE+DROP+SENSITIVE if c in df.columns], errors="ignore")

    encoders = {}
    for col in df_fe.select_dtypes(include="object").columns:
        le = LabelEncoder()
        df_fe[col] = le.fit_transform(df_fe[col].astype(str))
        encoders[col] = le
    df_fe.fillna(df_fe.median(numeric_only=True), inplace=True)

    X = df_fe.drop(columns=["Termd"])
    y = df_fe["Termd"]
    feat_names = X.columns.tolist()

    X.fillna(0, inplace=True)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
    scaler   = StandardScaler()
    X_tr_sc  = np.nan_to_num(scaler.fit_transform(X_tr), nan=0.0)
    X_te_sc  = np.nan_to_num(scaler.transform(X_te), nan=0.0)

    MODEL_DEFS = {
        "Logistic Regression": LogisticRegression(max_iter=1000, C=0.5, random_state=SEED),
        "Decision Tree":       DecisionTreeClassifier(max_depth=6, min_samples_leaf=3, random_state=SEED),
        "Random Forest":       RandomForestClassifier(n_estimators=300, max_depth=None,
                                                      min_samples_leaf=2,
                                                      random_state=SEED, n_jobs=-1),
        "XGBoost":             xgb.XGBClassifier(n_estimators=300, max_depth=6,
                                                  learning_rate=0.05, subsample=0.8,
                                                  colsample_bytree=0.8,
                                                  random_state=SEED,
                                                  eval_metric="logloss", verbosity=0),
    }

    results, trained = [], {}
    for name, model in MODEL_DEFS.items():
        Xtr = X_tr_sc if name=="Logistic Regression" else X_tr.values
        Xte = X_te_sc if name=="Logistic Regression" else X_te.values
        cv     = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
        cv_res = cross_validate(model, Xtr, y_tr, cv=cv, scoring=["f1","roc_auc"])
        t0     = time.perf_counter()
        model.fit(Xtr, y_tr)
        elapsed = time.perf_counter() - t0
        y_pred  = model.predict(Xte)
        y_prob  = model.predict_proba(Xte)[:,1]
        trained[name] = model
        results.append({
            "Model":        name,
            "Accuracy":     round(accuracy_score(y_te, y_pred), 3),
            "F1":           round(f1_score(y_te, y_pred, zero_division=0), 3),
            "AUC":          round(roc_auc_score(y_te, y_prob), 3),
            "CV F1":        f"{cv_res['test_f1'].mean():.3f} +/- {cv_res['test_f1'].std():.3f}",
            "Time (ms)":    round(elapsed*1000, 1),
            "CO2 (g)":      CO2_G[name],
            "Size (KB)":    SIZE_KB[name],
        })

    results_df = pd.DataFrame(results)

    rf      = trained["Random Forest"]
    explainer = shap.TreeExplainer(rf)
    sv_all  = explainer.shap_values(X)
    if isinstance(sv_all, list):
        sv = sv_all[1]
    elif sv_all.ndim == 3:
        sv = sv_all[:,:,1]
    else:
        sv = sv_all

    # Out-of-fold predictions to avoid overfit risk scores on training data
    probs_all = np.zeros(len(X))
    oof_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    for train_idx, val_idx in oof_cv.split(X, y):
        rf_fold = RandomForestClassifier(n_estimators=300, max_depth=None,
                                         min_samples_leaf=2,
                                         random_state=SEED, n_jobs=-1)
        rf_fold.fit(X.values[train_idx], y.values[train_idx])
        probs_all[val_idx] = rf_fold.predict_proba(X.values[val_idx])[:, 1]

    return {
        "trained":    trained,
        "results_df": results_df,
        "X": X, "y": y,
        "X_tr": X_tr, "X_te": X_te,
        "y_tr": y_tr, "y_te": y_te,
        "X_tr_sc": X_tr_sc, "X_te_sc": X_te_sc,
        "scaler":     scaler,
        "feat_names": feat_names,
        "sv":         sv,
        "probs_all":  probs_all,
        "explainer":  explainer,
        "encoders":   encoders,
    }


@st.cache_resource(show_spinner="Preparing data...")
def load_all():
    df, text_df = load_data()
    ml = train_models(df)

    sv         = ml["sv"]
    feat_names = ml["feat_names"]
    probs_all  = ml["probs_all"]
    mean_abs_sv = np.abs(sv).mean(axis=0)

    emp = df.copy()
    emp["RiskScore"]  = probs_all
    emp["RiskLevel"]  = emp["RiskScore"].apply(lambda p: "High" if p>=0.70 else "Medium" if p>=0.40 else "Low")
    emp["RiskEmoji"]  = emp["RiskScore"].apply(risk_emoji)
    emp["TopFeat"]    = [feat_names[np.argmax(np.abs(sv[i]))] for i in range(len(sv))]
    emp["RaisonCourte"], emp["ActionCourte"] = zip(*[
        get_risk_summary(sv[i], feat_names) for i in range(len(sv))
    ])

    return {
        "df":          df,
        "text_df":     text_df,
        "emp":         emp,
        "sv":          sv,
        "feat_names":  feat_names,
        "probs_all":   probs_all,
        "mean_abs_sv": mean_abs_sv,
        "ml":          ml,
    }
