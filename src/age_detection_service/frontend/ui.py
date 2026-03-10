import streamlit as st
from PIL import Image
from datetime import date
from age_detection_service.backend.server import analyze_image
from age_detection_service.backend.validation import validar_formulario
from age_detection_service.backend.config import MAX_BIRTHDATE


class SessionStateManager:
    """Gestiona el estado de la sesión de Streamlit de forma centralizada."""

    @staticmethod
    def init_state():
        if "page" not in st.session_state:
            st.session_state.page = "formulario"
        if "user_data" not in st.session_state:
            st.session_state.user_data = {}
        if "result" not in st.session_state:
            st.session_state.result = None

    @staticmethod
    def reset():
        st.session_state.page = "formulario"
        st.session_state.user_data = {}
        st.session_state.result = None

    @staticmethod
    def set_page(page_name):
        st.session_state.page = page_name

    @staticmethod
    def set_user_data(data):
        st.session_state.user_data = data

    @staticmethod
    def set_result(result):
        st.session_state.result = result

    @property
    def page(self):
        return st.session_state.page

    @property
    def user_data(self):
        return st.session_state.user_data

    @property
    def result(self):
        return st.session_state.result


def render_formulario():
    state = SessionStateManager()
    state.init_state()

    if state.page == "formulario":
        _render_user_form(state)
    elif state.page == "camara":
        _render_camera_capture(state)
    elif state.page == "resultado":
        _render_analysis_result(state)


def _render_user_form(state):
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
        _handle_form_submission(state, nombre, genero, cedula, fecha_nacimiento)


def _handle_form_submission(state, nombre, genero, cedula, fecha_nacimiento):
    errores, edad = validar_formulario(nombre, genero, cedula, fecha_nacimiento)

    if errores:
        for error in errores:
            st.error(error)
    else:
        user_data = {
            "nombre": nombre.strip(),
            "genero": genero,
            "cedula": cedula.strip(),
            "fecha_nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
            "edad": edad
        }
        state.set_user_data(user_data)
        state.set_page("camara")
        st.rerun()


def _render_camera_capture(state):
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
            result = analyze_image(image)

        state.set_result(result)
        state.set_page("resultado")
        st.rerun()


def _render_analysis_result(state):
    datos = state.user_data
    result = state.result

    st.subheader("Resultado del análisis")
    st.write(f"**Rango de edad predicho:** {result['label']}")
    st.write(f"**Confianza:** {result['confidence']:.2f}%")

    if result["mayor"]:
        _render_success_result(state, datos)
    else:
        _render_error_result(state)


def _render_success_result(state, datos):
    st.balloons()
    st.success(f"✅ {datos['nombre']}, tienes permitido el ingreso.")
    if st.button("Volver al inicio"):
        state.reset()
        st.rerun()


def _render_error_result(state):
    st.error("🚫 No tienes permitido continuar ya que no cumples con la mayoría de edad.")
    if st.button("Volver al inicio"):
        state.reset()
        st.rerun()
