import streamlit as st

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
