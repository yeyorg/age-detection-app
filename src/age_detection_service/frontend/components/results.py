import streamlit as st


def render_analysis_result(state):

    """
    Renderiza la vista de resultado del análisis de edad en la interfaz de Streamlit.

    Esta función muestra al usuario el resultado obtenido tras procesar la imagen
    capturada. El resultado incluye el rango de edad predicho por el modelo y el
    porcentaje de confianza asociado a esa predicción.

    Dependiendo de si el resultado indica que el usuario es mayor de edad o no,
    se delega la presentación del resultado a una de las siguientes funciones:

        - `_render_success_result`: se ejecuta cuando el usuario es considerado
          mayor de edad y se le permite continuar.
        - `_render_error_result`: se ejecuta cuando el usuario es considerado
          menor de edad y se bloquea el acceso.

    Args:
        state: Objeto que gestiona el estado de la aplicación.
            Debe contener al menos los siguientes atributos:
            - `user_data` (dict): información del usuario ingresada en el formulario.
            - `result` (dict): resultado del análisis de imagen generado por el
              servicio de predicción.

            El diccionario `result` debe contener:
            - `label` (str): rango de edad predicho por el modelo.
            - `confidence` (float): porcentaje de confianza de la predicción.
            - `mayor` (bool): indicador de si el usuario se considera mayor de edad.

    Returns:
        None.
    """

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

    """
    Muestra el resultado positivo del análisis cuando el usuario es mayor de edad.

    Esta función se ejecuta cuando el sistema determina que el rango de edad
    predicho corresponde a una persona mayor de edad. En este caso:

        - Se muestra una animación visual de celebración usando `st.balloons`.
        - Se presenta un mensaje de éxito indicando que el usuario puede ingresar.
        - Se habilita un botón que permite reiniciar el flujo de la aplicación.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe implementar:
            - `reset()`: método para limpiar el estado actual de la sesión.

        datos (dict): Diccionario con la información del usuario.
            Debe contener al menos:
            - `nombre` (str): nombre del usuario que se mostrará en el mensaje
              de confirmación.

    Returns:
        None.
    """

    st.balloons()
    st.success(f"✅ {datos['nombre']}, tienes permitido el ingreso.")
    if st.button("Volver al inicio"):
        state.reset()
        st.rerun()


def _render_error_result(state):
    """
    Muestra el resultado negativo del análisis cuando el usuario es menor de edad.

    Esta función se ejecuta cuando el sistema determina que el rango de edad
    predicho corresponde a una persona menor de edad. En este caso:

        - Se muestra un mensaje de error indicando que el usuario no cumple
          con el requisito de mayoría de edad.
        - Se habilita un botón para reiniciar el flujo de la aplicación y
          regresar al inicio.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe implementar:
            - `reset()`: método para limpiar el estado actual de la sesión.

    Returns:
        None.
    """
    st.error(
        "🚫 No tienes permitido continuar ya que no cumples con la mayoría de edad."
    )
    if st.button("Volver al inicio"):
        state.reset()
        st.rerun()
