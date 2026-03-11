from .config import CLASES_PERMITIDAS, TODAY, MAX_BIRTHDATE


def es_mayor_segun_prediccion(label):

    return label in CLASES_PERMITIDAS


def calcular_edad(fecha_nacimiento):

    edad = TODAY.year - fecha_nacimiento.year

    if (TODAY.month, TODAY.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1

    return edad


def validar_formulario(nombre, genero, cedula, fecha_nacimiento):

    errores = []

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
