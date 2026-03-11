import torch
import streamlit as st
from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
from age_detection_service.backend.config import MODEL_NAME, ID2LABEL


@st.cache_resource
def load_model():
    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = SiglipForImageClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return processor, model


def predict_age(image: Image.Image):
    processor, model = load_model()

    image = image.convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=1)[0]

    top_idx = torch.argmax(probs).item()
    label = ID2LABEL[top_idx]
    confidence = float(probs[top_idx]) * 100

    scores = {ID2LABEL[i]: float(probs[i]) * 100 for i in range(len(probs))}

    return label, confidence, scores
