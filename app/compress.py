import subprocess
from pathlib import Path

def compress_video(input_path: Path, output_path: Path):
    command = [
        "ffmpeg",
        "-i", str(input_path),
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "fast",
        str(output_path)
    ]

    subprocess.run(command, check=True)
