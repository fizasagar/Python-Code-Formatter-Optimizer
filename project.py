import streamlit as st
import ast, random, tempfile, subprocess, re, requests, isort, black
import plotly.express as px
from radon.complexity import cc_visit

# ----- Sidebar -----
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/code.png", width=70)
    st.markdown("### 🚀 Features")
    st.info("Refactor, analyze, optimize your code.")

    st.markdown("### 📘 Documentation")
    st.success("Get started with AI-driven optimization.")

    if st.button("🗑️ Clear Code"):
        st.session_state['code_input'] = ""

# ----- Title -----
st.markdown("<h1 style='text-align: center;'>AI-Powered Python Code<br>Formatter & Optimizer 🚀</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Empower your Python code with AI-driven formatting, optimization,<br>and analysis</p>", unsafe_allow_html=True)

# ----- Tabs -----
tabs = st.tabs(["📝 Code Input", "⚙️ Refactored Output", "🎯 Scorecard", "📊 Module Graph", "✨ Code Optimization Suggestions"])

# ----- Code Input -----
with tabs[0]:
    code_input = st.text_area("Paste your Python code here:", height=250, key="code_input")

# ----- Refactor Code -----
def refactor_code(code):
    sorted_code = isort.code(code)
    formatted_code = black.format_file_contents(sorted_code, fast=False, mode=black.Mode())
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp_file:
        tmp_file.write(formatted_code)
        tmp_path = tmp_file.name
    result = subprocess.run(["flake8", tmp_path], capture_output=True, text=True)
    return formatted_code, result.stdout

# ----- Extract Imports -----
def extract_imports(code):
    try:
        tree = ast.parse(code)
        return [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    except:
        return []

# ----- Optimize Suggestions -----
def optimize_code_suggestions(code):
    suggestions = []
    if "for i in range(len(list))" in code:
        suggestions.append("Use `for item in list` instead of `for i in range(len(list))`.")
    if "== None" in code:
        suggestions.append("Use `is None` instead of `== None`.")
    if len(re.findall(r"print\(", code)) > 3:
        suggestions.append("Too many `print` statements. Consider logging.")
    if "enumerate(" not in code and "for i in range(len(" in code:
        suggestions.append("Try using `enumerate()` for cleaner loops.")
    if "open(" in code and "close()" in code:
        suggestions.append("Use `with open(...) as f:` instead of manually closing files.")
    return suggestions

# ----- Show Refactored Code -----
if code_input.strip():
    formatted_code, flake8_output = refactor_code(code_input)
    with tabs[1]:
        st.subheader("⚙️ Refactored Code:")
        st.code(formatted_code, language="python")

    with tabs[2]:
        st.subheader("🎯 Code Scorecard (Flake8):")
        st.text(flake8_output or "✅ No linting issues found!")

    with tabs[3]:
        st.subheader("📊 Module Usage")
        imports = extract_imports(code_input)
        if imports:
            import_counts = {i: imports.count(i) for i in set(imports)}
            fig = px.bar(x=list(import_counts.keys()), y=list(import_counts.values()),
                         labels={'x': 'Used Modules', 'y': 'Usage Count'},
                         color=list(import_counts.keys()))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No imports found in your code.")

    with tabs[4]:
        st.subheader("✨ Optimization Suggestions")
        for suggestion in optimize_code_suggestions(code_input):
            st.markdown(f"✅ {suggestion}")

# ----- Footer -----
st.markdown("""
    <hr><center>
    RefactorPro © 2025 — Built with ❤️ by Fiza Asif <br>
    <a href="https://github.com/fizasagar"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="24"/></a>
    <a href="https://www.linkedin.com/in/fiza-sagar-bb3b652b9/"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="24"/></a>
    <a href="https://www.facebook.com/fiza.sagar.7/"><img src="https://cdn-icons-png.flaticon.com/512/124/124010.png" width="24"/></a>

    </center>
""", unsafe_allow_html=True)
