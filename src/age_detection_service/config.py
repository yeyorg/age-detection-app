"""Shared configuration constants used across API, backend, and scripts."""

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

FAIRFACE_TO_MODEL = {
    "0-2": "Edad 01-10",
    "3-9": "Edad 01-10",
    "10-19": "Edad 11-20",
    "20-29": "Edad 21-30",
    "30-39": "Edad 31-40",
    "40-49": "Edad 41-55",
    "50-59": "Edad 56-65",
    "60-69": "Edad 66-80",
    "more than 70": "Edad 80+",
}
