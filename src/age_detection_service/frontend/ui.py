import streamlit as st
from PIL import Image
from datetime import date
from age_detection_service.backend.server import analyze_image
from age_detection_service.backend.validation import validar_formulario
from age_detection_service.backend.config import MAX_BIRTHDATE


def _init_state():
    if "page" not in st.session_state:
        st.session_state.page = "formulario"
    if "user_data" not in st.session_state:
        st.session_state.user_data = {}
    if "result" not in st.session_state:
        st.session_state.result = None


def _reset():
    st.session_state.page = "formulario"
    st.session_state.user_data = {}
    st.session_state.result = None


def render_formulario():
    _init_state()

    if st.session_state.page == "formulario":
        _render_form()
    elif st.session_state.page == "camara":
        _render_camera()
    elif st.session_state.page == "resultado":
        _render_resultado()


def _render_form():
    st.subheader("Datos del usuario")

    with st.form("registro_usuario"):
        nombre = st.text_input("Nombre completo")
        genero = st.selectbox(
            "Género",
            options=["", "Femenino", "Masculino", "Otro", "Prefiero no decirlo"]
        )
        cedula = st.text_input("Cédula")
        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            min_value=date(1900, 1, 1),
            max_value=MAX_BIRTHDATE,
            value=date(2000, 1, 1),
            format="DD/MM/YYYY"
        )

        submitted = st.form_submit_button("Continuar")

    st.caption(f"Solo se permiten personas nacidas hasta el {MAX_BIRTHDATE.strftime('%d/%m/%Y')}.")

    if submitted:
        errores, edad = validar_formulario(nombre, genero, cedula, fecha_nacimiento)

        if errores:
            for error in errores:
                st.error(error)
        else:
            st.session_state.user_data = {
                "nombre": nombre.strip(),
                "genero": genero,
                "cedula": cedula.strip(),
                "fecha_nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
                "edad": edad
            }
            st.session_state.page = "camara"
            st.rerun()


def _render_camera():
    datos = st.session_state.user_data

    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"Bienvenido(a), {datos['nombre']}")
    with col2:
        if st.button("Salir"):
            _reset()
            st.rerun()

    with st.expander("Ver datos ingresados"):
        st.write(f"**Nombre:** {datos['nombre']}")
        st.write(f"**Género:** {datos['genero']}")
        st.write(f"**Cédula:** {datos['cedula']}")
        st.write(f"**Fecha de nacimiento:** {datos['fecha_nacimiento']}")
        st.write(f"**Edad calculada:** {datos['edad']} años")

    st.subheader("Captura en vivo")
    foto = st.camera_input("Toma una foto")

    if foto is not None:
        image = Image.open(foto)
        st.image(image, caption="Imagen capturada", use_container_width=True)

        if st.button("Analizar imagen"):
            with st.spinner("Procesando imagen..."):
                result = analyze_image(image)

            st.session_state.result = result
            st.session_state.page = "resultado"
            st.rerun()


def _render_resultado():
    datos = st.session_state.user_data
    result = st.session_state.result

    st.subheader("Resultado del análisis")
    st.write(f"**Rango de edad predicho:** {result['label']}")
    st.write(f"**Confianza:** {result['confidence']:.2f}%")

    if result["mayor"]:
        st.balloons()
        st.success(f"✅ {datos['nombre']}, tienes permitido el ingreso.")

        if st.button("Volver al inicio"):
            _reset()
            st.rerun()
    else:
        st.error("🚫 No tienes permitido continuar ya que no cumples con la mayoría de edad.")

        if st.button("Volver al inicio"):
            _reset()
            st.rerun()
