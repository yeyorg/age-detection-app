import io

import streamlit as st
from PIL import Image

from age_detection_service.core.age_verification import es_mayor_segun_prediccion
from age_detection_service.frontend.api_client import api_predict


def render_camera_capture(state):
    datos = state.user_data

    _render_user_welcome_header(state, datos)
    _render_user_data_expander(datos)

    st.subheader("Captura en vivo")
    foto = st.camera_input("Toma una foto")

    if foto is not None:
        _handle_camera_input(state, foto)


def _render_user_welcome_header(state, datos):
    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"Bienvenido(a), {datos['nombre']}")
    with col2:
        if st.button("Salir"):
            state.reset()
            st.rerun()


def _render_user_data_expander(datos):
    with st.expander("Ver datos ingresados"):
        st.write(f"**Nombre:** {datos['nombre']}")
        st.write(f"**Género:** {datos['genero']}")
        st.write(f"**Cédula:** {datos['cedula']}")
        st.write(f"**Fecha de nacimiento:** {datos['fecha_nacimiento']}")
        st.write(f"**Edad calculada:** {datos['edad']} años")


def _handle_camera_input(state, foto):
    image = Image.open(foto)
    st.image(image, caption="Imagen capturada", use_container_width=True)

    if st.button("Analizar imagen"):
        with st.spinner("Procesando imagen..."):
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            data = api_predict(buf.getvalue(), "capture.jpg")

            result = {
                "label": data["predicted_age_range"],
                "confidence": data["confidence_percent"],
                "scores": {
                    p["age_range"]: p["confidence_percent"]
                    for p in data["all_probabilities"]
                },
                "mayor": es_mayor_segun_prediccion(data["predicted_age_range"]),
            }

        state.set_result(result)
        state.set_page("resultado")
        st.rerun()
