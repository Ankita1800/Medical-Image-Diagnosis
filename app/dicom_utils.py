from typing import Tuple
import io

import pydicom
from pydicom.uid import generate_uid


# Minimal de-identification: remove direct identifiers; keep technical metadata
REMOVE_TAGS = [
	(0x0010, 0x0010),  # PatientName
	(0x0010, 0x0020),  # PatientID
	(0x0010, 0x0030),  # PatientBirthDate
	(0x0010, 0x0040),  # PatientSex
	(0x0008, 0x0090),  # ReferringPhysicianName
	(0x0010, 0x2160),  # EthnicGroup
]


def load_and_deidentify_dicom(data: bytes) -> Tuple[pydicom.dataset.FileDataset, bytes]:
	ds = pydicom.dcmread(io.BytesIO(data))
	# Remove direct identifiers
	for tag in REMOVE_TAGS:
		if tag in ds:
			del ds[tag]
	# Replace UIDs for anonymization
	if "StudyInstanceUID" in ds:
		ds.StudyInstanceUID = generate_uid()
	if "SeriesInstanceUID" in ds:
		ds.SeriesInstanceUID = generate_uid()
	if "SOPInstanceUID" in ds:
		ds.SOPInstanceUID = generate_uid()
	# Return possibly modified bytes
	buf = io.BytesIO()
	ds.save_as(buf)
	return ds, buf.getvalue()