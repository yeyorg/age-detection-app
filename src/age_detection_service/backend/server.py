from age_detection_service.backend.model import predict_age
from age_detection_service.backend.validation import es_mayor_segun_prediccion


def analyze_image(image):
    label, confidence, scores = predict_age(image)
    mayor = es_mayor_segun_prediccion(label)

    return {
        "label": label,
        "confidence": confidence,
        "scores": scores,
        "mayor": mayor
    }