from datetime import date

import streamlit as st

from age_detection_service.core.age_verification import (
    MAX_BIRTHDATE,
    validar_formulario,
)


def render_user_form(state):
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
