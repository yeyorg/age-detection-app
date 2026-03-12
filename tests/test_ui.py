"""
Pruebas unitarias para la clase `SessionStateManager`.

Este módulo valida el comportamiento de la clase encargada de gestionar
el estado de sesión de Streamlit dentro del frontend de la aplicación.

Dado que estas pruebas se ejecutan fuera del entorno real de Streamlit,
se simulan las dependencias externas necesarias antes de importar el
módulo objetivo. En particular:

    - Se crea un mock de `streamlit` para simular `st.session_state`.
    - Se mockean `torch` y `transformers` para evitar dependencias pesadas
      o innecesarias durante la ejecución de las pruebas.
    - Se agrega el directorio `src` al `sys.path` para permitir la
      importación local del paquete `age_detection_service`.

El objetivo principal de este módulo es comprobar que `SessionStateManager`:

    - inicializa correctamente las claves del estado,
    - reinicia el estado a sus valores por defecto,
    - actualiza correctamente la página activa,
    - guarda datos del usuario,
    - expone correctamente las propiedades de acceso.
"""

import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Añadir el directorio src al path para poder importar el módulo
sys.path.append(str(Path(__file__).parent.parent / "src"))

# Mock streamlit, torch y transformers antes de importar ui
mock_st = MagicMock()
sys.modules["streamlit"] = mock_st
sys.modules["torch"] = MagicMock()
sys.modules["transformers"] = MagicMock()

from age_detection_service.frontend.state import SessionStateManager


class MockSessionState(dict):
    """
    Implementación simulada de `st.session_state` para pruebas unitarias.

    Esta clase hereda de `dict` y añade soporte para acceso mediante
    atributos, imitando el comportamiento habitual de `streamlit.session_state`.

    Su propósito es permitir que las pruebas interactúen con el estado
    de sesión usando tanto sintaxis de diccionario como sintaxis de atributo,
    por ejemplo:

        - `session_state["page"]`
        - `session_state.page`

    Esto facilita la simulación del comportamiento esperado por
    `SessionStateManager` sin requerir una instancia real de Streamlit.
    """

    def __getattr__(self, key):
        """
        Recupera un valor del estado usando acceso por atributo.

        Si la clave existe en el diccionario interno, retorna su valor.
        En caso contrario, lanza `AttributeError` para emular el
        comportamiento estándar de acceso a atributos en Python.

        Args:
            key (str):
                Nombre del atributo o clave que se desea recuperar.

        Returns:
            Any:
                Valor almacenado bajo la clave indicada.

        Raises:
            AttributeError:
                Se lanza si la clave no existe en el diccionario.
        """
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        """
        Asigna un valor al estado usando sintaxis de atributo.

        Este método redirige la asignación al diccionario interno,
        permitiendo que expresiones como `session_state.page = "camara"`
        se almacenen como una entrada normal del diccionario.

        Args:
            key (str):
                Nombre de la clave o atributo a establecer.

            value:
                Valor que se desea almacenar en el estado.

        Returns:
            None.
        """
        self[key] = value


class TestSessionStateManager(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para la clase `SessionStateManager`.

    Esta clase verifica que los métodos de gestión de estado funcionen
    correctamente sobre un `session_state` simulado. Cada prueba se
    ejecuta sobre un estado limpio e independiente.

    Casos cubiertos:
        - Inicialización del estado.
        - Reinicio del estado.
        - Cambio de página.
        - Almacenamiento de datos del usuario.
        - Lectura correcta de propiedades.
    """

    def setUp(self):
        """
        Prepara el entorno antes de cada prueba.

        Este método reinicia el mock de `session_state` para garantizar
        que cada caso de prueba se ejecute sobre un estado limpio y
        aislado, evitando interferencias entre pruebas consecutivas.

        Args:
            None.

        Returns:
            None.
        """
        # Reiniciar el mock de session_state para cada test
        mock_st.session_state = MockSessionState()

    def test_init_state_creates_keys(self):
        """
        Verifica que `init_state` cree las claves necesarias en el estado.

        Esta prueba comprueba que, tras invocar `SessionStateManager.init_state()`,
        se creen las claves esperadas dentro de `session_state`:

            - `page`
            - `user_data`
            - `result`

        Además, valida que la página inicial se establezca en `"formulario"`.

        Args:
            None.

        Returns:
            None.
        """
        SessionStateManager.init_state()
        self.assertIn("page", mock_st.session_state)
        self.assertIn("user_data", mock_st.session_state)
        self.assertIn("result", mock_st.session_state)
        self.assertEqual(mock_st.session_state["page"], "formulario")

    def test_reset_clears_state(self):
        """
        Verifica que `reset` restablezca el estado a sus valores por defecto.

        Esta prueba primero carga valores simulados en el estado y luego
        invoca `SessionStateManager.reset()`. Después, comprueba que:

            - `page` vuelva a `"formulario"`,
            - `user_data` quede como un diccionario vacío,
            - `result` quede en `None`.

        Args:
            None.

        Returns:
            None.
        """
        mock_st.session_state.update(
            {
                "page": "resultado",
                "user_data": {"nombre": "Test"},
                "result": {"mayor": True},
            }
        )
        SessionStateManager.reset()
        self.assertEqual(mock_st.session_state["page"], "formulario")
        self.assertEqual(mock_st.session_state["user_data"], {})
        self.assertIsNone(mock_st.session_state["result"])

    def test_set_page(self):
        """
        Verifica que `set_page` actualice correctamente la página activa.

        Esta prueba llama al método `SessionStateManager.set_page("camara")`
        y valida que el valor almacenado en `session_state["page"]` coincida
        con el valor enviado.

        Args:
            None.

        Returns:
            None.
        """
        SessionStateManager.set_page("camara")
        self.assertEqual(mock_st.session_state["page"], "camara")

    def test_set_user_data(self):
        """
        Verifica que `set_user_data` almacene correctamente los datos del usuario.

        Esta prueba define un diccionario simple de datos y comprueba que,
        al llamar a `SessionStateManager.set_user_data(data)`, dicho
        diccionario quede guardado exactamente en `session_state["user_data"]`.

        Args:
            None.

        Returns:
            None.
        """
        data = {"nombre": "Juan"}
        SessionStateManager.set_user_data(data)
        self.assertEqual(mock_st.session_state["user_data"], data)

    def test_properties_return_correct_values(self):
        """
        Verifica que las propiedades de instancia retornen los valores correctos.

        Esta prueba carga valores simulados en `session_state`, crea una
        instancia de `SessionStateManager` y comprueba que las propiedades:

            - `page`
            - `user_data`
            - `result`

        devuelvan exactamente los datos almacenados en el estado.

        Args:
            None.

        Returns:
            None.
        """
        mock_st.session_state.update(
            {
                "page": "camara",
                "user_data": {"nombre": "Maria"},
                "result": {"label": "21-30"},
            }
        )
        state = SessionStateManager()
        self.assertEqual(state.page, "camara")
        self.assertEqual(state.user_data, {"nombre": "Maria"})
        self.assertEqual(state.result, {"label": "21-30"})


if __name__ == "__main__":
    unittest.main()
