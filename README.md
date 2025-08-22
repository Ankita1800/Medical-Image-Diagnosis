# CXR Pneumonia/TB Screening (Research)

- PRD: prd.json

## Run API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: GET http://localhost:8000/v1/health
- Infer: POST http://localhost:8000/v1/infer (multipart form: file, patient_age [opt], view)
- Metrics: GET http://localhost:8000/v1/metrics
- Static files: GET http://localhost:8000/static/<name>.png

## Batch CLI

```bash
python cli/batch_infer.py /path/to/folder --api http://localhost:8000/v1/infer
```

## Notes
- Accepts PNG/JPEG and DICOM; minimal de-identification applied for DICOM.
- Saves preview and heatmap images to `./static` and returns URLs.
- Stub implementation for probabilities and heatmap; replace with real model + Grad-CAM.
- Follows API contract in `prd.json`.