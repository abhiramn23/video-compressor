from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.compress import compress_video

app = FastAPI(title="Video Compression API")

# Directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Constraints
ALLOWED_EXTENSIONS = {".mp4", ".mov", ".mkv"}
MAX_SIZE_MB = 100


@app.post(
    "/compress",
    responses={
        200: {
            "content": {"video/mp4": {}},
            "description": "Compressed video file returned as download"
        },
        413: {"description": "File too large"},
        415: {"description": "Unsupported file type"}
    },
)
async def compress(file: UploadFile = File(...)):
    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    # Read file into memory
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)

    # Validate size
    if size_mb > MAX_SIZE_MB:
        raise HTTPException(status_code=413, detail="File too large")

    # Paths
    input_path = UPLOAD_DIR / file.filename
    output_path = OUTPUT_DIR / f"compressed_{file.filename}"

    # Save uploaded file
    with open(input_path, "wb") as f:
        f.write(contents)

    # Compress using FFmpeg
    compress_video(input_path, output_path)

    # Return compressed file immediately
    return FileResponse(
        path=output_path,
        media_type="video/mp4",
        filename=f"compressed_{file.filename}"
    )
