"""Backward-compatible entry point — delegates to the new api.app module.

Usage:
    uvicorn age_detection_service.api.app:app

This file is kept only so that existing scripts referencing
'age_detection_service.API.main' continue to work.
"""

from age_detection_service.api.app import app  # noqa: F401

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
