from pydantic import BaseModel, Field
from typing import Dict, Optional, List


class HealthResponse(BaseModel):
	status: str
	model_version: str


class InferenceRequestMeta(BaseModel):
	patient_age: Optional[str] = None
	view: str = Field(default="unknown", pattern="^(PA|AP|unknown)$")


class InferenceResponse(BaseModel):
	classes: List[str] = Field(default_factory=lambda: ["normal", "pneumonia", "tb"])  # PRD order
	probabilities: Dict[str, float]
	calibrated: bool
	heatmap_url: Optional[str] = None
	model_version: str
	inference_ms: int
	preview_url: Optional[str] = None