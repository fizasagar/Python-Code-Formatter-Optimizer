import streamlit as st
import requests
import isort
import black
import tempfile
import subprocess
import ast
import re
import random
import plotly.express as px

from radon.complexity import cc_visit
from streamlit_lottie import st_lottie


# Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Load animation
animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")
if animation:
    st_lottie(animation, speed=1, height=200)

# Tabs
tabs = st.tabs([
    "📝 Code Input",
    "⚙️ Refactored Output",
    "🎯 Scorecard",
    "📊 Module Graph",
    "✨ Code Optimization Suggestions"
])


def refactor_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name
    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
    return formatted_code, result.stdout


def extract_imports(code):
    tree = ast.parse(code)
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    return imports


def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]
    fig = px.bar(x=list(import_counts.keys()), y=list(import_counts.values()),
                 labels={'x': 'Used Modules', 'y': 'Usage Counts'},
                 title="📊 Module Usage",
                 color=list(import_counts.keys()),
                 color_discrete_sequence=colors)
    fig.update_layout(bargap=0.3)
    st.plotly_chart(fig, use_container_width=True)


def optimize_code_suggestions(code):
    suggestions = []

    if "for i in range(len(list))" in code:
        suggestions.append("✅ Use 'for item in list' instead of 'for i in range(len(list))'.")
    if "== None" in code:
        suggestions.append("✅ Use 'is None' instead of '== None'.")
    if len(re.findall(r"print\(", code)) > 3:
        suggestions.append("⚠️ Too many print statements. Use logging or debugging tools.")
    if "for i in range(len(" in code:
        suggestions.append("✅ Use 'enumerate()' for cleaner loops.")
    if "list1 + list2" in code:
        suggestions.append("⚠️ Use 'list.extend()' or 'append()' instead of list concatenation in loops.")
    if "list.remove(" in code:
        suggestions.append("✅ Use 'set()' for removing duplicates.")
    if "global " in code:
        suggestions.append("⚠️ Avoid using 'global' variables.")
    if len(re.findall(r"\b[a-z]{1,2}\b", code)) > 5:
        suggestions.append("🧠 Use descriptive variable names.")
    if "open(" in code and "close()" in code:
        suggestions.append("✅ Use 'with open(...) as file:' instead of manual close.")
    if "if x == None:" in code:
        suggestions.append("✅ Use default arguments in functions instead of None checks.")
    if "lambda " in code and len(re.findall(r"lambda", code)) > 3:
        suggestions.append("⚠️ Too many lambdas. Use named functions for clarity.")
    if "list(map(" in code:
        suggestions.append("✅ Prefer list comprehensions over map().")

    return suggestions


# Tab 1 - Code Input
with tabs[0]:
    st.header("📝 Paste Your Python Code")
    user_code = st.text_area("Paste your Python code here:", height=300)

# Tab 2 - Refactored Code Output
with tabs[1]:
    if user_code:
        st.header("⚙️ Refactored Code")
        formatted_code, linter_output = refactor_code(user_code)
        st.code(formatted_code, language='python')
        st.subheader("🧪 Flake8 Report:")
        st.text(linter_output)

# Tab 3 - Complexity Scorecard
with tabs[2]:
    if user_code:
        st.header("🎯 Cyclomatic Complexity")
        blocks = cc_visit(user_code)
        for block in blocks:
            st.write(f"🔹 {block.name} — Complexity Score: {block.complexity}")

# Tab 4 - Module Graph
with tabs[3]:
    if user_code:
        st.header("📊 Imported Module Usage")
        imports = extract_imports(user_code)
        if imports:
            plot_import_usage(imports)
        else:
            st.info("No import statements found.")

# Tab 5 - Optimization Suggestions
with tabs[4]:
    if user_code:
        st.header("✨ Optimization Suggestions")
        suggestions = optimize_code_suggestions(user_code)
        if suggestions:
            for suggestion in suggestions:
                st.write("✅", suggestion)
        else:
            st.success("Your code looks clean and optimized! 🎉")

# Footer
st.markdown("""
    <hr>
    <div style='text-align: center;'>
        <strong>RefactorPro &copy; 2025</strong><br>
        Built with ❤️ by Mehak Alamgir<br><br>
        <a href="https://github.com/mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" height="30"></a>
        <a href="https://linkedin.com/in/mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" height="30"></a>
        <a href="https://youtube.com/@mehakalamgir"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" height="30"></a>
    </div>
""", unsafe_allow_html=True)
