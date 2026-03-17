import sys

with open("app.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if "Talent Retention</div>" in line:
        new_lines.append("    </div>\", unsafe_allow_html=True)\n\n")
        new_lines.append("    colA, colB = st.columns([3, 1])\n")
        new_lines.append("    with colB:\n")
        new_lines.append("        st.button(\"☀️\" if st.session_state.is_dark else \"🌙\", on_click=toggle_theme)\n\n")

with open("app.py", "w") as f:
    f.writelines(new_lines)

