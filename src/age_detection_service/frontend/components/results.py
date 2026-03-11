import streamlit as st


def render_analysis_result(state):
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
    st.error(
        "🚫 No tienes permitido continuar ya que no cumples con la mayoría de edad."
    )
    if st.button("Volver al inicio"):
        state.reset()
        st.rerun()
