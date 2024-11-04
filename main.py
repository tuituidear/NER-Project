import streamlit as st

# สร้างหน้า Streamlit
st.title("NER Visualization with Spark NLP and Streamlit")
text_input = st.text_area("Enter text for NER analysis", "Enter your text here...")
