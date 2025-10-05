import streamlit as st
import main

# Initialize system once
llm_handler, optimizer, _, _, _ = main.initialize_system()

st.set_page_config(page_title="AI Code Assistant", page_icon="🤖", layout="wide")

st.title("👨‍💻 AI Code Assistant")

language_options = ["Python", "JavaScript", "Java", "C++", "Go", "Rust"]
selected_language = st.selectbox("Select Language", language_options)
problem_prompt = st.text_area("Enter problem description:", height=200)

if st.button("Generate Code"):
    if not problem_prompt.strip():
        st.error("Please enter a problem description.")
    else:
        with st.spinner("Generating code..."):
            code, explanation = llm_handler.generate_with_explanation(problem_prompt, selected_language)
            st.session_state['generated_code'] = code
            st.session_state['explanation'] = explanation

if 'generated_code' in st.session_state and st.session_state['generated_code']:
    st.subheader("Generated Code")
    st.code(st.session_state['generated_code'], language=selected_language.lower())

    st.subheader("Explanation")
    st.markdown(st.session_state['explanation'])

    if st.button("✨ Optimize Code"):
        with st.spinner("Optimizing..."):
            opt_code, opt_expl = optimizer.optimize(problem_prompt, st.session_state['generated_code'], selected_language)
            st.session_state['optimized_code'] = opt_code
            st.session_state['optimized_explanation'] = opt_expl

if 'optimized_code' in st.session_state and st.session_state['optimized_code']:
    st.subheader("Optimized Code")
    st.code(st.session_state['optimized_code'], language=selected_language.lower())
    st.subheader("Optimization Explanation")
    st.markdown(st.session_state['optimized_explanation'])
