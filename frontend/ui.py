# ui.py
import streamlit as st
import requests

st.set_page_config(page_title="Gemini Explainer", page_icon="🤖", layout="wide")

st.title("🤖 AI Code Explanatory")
st.caption("2026 Unified GenAI Edition")

with st.sidebar:
    st.header("Controls")
    is_concise = st.checkbox("One-Sentence Mode", help="Summarize the code into a single line.")
    
    st.divider()
    if st.button("Check Backend Connection"):
        try:
            res = requests.get("http://localhost:8000/models")
            if res.status_code == 200:
                st.success("Backend Online")
                st.json(res.json())
            else:
                st.error("Backend found but returned error.")
        except:
            st.error("Backend Offline. Run main.py first.")

# UI Layout
input_col, output_col = st.columns(2)

with input_col:
    code = st.text_area("Paste Code Here:", height=400, placeholder="paste code...")
    if st.button("Analyze Code", type="primary", use_container_width=True):
        if code:
            with st.spinner("Analyzing..."):
                try:
                    r = requests.post("http://localhost:8000/explain", 
                                     json={"code": code, "concise": is_concise})
                    if r.status_code == 200:
                        st.session_state['expl'] = r.json()['explanation']
                    else:
                        st.error(r.json().get('detail'))
                except Exception as e:
                    st.error(f"UI Error: {e}")

with output_col:
    st.subheader("Analysis Results")
    if 'expl' in st.session_state:
        st.markdown(st.session_state['expl'])
    else:
        st.info("Your explanation will appear here after analysis.")