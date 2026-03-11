from datetime import date

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


def es_mayor_segun_prediccion(label: str) -> bool:
    return label in CLASES_PERMITIDAS


def calcular_edad(fecha_nacimiento: date) -> int:
    edad = TODAY.year - fecha_nacimiento.year
    if (TODAY.month, TODAY.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def validar_formulario(
    nombre: str, genero: str, cedula: str, fecha_nacimiento: date
) -> tuple[list[str], int]:
    errores: list[str] = []

    if not nombre or len(nombre.strip()) < 3:
        errores.append("Nombre inválido")

    if not genero:
        errores.append("Debe seleccionar género")

    if not cedula.isdigit():
        errores.append("La cédula debe ser numérica")

    if fecha_nacimiento > MAX_BIRTHDATE:
        errores.append("Debe ser mayor de edad")

    edad = calcular_edad(fecha_nacimiento)

    if edad < 18:
        errores.append("No cumple mayoría de edad")

    return errores, edad
