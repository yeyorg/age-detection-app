from datetime import date

import streamlit as st

from age_detection_service.core.age_verification import (
    MAX_BIRTHDATE,
    validar_formulario,
)


def render_user_form(state):
    """
    Renderiza el formulario de registro del usuario en la interfaz de Streamlit.

    Esta función construye la vista donde el usuario ingresa sus datos personales
    antes de realizar la verificación mediante imagen. El formulario solicita:

    - Nombre completo
    - Género
    - Número de cédula
    - Fecha de nacimiento

    La fecha de nacimiento se restringe mediante un rango válido definido por
    `MAX_BIRTHDATE`, lo que asegura que únicamente se puedan registrar personas
    nacidas antes o en esa fecha límite.

    Flujo de la función:
        1. Muestra el título de la sección.
        2. Renderiza un formulario interactivo usando `st.form`.
        3. Recoge los datos ingresados por el usuario.
        4. Muestra una nota informativa sobre la restricción de fechas.
        5. Si el usuario envía el formulario, delega el procesamiento y validación
           de los datos a `_handle_form_submission`.

    Args:
        state: Objeto que gestiona el estado de la aplicación.
            Debe proporcionar métodos para manejar el flujo de navegación
            y almacenamiento de datos del usuario, tales como:
            - `set_user_data(data)`: guarda los datos del usuario.
            - `set_page(page_name)`: cambia la página o vista actual.

    Returns:
        None.
    """

    st.subheader("Datos del usuario")

    with st.form("registro_usuario"):
        nombre = st.text_input("Nombre completo")
        genero = st.selectbox(
            "Género",
            options=["", "Femenino", "Masculino", "Otro", "Prefiero no decirlo"],
        )
        cedula = st.text_input("Cédula")
        fecha_nacimiento = st.date_input(
            "Fecha de nacimiento",
            min_value=date(1900, 1, 1),
            max_value=MAX_BIRTHDATE,
            value=date(2000, 1, 1),
            format="DD/MM/YYYY",
        )

        submitted = st.form_submit_button("Continuar")

    st.caption(
        f"Solo se permiten personas nacidas hasta el {MAX_BIRTHDATE.strftime('%d/%m/%Y')}."
    )

    if submitted:
        _handle_form_submission(state, nombre, genero, cedula, fecha_nacimiento)


def _handle_form_submission(state, nombre, genero, cedula, fecha_nacimiento):
    """
    Procesa los datos enviados desde el formulario de registro del usuario.

    Esta función recibe los valores ingresados en el formulario y realiza la
    validación correspondiente utilizando la función `validar_formulario`.
    Dependiendo del resultado de la validación, se ejecuta uno de los siguientes
    comportamientos:

    El objetivo es garantizar que solo los datos correctos y completos pasen a la
    siguiente etapa del flujo de la aplicación.

    Args:
        state: Objeto que administra el estado de la aplicación.
            Debe implementar al menos los siguientes métodos:
            - `set_user_data(data)`: almacena la información del usuario en la sesión.
            - `set_page(page_name)`: cambia la página actual dentro del flujo de la app.

        nombre (str):
            Nombre completo ingresado por el usuario en el formulario.

        genero (str):
            Género seleccionado por el usuario a partir de las opciones disponibles.

        cedula (str):
            Número de identificación ingresado por el usuario.

        fecha_nacimiento (date):
            Fecha de nacimiento seleccionada por el usuario mediante el selector
            de fecha (`st.date_input`).

    Returns:
        None.
    """

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
            "edad": edad,
        }
        state.set_user_data(user_data)
        state.set_page("camara")
        st.rerun()
