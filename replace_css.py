import re

with open("app.py", "r") as f:
    content = f.read()

# Make sure we import set_theme
content = content.replace('from model import load_all, C, styled_chart, risk_emoji', 'from model import load_all, C, set_theme, styled_chart, risk_emoji')

# Add session state and set_theme call before CSS
session_logic = """
if "is_dark" not in st.session_state:
    st.session_state.is_dark = True

def toggle_theme():
    st.session_state.is_dark = not st.session_state.is_dark

set_theme(st.session_state.is_dark)

st.markdown(f\"\"\"
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: visible !important;}
[data-testid="stAppViewContainer"] { background-color: {C['bg']}; transition: background-color 0.3s ease; }
[data-testid="stHeader"] { background-color: transparent; }
html, body, [class*="css"] { 
    font-family: 'Inter', system-ui, sans-serif !important; 
    color: {C['text']} !important;
}
.card {
    background: {C['card_rgba']};
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid {C['card_border']};
    border-radius: 12px;
    padding: 24px;
    margin: 12px 0;
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    border-color: {C['card_hover']};
}
.card h3 { color: {C['text']}; margin: 0 0 10px 0; font-weight: 600; }
.card p  { color: {C['text_muted']}; margin: 0; }

.kpi {
    background: {C['kpi_rgba']};
    backdrop-filter: blur(10px);
    border: 1px solid {C['card_border']};
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    border-top: 4px solid {C['primary']};
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.kpi:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.4);
}
.kpi-danger  { border-top-color: {C['danger']}; }
.kpi-warning { border-top-color: {C['warning']}; }
.kpi-success { border-top-color: {C['success']}; }
.kpi h2  { margin:0; font-size:2.8rem; font-weight:700; color:{C['text']}; line-height:1.1; letter-spacing:-0.5px; }
.kpi p   { margin:8px 0 0 0; font-size:.9rem; color:{C['text_muted']}; font-weight:500; }
.kpi small { font-size:.8rem; color:#64748b; margin-top: 4px; display: block; }

.section-title {
    font-size:1.2rem; font-weight:600; color:{C['text']};
    border-left:4px solid {C['primary']}; padding-left:12px;
    margin: 32px 0 16px 0;
    letter-spacing: -0.3px;
}

.profile-header {
    background: linear-gradient(135deg, {C['header_g1']} 0%, {C['header_g2']} 100%);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 16px;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.3);
    color: {C['text']};
    padding: 28px 32px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 16px;
    margin-bottom: 24px;
    transition: all 0.3s ease;
}
.profile-header:hover {
    border-color: rgba(59, 130, 246, 0.4);
}

.badge {
    display:inline-block; padding:6px 16px; border-radius:24px;
    font-weight:600; font-size:.95rem; letter-spacing: 0.5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.badge-high   { background: linear-gradient(135deg, {C['badge_hi_bg1']} 0%, {C['badge_hi_bg2']} 100%); color:{C['badge_hi_txt']}; border:1px solid {C['badge_hi_bd']}; }
.badge-medium { background: linear-gradient(135deg, {C['badge_me_bg1']} 0%, {C['badge_me_bg2']} 100%); color:{C['badge_me_txt']}; border:1px solid {C['badge_me_bd']}; }
.badge-low    { background: linear-gradient(135deg, {C['badge_lo_bg1']} 0%, {C['badge_lo_bg2']} 100%); color:{C['badge_lo_txt']}; border:1px solid {C['badge_lo_bd']}; }

.action-row {
    display:flex; align-items:flex-start; gap:16px;
    padding:16px 12px; border-bottom:1px solid {C['card_border']};
    transition: background 0.2s ease;
    border-radius: 8px;
}
.action-row:hover {
    background: {C['hover_bg']};
}
.action-icon { font-size:1.1rem; font-weight:700; min-width:48px; color:{C['text_muted']}; padding-top:2px; }

.priority-haute   { background:{C['prio_hi_bg']}; color:{C['prio_hi_txt']}; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:600; border: 1px solid {C['prio_hi_bd']}; }
.priority-moyenne { background:{C['prio_me_bg']}; color:{C['prio_me_txt']}; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:600; border: 1px solid {C['prio_me_bd']}; }
.priority-info    { background:{C['prio_in_bg']}; color:{C['prio_in_txt']}; padding:3px 10px; border-radius:12px; font-size:.75rem; font-weight:600; border: 1px solid {C['prio_in_bd']}; }

.callout-green {
    background: {C['call_gn_bg']}; border-left:4px solid {C['success']};
    padding:16px 20px; border-radius:0 12px 12px 0;
    color:{C['call_gn_txt']}; font-weight:500; margin:16px 0;
    border-top: 1px solid {C['call_gn_bd']};
    border-right: 1px solid {C['call_gn_bd']};
    border-bottom: 1px solid {C['call_gn_bd']};
}
.callout-blue {
    background: {C['call_bl_bg']}; border-left:4px solid {C['primary']};
    padding:16px 20px; border-radius:0 12px 12px 0;
    color:{C['call_bl_txt']}; font-weight:500; margin:16px 0;
    border-top: 1px solid {C['call_bl_bd']};
    border-right: 1px solid {C['call_bl_bd']};
    border-bottom: 1px solid {C['call_bl_bd']};
}

.theme-badge {
    display:inline-block; background:{C['thm_bg']}; color:{C['thm_txt']};
    border:1px solid {C['thm_bd']}; border-radius:24px;
    padding:4px 14px; font-size:.8rem; font-weight:600;
    margin: 0 4px; vertical-align: middle;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: {C['sb_bg']} !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid {C['sb_border']} !important;
}

/* Radio buttons to navigation tabs */
div.row-widget.stRadio > div[role="radiogroup"] {
    gap: 0px;
}
div.row-widget.stRadio > div[role="radiogroup"] > label {
    background: transparent;
    padding: 12px 16px;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}
div.row-widget.stRadio > div[role="radiogroup"] > label:hover {
    background: {C['hover_bg']};
    transform: translateX(2px);
}
/* Hide the actual radio circle */
div.row-widget.stRadio > div[role="radiogroup"] > label > div:first-child {
    display: none;
}
/* Style the text */
div.row-widget.stRadio > div[role="radiogroup"] > label > div:last-child {
    font-weight: 500;
    font-size: 1rem;
    color: {C['text_muted']};
    margin-left: 0 !important;
}
/* Active state */
div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
    background: {C['tab_act_bg']} !important;
    border-color: {C['thm_bd']} !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) > div:last-child {
    color: {C['primary']} !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] > div {
    background-color: {C['select_bg']};
    border-color: {C['sb_border']};
}

div[data-testid="stMetricValue"] { color: {C['text']} !important; }
div[data-testid="stMarkdownContainer"] p { color: {C['text']} !important; }

</style>
\"\"\", unsafe_allow_html=True)
"""

content = re.sub(r'st\.markdown\("""\n<style>.*?</style>\n""", unsafe_allow_html=True)', session_logic, content, flags=re.DOTALL)

with open("app.py", "w") as f:
    f.write(content)
