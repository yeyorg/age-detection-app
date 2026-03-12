# Age Detection App — Detección de Edad Facial 🚀

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.135.1-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.55.0-FF4B4B.svg)](https://streamlit.io/)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-yellow)](https://huggingface.co/prithivMLmods/facial-age-detection)

Este proyecto es una aplicación integral para la detección de edad facial, combinando un backend robusto con **FastAPI** y una interfaz de usuario interactiva con **Streamlit**. Utiliza modelos de vanguardia de **Hugging Face** para proporcionar predicciones precisas sobre el rango de edad a partir de imágenes faciales.

---

## 🏗️ Arquitectura del Sistema

La aplicación está diseñada siguiendo principios de código limpio y desacoplamiento, dividida en dos componentes principales:

1.  **Backend (API):** Construido con FastAPI, se encarga de la lógica de negocio y la inferencia del modelo. Expone puntos de enlace (endpoints) para predicción y verificación.
2.  **Frontend (UI):** Una interfaz intuitiva desarrollada en Streamlit que permite a los usuarios cargar imágenes o usar la cámara para obtener resultados en tiempo real.

---

## ✨ Características Principales

-   **Detección Precisa:** Utiliza el modelo `prithivMLmods/facial-age-detection` basado en Transformers.
-   **Interfaz Dual:** Soporte para carga de archivos y captura directa desde la cámara.
-   **Validación de Resultados:** Sistema de verificación integrado para comparar predicciones con etiquetas de referencia (FairFace).
-   **Gestión de Dependencias Moderna:** Implementado con `uv` para una instalación rápida y reproducible.
-   **Monitoreo:** Integración con **MLflow** para el seguimiento de experimentos y registro de modelos.
-   **Calidad de Código:** Configurado con **Ruff** para linting y formateo, y **Pytest** para pruebas unitarias.

---

## 🛠️ Tecnologías Utilizadas

-   **Lenguaje:** Python 3.12+
-   **Machine Learning:** PyTorch, Transformers (Hugging Face), TensorFlow.
-   **API Framework:** FastAPI, Uvicorn.
-   **Web Interface:** Streamlit.
-   **DevOps/Tooling:** UV, Makefile, Docker.

---

## 🚀 Instalación y Configuración

### Requisitos Previos

-   [UV](https://github.com/astral-sh/uv) instalado en el sistema.
-   Python 3.12 o superior.

### Pasos

1.  **Clonar el repositorio:**
    ```bash
    git clone <url-del-repositorio>
    cd age-detection-app
    ```

2.  **Instalar dependencias:**
    ```bash
    make install
    ```
    *Esto creará un entorno virtual y sincronizará todas las bibliotecas necesarias.*

---

## 📖 Instrucciones de Uso

El proyecto incluye un `Makefile` para facilitar la ejecución de las tareas comunes.

### Ejecutar el Servidor API (Backend)

Para iniciar el backend en `http://localhost:8000`:
```bash
make server
```
Puedes acceder a la documentación interactiva de la API en `http://localhost:8000/api/v1/docs`.

### Ejecutar la Aplicación Web (Frontend)

Para iniciar la interfaz de Streamlit:
```bash
make frontend
```

### Otras Tareas

-   **Ejecutar Pruebas:** `make test`
-   **Formatear Código:** `make quality`
-   **MLflow UI:** `make mlflow-ui`

---

## 🖼️ Galería del Proyecto

Aquí puedes encontrar capturas de pantalla de la aplicación en funcionamiento:

> [!NOTE]
> *Agrega aquí las imágenes del proyecto para mostrar la interfaz y los resultados.*

<!-- 
Ejemplo de cómo agregar imágenes:
![Dashboard de Predicción](path/to/screenshot1.png)
![Resultados de Verificación](path/to/screenshot2.png)
-->

---

## 👥 Equipo de Trabajo (Autores)

Este proyecto fue desarrollado por:

-   **Yerson David Rozo Giraldo**
-   **Valentina Lopez Maldonado**
-   **Christian Camilo Pineda Alarcon**
-   **Miguel Angel Zabaleta Gomez**

---

## ⚖️ Licencia y Disclaimer

Este proyecto ha sido desarrollado con fines exclusivamente **educativos**.

> [!WARNING]
> Las predicciones generadas por este modelo tienen carácter informativo y no deben ser utilizadas para fines críticos, médicos o de seguridad sin una validación humana profesional.

Licencia recomendada: **CC BY-NC 4.0** (Attribution-NonCommercial 4.0 International).
