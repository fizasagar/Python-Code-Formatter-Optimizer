from radon.complexity import cc_visit  
from streamlit_lottie import st_lottie 


# Function to load animation from a URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_lock = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")


 
tabs = st.tabs(["📝 Code Input", "⚙️ Refactored Output", "🎯 Scorecard", "📊 Module Graph", "✨ Code Optimization Suggestions"])


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



# Module usage ko plot karna
def plot_import_usage(imports):
    import_counts = {imp: imports.count(imp) for imp in set(imports)}  
    colors = [f"rgb({random.randint(50,255)}, {random.randint(50,255)}, {random.randint(50,255)})" for _ in import_counts]  
    fig = px.bar(x=list(import_counts.keys()), y=list(import_counts.values()), 
                 labels={'x':'Used Modules', 'y':'Usage Counts'},
                 title="📊 Module Usage", color=list(import_counts.keys()),  
                 color_discrete_sequence=colors)  
    fig.update_layout(bargap=0.3) 
    st.plotly_chart(fig, use_container_width=True) 




def optimize_code_suggestions(code):
    suggestions = [] 

    # Specific code patterns ke liye suggestions dena
    if "for i in range(len(list))" in code:
        suggestions.append("Use 'for item in list' instead of 'for i in range(len(list))' for better readability.")
    if "== None" in code:
        suggestions.append("Use 'is None' instead of '== None' for better performance and readability.")
    if len(re.findall(r"print\(", code)) > 3:
        suggestions.append("Avoid excessive 'print' statements. Consider logging or using a debugger for better performance.")
    if "for i in range(len(" in code:
        suggestions.append("Consider using 'enumerate()' for cleaner loops, e.g., 'for i, item in enumerate(list):'")
    if "list1 + list2" in code:
        suggestions.append("Avoid concatenating lists inside loops, as it's inefficient. Use 'list.extend()' or 'append()'.")
    if "list.remove(" in code:
        suggestions.append("If you're removing duplicates, consider using 'set()' instead of repeatedly removing elements from a list.")
    if "global " in code:
        suggestions.append("Avoid using 'global' variables. It's better to pass variables as function arguments or return values.")
    if len(re.findall(r"\b[a-z]{1,2}\b", code)) > 5: 
        suggestions.append("Use descriptive variable names instead of single-letter variables (e.g., 'x', 'y').")
    if "open(" in code and "close()" in code:
        suggestions.append("Use 'with open(...) as file' to automatically handle file closing and exceptions.")
    if "if x == None:" in code:
        suggestions.append("Use default arguments instead of manual 'None' checks in function definitions, e.g., 'def func(x=None):'")
    if "lambda " in code and len(re.findall(r"lambda", code)) > 3:
        suggestions.append("Consider replacing redundant lambda functions with regular function definitions.")
    if "list(map(" in code:
        suggestions.append("Consider using list comprehensions instead of 'map()' for better readability and performance.")

    return suggestions 




# Footer with Social Icons
st.markdown("""
    <div class='footer'>
        RefactorPro &copy; 2025 &mdash; Built with ❤️ by Fiza Asif<br>
    </div>
""", unsafe_allow_html=True)
