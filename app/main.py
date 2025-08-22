from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time
import logging

from .schemas import InferenceResponse, HealthResponse

logger = logging.getLogger("cxr_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="CXR Pneumonia/TB Screening API", version="0.1.0")


@app.get("/v1/health", response_model=HealthResponse)
async def health() -> HealthResponse:
	logger.info("health_check")
	return HealthResponse(status="ok", model_version="resnet50_v1.2")


@app.post("/v1/infer", response_model=InferenceResponse)
async def infer(
	file: UploadFile = File(..., description="image|dicom"),
	patient_age: Optional[str] = Form(default=None),
	view: str = Form(default="unknown")
) -> InferenceResponse:
	if file is None:
		raise HTTPException(status_code=400, detail="file is required")

	start = time.time()
	logger.info("image_uploaded", extra={"file_name": file.filename, "content_type": file.content_type})

	probabilities = {"normal": 0.12, "pneumonia": 0.7, "tb": 0.18}
	inference_ms = int((time.time() - start) * 1000)

	logger.info("inference_completed", extra={"inference_ms": inference_ms})

	return InferenceResponse(
		probabilities=probabilities,
		calibrated=True,
		heatmap_url="https://storage/heatmaps/abc.png",
		model_version="resnet50_v1.2",
		inference_ms=inference_ms,
	)