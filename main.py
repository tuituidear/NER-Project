import streamlit as st

# สร้างหน้า Streamlit
st.title("NER Visualization with Spark NLP and Streamlit")
text_input = st.text_area("Enter text for NER analysis", "Enter your text here...")

if st.button("Analyze"):
    entities = analyze_text(text_input)
    
    # แสดงผลลัพธ์
    st.write("Entities recognized:")
    for entity in entities:
        st.write(f"{entity['entity']} - {entity['result']} (Score: {entity['confidence']:.2f})")
