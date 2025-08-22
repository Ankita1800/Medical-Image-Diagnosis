import os
from pathlib import Path


class Settings:
	APP_NAME: str = os.getenv("APP_NAME", "CXR Pneumonia/TB Screening API")
	MODEL_VERSION: str = os.getenv("MODEL_VERSION", "resnet50_v1.2")
	STATIC_DIR: Path = Path(os.getenv("STATIC_DIR", "./static")).resolve()
	BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")


settings = Settings()

# Ensure static dir exists for local heatmap storage
settings.STATIC_DIR.mkdir(parents=True, exist_ok=True)