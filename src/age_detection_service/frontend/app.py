import streamlit as st
from age_detection_service.frontend.ui import render_formulario

"""
Módulo principal de la interfaz de verificación de edad.

Este archivo actúa como punto de entrada de la aplicación frontend construida
con Streamlit. Su responsabilidad es configurar la página de la aplicación,
mostrar el encabezado principal y delegar la renderización de la interfaz
principal al módulo de UI.

Este módulo no contiene lógica de negocio ni procesamiento de datos;
únicamente se encarga de inicializar la interfaz y conectar con la capa
de presentación definida en `age_detection_service.frontend.ui`.

Dependencias principales:
    - Streamlit: framework utilizado para construir la interfaz web.
    - render_formulario: función encargada de mostrar y gestionar el flujo
      inicial de interacción con el usuario.
"""

st.set_page_config(page_title="Detección de edad", page_icon="📷")

st.title("Verificación de edad")

render_formulario()
