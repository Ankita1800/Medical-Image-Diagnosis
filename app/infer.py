from typing import Tuple
import io

from PIL import Image, ImageOps
import numpy as np

from .dicom_utils import load_and_deidentify_dicom


def _to_512_grayscale(image: Image.Image) -> Image.Image:
	if image.mode != "L":
		image = ImageOps.grayscale(image)
	return image.resize((512, 512))


def preprocess_image(data: bytes, content_type: str) -> Tuple[np.ndarray, bytes]:
	if content_type in ("image/png", "image/jpeg"):
		img = Image.open(io.BytesIO(data))
		img = _to_512_grayscale(img)
		buf = io.BytesIO()
		img.save(buf, format="PNG")
		arr = np.array(img, dtype=np.float32) / 255.0
		return arr, buf.getvalue()
	elif content_type in ("application/dicom", "application/dicom+json", "application/dicom+octet-stream", "application/octet-stream"):
		# Attempt DICOM parse; fall back to image decode if not DICOM
		try:
			_, deid_bytes = load_and_deidentify_dicom(data)
			ds_img = Image.fromarray(Image.open(io.BytesIO(deid_bytes)))  # may raise
		except Exception:
			img = Image.open(io.BytesIO(data))
			ds_img = img
		ds_img = _to_512_grayscale(ds_img)
		buf = io.BytesIO()
		ds_img.save(buf, format="PNG")
		arr = np.array(ds_img, dtype=np.float32) / 255.0
		return arr, buf.getvalue()
	else:
		# Try generic image
		img = Image.open(io.BytesIO(data))
		img = _to_512_grayscale(img)
		buf = io.BytesIO()
		img.save(buf, format="PNG")
		arr = np.array(img, dtype=np.float32) / 255.0
		return arr, buf.getvalue()


def run_inference_stub(img_tensor: np.ndarray) -> Tuple[dict, bytes]:
	# Return fixed probabilities and a fake heatmap overlay for now
	probs = {"normal": 0.12, "pneumonia": 0.7, "tb": 0.18}
	# Create a simple heatmap: vertical gradient
	h, w = img_tensor.shape
	heat = (np.linspace(0, 255, w, dtype=np.uint8)[None, :]).repeat(h, axis=0)
	heat_img = Image.fromarray(heat)
	buf = io.BytesIO()
	heat_img.save(buf, format="PNG")
	return probs, buf.getvalue()