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
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value


class TestSessionStateManager(unittest.TestCase):
    def setUp(self):
        # Reiniciar el mock de session_state para cada test
        mock_st.session_state = MockSessionState()

    def test_init_state_creates_keys(self):
        SessionStateManager.init_state()
        self.assertIn("page", mock_st.session_state)
        self.assertIn("user_data", mock_st.session_state)
        self.assertIn("result", mock_st.session_state)
        self.assertEqual(mock_st.session_state["page"], "formulario")

    def test_reset_clears_state(self):
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
        SessionStateManager.set_page("camara")
        self.assertEqual(mock_st.session_state["page"], "camara")

    def test_set_user_data(self):
        data = {"nombre": "Juan"}
        SessionStateManager.set_user_data(data)
        self.assertEqual(mock_st.session_state["user_data"], data)

    def test_properties_return_correct_values(self):
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
