# CXR Pneumonia/TB Screening (Research)

- PRD: prd.json

## Run API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: GET http://localhost:8000/v1/health
- Infer: POST http://localhost:8000/v1/infer (multipart form: file, patient_age [opt], view)
- Metrics: GET http://localhost:8000/v1/metrics

## Batch CLI

```bash
python cli/batch_infer.py /path/to/folder --api http://localhost:8000/v1/infer
```

## Notes
- Stub implementation; replace with real model and Grad-CAM.
- Follows API contract in `prd.json`.