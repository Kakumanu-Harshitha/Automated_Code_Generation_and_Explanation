import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Code Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- API Configuration ---
# Define the base URL of your FastAPI backend
BACKEND_BASE_URL = "http://127.0.0.1:8000"
GENERATE_URL = f"{BACKEND_BASE_URL}/generate_code"
OPTIMIZE_URL = f"{BACKEND_BASE_URL}/optimize_code"

# --- Initialize Session State ---
# This will store the generated code so we can use it for optimization
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = ""
if 'generated_language' not in st.session_state:
    st.session_state.generated_language = ""
if 'problem_description' not in st.session_state:
    st.session_state.problem_description = ""


# --- Main App Interface ---
st.title("🤖 AI Code Assistant")
st.caption("Your intelligent partner for generating and optimizing code.")

# Use tabs for a clean layout
tab1, tab2 = st.tabs(["Code Generation & Optimization", "Manual Code Optimization"])

# --- Tab 1: Code Generation & Direct Optimization ---
with tab1:
    st.header("Generate Code from a Problem Description")

    with st.form("generate_form"):
        problem_description_input = st.text_area("Enter the problem description:", height=150)
        language_input = st.selectbox("Select the language:", ("Python", "JavaScript", "Java", "C++", "SQL"), key="gen_lang")
        
        submitted_generate = st.form_submit_button("Generate Code")

    if submitted_generate and problem_description_input.strip():
        with st.spinner("Generating code and analyzing complexity..."):
            try:
                payload = {"problem_description": problem_description_input, "language": language_input}
                response = requests.post(GENERATE_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    # Store results in session state to use later for optimization
                    st.session_state.generated_code = result.get("code", "")
                    st.session_state.generated_language = language_input
                    st.session_state.problem_description = problem_description_input

                    st.subheader("Complexity Analysis")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Time Complexity**")
                        st.info(result.get("time_complexity", "Not available"))
                    with col2:
                        st.markdown("**Space Complexity**")
                        st.info(result.get("space_complexity", "Not available"))

                    st.subheader("Generated Code")
                    st.code(st.session_state.generated_code, language=language_input.lower())
                    
                    st.subheader("Explanation")
                    st.markdown(result.get("explanation"))
                else:
                    # Clear previous results on error
                    st.session_state.generated_code = ""
                    st.error(f"Error: Received status code {response.status_code}")
                    st.json(response.json())

            except requests.exceptions.ConnectionError:
                st.session_state.generated_code = ""
                st.error("Connection Error: Could not connect to the backend. Please ensure the FastAPI server is running.")
            except Exception as e:
                st.session_state.generated_code = ""
                st.error(f"An unexpected error occurred: {e}")
    elif submitted_generate:
        st.warning("Please enter a problem description.")

    # --- In-Tab Optimization Button ---
    if st.session_state.generated_code:
        st.divider()
        if st.button("🚀 Optimize This Generated Code"):
            with st.spinner("Re-analyzing and optimizing..."):
                try:
                    # Use the stored code and description for optimization
                    payload = {
                        "problem_description": st.session_state.problem_description,
                        "language": st.session_state.generated_language,
                        "code": st.session_state.generated_code
                    }
                    response = requests.post(OPTIMIZE_URL, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        st.subheader("Optimization Results")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Original Complexity**")
                            st.info(f"Time: {result.get('original_complexity', 'N/A')}")
                            st.info(f"Space: {result.get('original_space_complexity', 'N/A')}")
                        with col2:
                            st.markdown("**Optimized Complexity**")
                            st.info(f"Time: {result.get('optimized_complexity', 'N/A')}")
                            st.info(f"Space: {result.get('optimized_space_complexity', 'N/A')}")

                        st.subheader("Optimized Code")
                        st.code(result.get("optimized_code"), language=st.session_state.generated_language.lower())
                        
                        st.subheader("Explanation of Optimization")
                        st.markdown(result.get("optimization_explanation"))
                    else:
                        st.error(f"Error from backend: Status {response.status_code}")
                        st.json(response.json())
                
                except requests.exceptions.ConnectionError:
                    st.error("Connection Error: Could not connect to the backend.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")


# --- Tab 2: Manual Code Optimization ---
with tab2:
    st.header("Manually Optimize Code & Analyze Complexity")
    
    with st.form("optimize_form"):
        original_code = st.text_area("Paste your original code here:", height=200)
        optimize_problem_desc = st.text_area("Briefly describe the problem this code solves (for context):", height=100)
        optimize_language = st.selectbox("Select the code language:", ("Python", "JavaScript", "Java", "C++"), key="opt_lang")
        
        submitted_optimize = st.form_submit_button("Optimize Code")

    if submitted_optimize and original_code.strip():
        with st.spinner("Analyzing and optimizing... This may take a moment."):
            try:
                payload = {
                    "problem_description": optimize_problem_desc,
                    "language": optimize_language,
                    "code": original_code
                }
                response = requests.post(OPTIMIZE_URL, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.subheader("Complexity Analysis")

                    # Use markdown and info boxes for better text display
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Original Complexity**")
                        st.info(f"Time: {result.get('original_complexity', 'N/A')}")
                        st.info(f"Space: {result.get('original_space_complexity', 'N/A')}")
                    with col2:
                        st.markdown("**Optimized Complexity**")
                        st.info(f"Time: {result.get('optimized_complexity', 'N/A')}")
                        st.info(f"Space: {result.get('optimized_space_complexity', 'N/A')}")

                    st.subheader("Optimized Code")
                    st.code(result.get("optimized_code"), language=optimize_language.lower())
                    
                    st.subheader("Explanation of Optimization")
                    st.markdown(result.get("optimization_explanation"))
                else:
                    st.error(f"Error from backend: Status {response.status_code}")
                    st.json(response.json())
            
            except requests.exceptions.ConnectionError:
                st.error("Connection Error: Could not connect to the backend.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
    elif submitted_optimize:
        st.warning("Please paste your code before optimizing.")

