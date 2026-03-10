from age_detection_service.frontend.state import SessionStateManager
from age_detection_service.frontend.components.form import render_user_form
from age_detection_service.frontend.components.camera import render_camera_capture
from age_detection_service.frontend.components.results import render_analysis_result


def render_formulario():
    """Orquestador principal de la interfaz de usuario."""
    state = SessionStateManager()
    state.init_state()

    if state.page == "formulario":
        render_user_form(state)
    elif state.page == "camara":
        render_camera_capture(state)
    elif state.page == "resultado":
        render_analysis_result(state)
