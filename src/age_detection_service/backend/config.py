from datetime import date
from age_detection_service.config import ID2LABEL as SHARED_ID2LABEL, MODEL_NAME as SHARED_MODEL_NAME

# Backward-compatible aliases for modules still importing backend.config.
MODEL_NAME = SHARED_MODEL_NAME
ID2LABEL = SHARED_ID2LABEL

CLASES_PERMITIDAS = [
    "Edad 21-30",
    "Edad 31-40",
    "Edad 41-55",
    "Edad 56-65",
    "Edad 66-80",
    "Edad 80+",
]

TODAY = date(2026, 3, 7)
MAX_BIRTHDATE = date(2008, 3, 7)
