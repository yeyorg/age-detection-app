"""
Constantes de configuración compartidas utilizadas en la API, el backend y los scripts.

Este módulo define constantes utilizadas de forma compartida en distintas
partes del sistema de detección de edad, incluyendo la API, el backend y
scripts auxiliares.

Su propósito es centralizar configuraciones importantes relacionadas con
el modelo de detección de edad y los mapeos de etiquetas utilizadas en
la clasificación de rangos de edad. Esto permite mantener consistencia
en todo el sistema y evitar duplicación de configuraciones en múltiples
módulos.

Constantes definidas:

MODEL_NAME:
    Nombre del modelo de machine learning utilizado para la predicción
    de edad facial. Este identificador corresponde a un modelo alojado
    en Hugging Face que se carga para realizar inferencias.

ID2LABEL:
    Diccionario que mapea los índices de salida del modelo a etiquetas
    legibles de rangos de edad. Cada índice corresponde a una clase
    predicha por el modelo.

FAIRFACE_TO_MODEL:
    Diccionario de conversión entre los rangos de edad utilizados en el
    dataset FairFace y los rangos de edad definidos en el modelo actual.
    Esto permite adaptar salidas de diferentes formatos de dataset o
    modelos hacia una representación unificada dentro del sistema.
"""

MODEL_NAME = "prithivMLmods/facial-age-detection"
"""
str: Nombre del modelo de detección de edad utilizado por el sistema.

Este valor identifica el modelo preentrenado que se utiliza para realizar
la predicción de rangos de edad a partir de imágenes faciales.
Generalmente corresponde a un modelo disponible en Hugging Face Hub
y es utilizado durante la carga del pipeline de inferencia.
"""

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
"""
dict[int, str]: Mapeo entre los índices de salida del modelo y las etiquetas
de rangos de edad correspondientes.

Cada clave representa el índice de la clase predicha por el modelo
de clasificación, mientras que el valor asociado corresponde a la
etiqueta textual que describe el rango de edad estimado.

Ejemplo:
    Si el modelo devuelve la clase `2`, el rango de edad correspondiente
    será `"Edad 21-30"`.
"""

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
"""
dict[str, str]: Mapeo de conversión entre rangos de edad del dataset
FairFace y los rangos de edad definidos en el modelo actual.

Este diccionario se utiliza cuando los datos o predicciones provienen
de un sistema que utiliza el esquema de rangos de edad del dataset
FairFace. El objetivo es transformar esos rangos hacia el formato
estandarizado utilizado por el modelo de detección de edad del sistema.

Esto permite mantener consistencia en la interpretación de los resultados
independientemente del origen del rango de edad.
"""