import streamlit as st
import pandas as pd
import libreria_funciones as lf

st.title("Proyecto Final")

st.image("python_logo.png")


uploaded_files = st.file_uploader(
    "Upload data", accept_multiple_files=True, type="csv"
)
for uploaded_file in uploaded_files:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    
    
cuota= lf.cuota_prestamo(1000,0.10,5,12)
st.write(cuota)