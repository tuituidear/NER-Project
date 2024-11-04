import streamlit as st
import pandas as pd

st.title("TESTTEST")
df = pd.DataFrame(
    {'first column' : [1,2,3,4],
    'secound column' : [10,20,30,40]}
)
st.dataframe(df)