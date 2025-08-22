from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional
import time
import logging

from .schemas import InferenceResponse, HealthResponse
from .metrics import METRICS
from .config import settings
from .infer import preprocess_image, run_inference_stub
from .storage import storage

logger = logging.getLogger("cxr_api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.APP_NAME, version="0.1.0")
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")


@app.get("/v1/health", response_model=HealthResponse)
async def health() -> HealthResponse:
	logger.info("health_check")
	return HealthResponse(status="ok", model_version=settings.MODEL_VERSION)


@app.post("/v1/infer", response_model=InferenceResponse)
async def infer(
	file: UploadFile = File(..., description="image|dicom"),
	patient_age: Optional[str] = Form(default=None),
	view: str = Form(default="unknown")
) -> InferenceResponse:
	if file is None:
		raise HTTPException(status_code=400, detail="file is required")

	raw = await file.read()
	content_type = file.content_type or "application/octet-stream"

	start = time.time()
	logger.info("image_uploaded", extra={"filename": file.filename, "content_type": content_type})
	METRICS.inc("image_uploaded")

	img_tensor, preview_png = preprocess_image(raw, content_type)
	_, preview_url = storage.save_bytes(preview_png, suffix=".png")

	probs, heat_png = run_inference_stub(img_tensor)
	heat_path, heat_url = storage.save_bytes(heat_png, suffix=".png")

	inference_ms = int((time.time() - start) * 1000)
	METRICS.observe_latency_ms(inference_ms)
	METRICS.inc("inference_completed")

	logger.info("inference_completed", extra={"inference_ms": inference_ms})

	return InferenceResponse(
		probabilities=probs,
		calibrated=True,
		heatmap_url=heat_url,
		model_version=settings.MODEL_VERSION,
		inference_ms=inference_ms,
		preview_url=preview_url,
	)


@app.get("/v1/metrics")
async def get_metrics() -> dict:
	return METRICS.snapshot()