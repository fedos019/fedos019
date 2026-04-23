"""Centralized file paths for the STL/JPG -> point-cloud pipeline.

Edit this file once and run scripts without CLI arguments.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Inputs
INPUT_STL = DATA_DIR / "model.stl"
INPUT_JPG = DATA_DIR / "photo.jpg"

# Intermediate clouds
STL_CLOUD = OUTPUT_DIR / "model_cloud.ply"
JPG_CLOUD = OUTPUT_DIR / "photo_cloud.ply"

# Final outputs
ALIGNED_STL = OUTPUT_DIR / "model_aligned.stl"
TRANSFORM_TXT = OUTPUT_DIR / "transform.txt"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
