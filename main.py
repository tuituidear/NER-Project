import joblib
import spacy
from spacy.tokens import Doc
import streamlit as st

# โหลดโมเดล
try:
    model = joblib.load("model.joblib")
except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
    model = None  # กำหนดให้ model เป็น None หากการโหลดล้มเหลว

stopwords = ["ผู้", "ที่", "ซึ่ง", "อัน"]

def tokens_to_features(tokens, i):
    word = tokens[i]
    features = {
        "bias": 1.0,
        "word.word": word,
        "word[:3]": word[:3],
        "word.isspace()": word.isspace(),
        "word.is_stopword()": word in stopwords,
        "word.isdigit()": word.isdigit(),
        "word.islen5": word.isdigit() and len(word) == 5
    }

    if i > 0:
        prevword = tokens[i - 1]
        features.update({
            "-1.word.prevword": prevword,
            "-1.word.isspace()": prevword.isspace(),
            "-1.word.is_stopword()": prevword in stopwords,
            "-1.word.isdigit()": prevword.isdigit(),
        })
    else:
        features["BOS"] = True

    if i < len(tokens) - 1:
        nextword = tokens[i + 1]
        features.update({
            "+1.word.nextword": nextword,
            "+1.word.isspace()": nextword.isspace(),
            "+1.word.is_stopword()": nextword in stopwords,
            "+1.word.isdigit()": nextword.isdigit(),
        })
    else:
        features["EOS"] = True

    return features

def parse_and_visualize(text):
    try:
        tokens = text.split()
        features = [tokens_to_features(tokens, i) for i in range(len(tokens))]
        
        # ตรวจสอบว่าโมเดลถูกโหลดก่อนการทำนาย
        if model is None:
            raise ValueError("โมเดลยังไม่ได้ถูกโหลด.")
        
        predictions = model.predict([features])[0]

        # ใช้ SpaCy Thai tokenizer
        nlp = spacy.blank("th")  # ตรวจสอบให้แน่ใจว่าคุณมี Thai tokenizer ที่เหมาะสม
        doc = Doc(nlp.vocab, words=tokens)

        # สร้าง HTML output โดยคำและป้ายกำกับอยู่ในกล่องเดียวกัน
        html_output = '<div style="font-family: sans-serif; text-align: left; line-height: 1.5;">'
        for i, token in enumerate(tokens):
            label = predictions[i]
            # สร้างกล่องสำหรับคำและป้ายกำกับ
            if label != ' ':  # ตรวจสอบว่ามีป้ายกำกับหรือไม่
                html_output += f'<div style="display: inline-block; margin: 0 5px; text-align: center; border: 1px solid #007bff; padding: 5px; border-radius: 5px;">'
                html_output += f'<div>{token}</div>'
                html_output += f'<div style="background-color: #007bff; color: white; padding: 2px 5px; margin-top: 2px; border-radius: 3px; font-weight: bold; font-size: 0.8em;">{label}</div>'
                html_output += '</div>'
            else:
                html_output += f'<div style="display: inline-block; margin: 0 5px; text-align: center; border: 0px solid #007bff; padding: 5px; border-radius: 5px;">'
                html_output += f'<div>{token}</div>'
                html_output += f'<div style="background-color: #ffffff; color: white; padding: 2px 5px; margin-top: 2px; border-radius: 3px; font-weight: bold; font-size: 0.8em;">{label}</div>'
                html_output += '</div>'
        html_output += '</div>'
        
        return html_output

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการประมวลผล NER: {e}")
        return ""

# แอปพลิเคชัน Streamlit
st.title("Named Entity Recognition (NER)")

text_input = st.text_area("กรอกข้อความที่นี่:", "")
if st.button("Analyst"):
    if text_input:
        html_output = parse_and_visualize(text_input)
        if html_output:
            st.markdown(html_output, unsafe_allow_html=True)
    else:
        st.warning("กรุณากรอกข้อความเพื่อวิเคราะห์.")
