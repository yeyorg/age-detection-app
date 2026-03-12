from age_detection_service.frontend.state import SessionStateManager
from age_detection_service.frontend.components.form import render_user_form
from age_detection_service.frontend.components.camera import render_camera_capture
from age_detection_service.frontend.components.results import render_analysis_result


def render_formulario():
    """
    Función orquestadora principal de la interfaz de usuario.

    Esta función controla el flujo de navegación dentro de la aplicación
    de verificación de edad construida con Streamlit. Su responsabilidad
    es determinar qué componente de la interfaz debe renderizarse según
    el estado actual de la sesión.

    Vistas del flujo:
        - "formulario":
            Muestra el formulario inicial donde el usuario ingresa sus datos
            personales (nombre, género, cédula y fecha de nacimiento).

        - "camara":
            Muestra la interfaz de captura de imagen utilizando la cámara
            del dispositivo del usuario. En esta etapa se toma la fotografía
            que será enviada al backend para la predicción de edad.

        - "resultado":
            Muestra el resultado del análisis de la imagen, incluyendo
            el rango de edad estimado, el nivel de confianza y la
            validación de mayoría de edad.

    Args:
        None.

    Returns:
        None.
    """
    state = SessionStateManager()
    state.init_state()

    if state.page == "formulario":
        render_user_form(state)
    elif state.page == "camara":
        render_camera_capture(state)
    elif state.page == "resultado":
        render_analysis_result(state)
