import streamlit as st


class SessionStateManager:
    """
    Gestiona el estado de la sesión de Streamlit de forma centralizada.

    Esta clase encapsula el acceso y la manipulación del objeto `st.session_state`
    para mantener la información necesaria durante el flujo de la aplicación.
    Permite almacenar y recuperar datos persistentes entre las distintas
    interacciones del usuario con la interfaz.

    El objetivo de esta clase es evitar accesos directos y dispersos a
    `st.session_state` a lo largo del código, proporcionando una capa
    centralizada y estructurada para gestionar:

        - la página actual de la aplicación,
        - los datos del usuario ingresados en el formulario,
        - los resultados del análisis de edad.

    Estructura del estado manejado:
        - page (str): identifica la vista actual de la aplicación.
        - user_data (dict): información del usuario ingresada en el formulario.
        - result (dict | None): resultado del análisis de imagen generado por la API.
    """

    @staticmethod
    def init_state():
        """
        Inicializa las variables necesarias dentro del estado de sesión de Streamlit.

        Este método verifica si las claves necesarias existen dentro de
        `st.session_state`. Si alguna de ellas no está presente, se crea
        con un valor por defecto.

        Variables inicializadas:
            - `page`: define la página actual de la aplicación. Se inicializa
              con el valor `"formulario"` para comenzar el flujo desde el
              formulario de registro del usuario.

            - `user_data`: diccionario vacío destinado a almacenar los datos
              ingresados por el usuario.

            - `result`: almacena el resultado del análisis de edad obtenido
              tras enviar la imagen al backend. Se inicializa como `None`.

        Args:
            None.

        Returns:
            None.
        """
        if "page" not in st.session_state:
            st.session_state.page = "formulario"
        if "user_data" not in st.session_state:
            st.session_state.user_data = {}
        if "result" not in st.session_state:
            st.session_state.result = None

    @staticmethod
    def reset():
        """
        Reinicia el estado de la sesión de la aplicación.

        Este método restablece todas las variables del estado a sus valores
        iniciales, permitiendo que el flujo de la aplicación comience desde
        el inicio nuevamente.

        Se utiliza típicamente cuando el usuario presiona un botón como
        "Volver al inicio" o "Salir".

        Variables reiniciadas:
            - `page` se establece nuevamente en `"formulario"`.
            - `user_data` se limpia a un diccionario vacío.
            - `result` se restablece a `None`.

        Args:
            None.

        Returns:
            None.
        """
        st.session_state.page = "formulario"
        st.session_state.user_data = {}
        st.session_state.result = None

    @staticmethod
    def set_page(page_name):
        """
        Actualiza la página actual del flujo de la aplicación.

        Este método permite cambiar la vista activa dentro de la aplicación,
        lo cual es útil para navegar entre distintas etapas del proceso,
        como el formulario, la captura de imagen o el resultado del análisis.

        Args:
            page_name (str):
                Nombre de la página o vista que se desea establecer como
                página actual dentro del estado de la sesión.

        Returns:
            None.
        """
        st.session_state.page = page_name

    @staticmethod
    def set_user_data(data):
        """
        Guarda la información del usuario en el estado de sesión.

        Este método se utiliza después de validar el formulario de registro,
        almacenando los datos del usuario para que puedan ser utilizados
        posteriormente en otras vistas de la aplicación.

        Args:
            data (dict):
                Diccionario que contiene la información del usuario.
                Normalmente incluye campos como:
                    - nombre
                    - genero
                    - cedula
                    - fecha_nacimiento
                    - edad

        Returns:
            None.
        """
        st.session_state.user_data = data

    @staticmethod
    def set_result(result):
        """
        Guarda el resultado del análisis de edad en el estado de sesión.

        Este método se utiliza después de recibir la respuesta de la API
        de predicción de edad. El resultado almacenado será utilizado
        posteriormente para mostrar la vista de resultados al usuario.

        Args:
            result (dict):
                Diccionario con el resultado del análisis de imagen.
                Generalmente contiene:
                    - label (str): rango de edad predicho.
                    - confidence (float): porcentaje de confianza.
                    - scores (dict): probabilidades por rango de edad.
                    - mayor (bool): indicador de si el usuario es mayor de edad.

        Returns:
            None.
        """
        st.session_state.result = result

    @property
    def page(self):
        """
        Devuelve la página actual almacenada en el estado de sesión.

        Returns:
            str:
                Nombre de la página activa dentro del flujo de la aplicación.
        """
        return st.session_state.page

    @property
    def user_data(self):
        """
        Devuelve los datos del usuario almacenados en el estado de sesión.

        Returns:
            dict:
                Diccionario con la información del usuario registrada en el
                formulario.
        """
        return st.session_state.user_data

    @property
    def result(self):
        """
        Devuelve el resultado del análisis de edad almacenado en el estado.

        Returns:
            dict | None:
                Diccionario con los resultados del análisis de imagen o `None`
                si aún no se ha realizado la predicción.
        """
        return st.session_state.result
