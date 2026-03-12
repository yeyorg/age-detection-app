"""Lógica de verificación de mayoría de edad y validación de formularios.

Contiene funciones para determinar si una predicción de rango de edad
corresponde a un adulto, calcular la edad a partir de la fecha de nacimiento
y validar los datos ingresados por el usuario en el formulario de registro.
"""

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
    """Determina si la etiqueta predicha corresponde a un adulto (>=21 años).

    Args:
        label: Etiqueta de rango de edad predicha por el modelo.

    Returns:
        True si la etiqueta está dentro de los rangos permitidos para adultos.
    """
    return label in CLASES_PERMITIDAS


def calcular_edad(fecha_nacimiento: date) -> int:
    """Calcula la edad en años a partir de la fecha de nacimiento.

    Args:
        fecha_nacimiento: Fecha de nacimiento del usuario.

    Returns:
        Edad en años completos respecto a la fecha de referencia TODAY.
    """
    edad = TODAY.year - fecha_nacimiento.year
    if (TODAY.month, TODAY.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad


def validar_formulario(
    nombre: str, genero: str, cedula: str, fecha_nacimiento: date
) -> tuple[list[str], int]:
    """Valida los campos del formulario de registro de usuario.

    Verifica que el nombre tenga al menos 3 caracteres, que se haya
    seleccionado un género, que la cédula sea numérica y que la fecha
    de nacimiento corresponda a una persona mayor de edad.

    Args:
        nombre: Nombre completo del usuario.
        genero: Género seleccionado.
        cedula: Número de cédula.
        fecha_nacimiento: Fecha de nacimiento del usuario.

    Returns:
        Tupla con la lista de errores de validación y la edad calculada.
    """
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
