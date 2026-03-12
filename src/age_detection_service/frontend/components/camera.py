import io

import streamlit as st
from PIL import Image

from age_detection_service.core.age_verification import es_mayor_segun_prediccion
from age_detection_service.frontend.api_client import api_predict


def render_camera_capture(state):
    """
    Renderiza la vista de captura en vivo dentro de la interfaz de Streamlit.

    Esta función se encarga de construir la sección de la aplicación en la que
    el usuario puede visualizar su información previamente registrada, acceder
    al encabezado de bienvenida y capturar una fotografía en tiempo real usando
    la cámara del dispositivo.

    Flujo general:
        1. Obtiene los datos del usuario almacenados en el estado de sesión.
        2. Muestra un encabezado de bienvenida con opción de salir.
        3. Muestra un panel desplegable con los datos ingresados por el usuario.
        4. Habilita el componente de captura de cámara.
        5. Si se captura una imagen, delega su procesamiento a la función
           `_handle_camera_input`.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe exponer al menos:
            - `user_data`: diccionario con la información del usuario.
            - `reset()`: método para reiniciar el estado.
            - otros métodos usados posteriormente en el flujo como
              `set_result()` y `set_page()`.

    Returns:
        None.
    """

    datos = state.user_data

    _render_user_welcome_header(state, datos)
    _render_user_data_expander(datos)

    st.subheader("Captura en vivo")
    foto = st.camera_input("Toma una foto")

    if foto is not None:
        _handle_camera_input(state, foto)


def _render_user_welcome_header(state, datos):

    """
    Muestra el encabezado de bienvenida del usuario en la interfaz.

    Esta función construye una fila con dos columnas:
        - En la primera, muestra un mensaje de bienvenida usando el nombre
          del usuario almacenado en `datos`.
        - En la segunda, renderiza un botón de salida que, al ser presionado,
          reinicia el estado de la aplicación y recarga la interfaz.

    Se utiliza como parte de la pantalla de captura para dar contexto al
    usuario actual y permitirle salir del flujo activo.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe implementar:
            - `reset()`: método para limpiar o reiniciar el estado actual.

        datos (dict): Diccionario con la información del usuario.
            Debe contener como mínimo la clave:
            - `nombre` (str): nombre del usuario que se mostrará en el mensaje
              de bienvenida.

    Returns:
        None.
    """

    col1, col2 = st.columns([4, 1])
    with col1:
        st.success(f"Bienvenido(a), {datos['nombre']}")
    with col2:
        if st.button("Salir"):
            state.reset()
            st.rerun()


def _render_user_data_expander(datos):

    """
    Muestra un panel desplegable con los datos personales ingresados por el usuario.

    Esta función presenta de forma resumida la información registrada previamente
    en el formulario, permitiendo al usuario revisar sus datos antes de realizar
    la captura y análisis de imagen.

    Los datos se muestran dentro de un `st.expander` para no sobrecargar visualmente
    la interfaz principal y mantener la información accesible solo cuando el usuario
    desee consultarla.

    Args:
        datos (dict): Diccionario con la información del usuario.
            Se espera que incluya las siguientes claves:
            - `nombre` (str): nombre completo del usuario.
            - `genero` (str): género ingresado por el usuario.
            - `cedula` (str | int): número de identificación.
            - `fecha_nacimiento` (str | date): fecha de nacimiento registrada.
            - `edad` (int): edad calculada del usuario.

    Returns:
        None.
    """

    with st.expander("Ver datos ingresados"):
        st.write(f"**Nombre:** {datos['nombre']}")
        st.write(f"**Género:** {datos['genero']}")
        st.write(f"**Cédula:** {datos['cedula']}")
        st.write(f"**Fecha de nacimiento:** {datos['fecha_nacimiento']}")
        st.write(f"**Edad calculada:** {datos['edad']} años")


def _handle_camera_input(state, foto):

    """
    Procesa la imagen capturada por la cámara y gestiona el flujo de análisis.

    Esta función recibe el archivo generado por `st.camera_input`, lo abre como
    imagen usando PIL y lo muestra en pantalla como vista previa. Posteriormente,
    cuando el usuario presiona el botón "Analizar imagen", ejecuta el flujo de
    inferencia enviando la imagen al servicio de predicción.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe implementar como mínimo:
            - `set_result(result)`: guarda el resultado del análisis.
            - `set_page(page_name)`: actualiza la vista/página actual.

        foto: Archivo retornado por `st.camera_input`.
            Debe ser un objeto compatible con `PIL.Image.open`, normalmente
            un archivo en memoria con la imagen capturada por la cámara.

    Returns:
        None.

    Notes:
        - La función asume que la respuesta de `api_predict` contiene las claves:
          `predicted_age_range`, `confidence_percent` y `all_probabilities`.
        - La mayoría de edad se determina usando la función
          `es_mayor_segun_prediccion`, basada en el rango de edad predicho.
    """

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
