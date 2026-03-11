import io

from fastapi import UploadFile, HTTPException
from PIL import Image

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB


async def decode_and_validate_image(upload: UploadFile) -> Image.Image:
    """Read an UploadFile, validate type/size, and return a PIL RGB image."""
    if not upload.content_type or not upload.content_type.startswith("image/"):
        raise HTTPException(400, detail="Solo se aceptan imágenes JPG/PNG")

    contents = await upload.read()

    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(400, detail="La imagen excede 10 MB")

    return Image.open(io.BytesIO(contents)).convert("RGB")
