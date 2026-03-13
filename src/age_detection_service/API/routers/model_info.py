from fastapi import APIRouter

from age_detection_service.config import ID2LABEL, MODEL_NAME

router = APIRouter()


@router.get("/model/metadata")
async def model_metadata():
    """
    Endpoint que expone metadatos del modelo de detección de edad.

    Este endpoint permite consultar información básica sobre el modelo
    actualmente configurado en el sistema sin necesidad de realizar
    una predicción. 

    La información retornada describe las características principales
    del modelo, incluyendo su nombre, el número de clases que predice
    y las etiquetas asociadas a cada clase.

    Returns:
        dict:
            Diccionario con los metadatos del modelo que contiene:

            - model_name (str):
                Nombre del modelo utilizado para la detección de edad.
                Este valor proviene de la constante `MODEL_NAME`.

            - num_classes (int):
                Número total de clases de edad que el modelo puede
                predecir. Se calcula a partir de la longitud del
                diccionario `ID2LABEL`.

            - labels (dict[int, str]):
                Diccionario que mapea los índices de clase del modelo
                a sus etiquetas correspondientes de rango de edad.
    """
    return {
        "model_name": MODEL_NAME,
        "num_classes": len(ID2LABEL),
        "labels": ID2LABEL,
    }
