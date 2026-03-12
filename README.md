# age-detection-app

Servicio de detección de rango de edad a partir de imágenes faciales.
El sistema expone una API REST (FastAPI) que ejecuta inferencia sobre el modelo
[`prithivMLmods/facial-age-detection`](https://huggingface.co/prithivMLmods/facial-age-detection)
(ViT, Hugging Face Transformers) y un frontend en Streamlit para consumirla.

---

## Quick start

> **Requisitos:** Python >= 3.12 y [uv](https://github.com/astral-sh/uv) instalado.

```bash
# 1. Clonar e instalar
git clone <url-del-repositorio>
cd age-detection-app
make install                 # uv lock && uv sync

# 2. Configurar variables de entorno
cp .env.example .env         # Editar según el entorno

# 3. Levantar la API
make server                  # http://localhost:8000  (hot-reload)

# 4. Levantar el frontend
make frontend                # Streamlit
```

La documentación Swagger queda en `http://localhost:8000/api/v1/docs`.

---

## Arquitectura

El proyecto separa la capa de presentación, la API y la lógica de dominio:

```
src/age_detection_service/
├── API/
│   ├── routers/          predict, verify, health, model_info
│   ├── schemas/          modelos Pydantic (request / response)
│   └── middleware/       error handler, logging, request ID
├── core/
│   ├── model_service.py        carga e inferencia del modelo
│   ├── image_processing.py     preprocesamiento de imágenes
│   └── age_verification.py     verificación contra etiquetas FairFace
└── frontend/
    ├── components/       cámara, formulario, resultados
    └── api_client.py     cliente HTTP hacia la API

scripts/                  utilidades MLflow (registro, validación, evaluación)
```

El backend recibe una imagen, ejecuta el pipeline de clasificación y devuelve
el rango de edad predicho con sus scores de confianza.
El endpoint `/verify` permite comparar la predicción contra etiquetas del
dataset FairFace.

---

## Stack técnico

| Capa | Tecnologías |
|------|-------------|
| Lenguaje | Python 3.12+ |
| ML / DL | PyTorch, Transformers, TensorFlow |
| API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Tracking | MLflow |
| Tooling | uv, Ruff, pytest |
| Contenedores | Docker |

---

## Comandos disponibles

Todo se gestiona a través del `Makefile`:

**Desarrollo**

| Comando | Descripción |
|---------|-------------|
| `make server` | API con hot-reload (`localhost:8000`) |
| `make frontend` | Interfaz Streamlit |
| `make test` | Pruebas con pytest |
| `make quality` | `ruff format` + `ruff check` |
| `make clean` | Limpia caches y artefactos |

**MLflow**

| Comando | Descripción |
|---------|-------------|
| `make mlflow-ui` | UI de MLflow en puerto 5000 |
| `make register` | Registra el modelo |
| `make validate` | Valida el modelo registrado |
| `make evaluate` | Ejecuta evaluación |

**Producción**

| Comando | Descripción |
|---------|-------------|
| `make apirun` | API sin hot-reload |

---

## Docker

```bash
docker build -t age-detection-app .
docker run -p 8000:8000 age-detection-app
```

El contenedor expone únicamente la API en el puerto 8000.

---

## Autores

- Yerson David Rozo Giraldo
- Valentina Lopez Maldonado
- Christian Camilo Pineda Alarcon
- Miguel Angel Zabaleta Gomez

---

## Licencia

Proyecto con fines educativos bajo licencia **CC BY-NC 4.0**.

> Las predicciones del modelo son informativas y no deben usarse para
> decisiones críticas, médicas o de seguridad sin validación profesional.
