from datetime import date

MODEL_NAME = "prithivMLmods/facial-age-detection"

ID2LABEL = {
    0: "Edad 01-10",
    1: "Edad 11-20",
    2: "Edad 21-30",
    3: "Edad 31-40",
    4: "Edad 41-55",
    5: "Edad 56-65",
    6: "Edad 66-80",
    7: "Edad 80+",
}

CLASES_PERMITIDAS = [
    "Edad 21-30",
    "Edad 31-40",
    "Edad 41-55",
    "Edad 56-65",
    "Edad 66-80",
    "Edad 80+"
]

TODAY = date(2026, 3, 7)
MAX_BIRTHDATE = date(2008, 3, 7)