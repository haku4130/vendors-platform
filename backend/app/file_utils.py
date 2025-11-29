import os
import uuid

from fastapi import HTTPException, UploadFile
from pathvalidate import sanitize_filename

MAX_FILE_SIZE = 2 * 1024 * 1024
ALLOWED_MIME = {"image/png", "image/jpeg"}


def validate_image(file: UploadFile):
    """Check MIME and size."""
    if file.content_type not in ALLOWED_MIME:
        raise HTTPException(400, "Only PNG or JPEG files are allowed")

    content_length = file.headers.get("content-length")
    if content_length and int(content_length) > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large (max 2MB)")


def generate_avatar_filename(full_name: str, company: str, ext: str) -> str:
    raw = f"{full_name}-{company}"
    safe = sanitize_filename(raw).replace(" ", "_")
    return f"{safe}_{uuid.uuid4()}.{ext}"


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


async def save_file(path: str, file: UploadFile):
    contents = await file.read()
    with open(path, "wb") as f:
        f.write(contents)


def delete_file_if_exists(path: str | None):
    if not path:
        return
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass


def avatar_url_to_path(url: str | None, media_root: str) -> str | None:
    if not url:
        return None

    # url может быть типа: http://localhost:8088/media/avatar/foo.jpg
    # нам нужно извлечь: avatar/foo.jpg
    try:
        parts = url.split("/media/")[1]
    except Exception:
        return None

    return os.path.join(media_root, parts)
