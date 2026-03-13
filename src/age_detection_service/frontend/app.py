import streamlit as st
from age_detection_service.frontend.ui import render_formulario


st.set_page_config(page_title="Detección de edad", page_icon="📷")

st.title("Verificación de edad")

render_formulario()
