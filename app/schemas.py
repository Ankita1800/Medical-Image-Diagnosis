from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Optional, List


class HealthResponse(BaseModel):
	model_config = ConfigDict(protected_namespaces=())
	
	status: str
	model_version: str


class InferenceRequestMeta(BaseModel):
	model_config = ConfigDict(protected_namespaces=())
	
	patient_age: Optional[str] = None
	view: str = Field(default="unknown", pattern="^(PA|AP|unknown)$")


class InferenceResponse(BaseModel):
	model_config = ConfigDict(protected_namespaces=())
	
	classes: List[str] = Field(default_factory=lambda: ["normal", "pneumonia", "tb"])  # PRD order
	probabilities: Dict[str, float]
	calibrated: bool
	heatmap_url: Optional[str] = None
	model_version: str
	inference_ms: int