#!/usr/bin/env python3
import argparse
import sys
import os
import time
import zipfile
import requests

SUPPORTED_EXTS = {".png", ".jpg", ".jpeg", ".dcm"}


def iter_files(path: str):
	if os.path.isdir(path):
		for root, _, files in os.walk(path):
			for fname in files:
				ext = os.path.splitext(fname)[1].lower()
				if ext in SUPPORTED_EXTS:
					yield os.path.join(root, fname)
	elif zipfile.is_zipfile(path):
		with zipfile.ZipFile(path, 'r') as z:
			for info in z.infolist():
				if info.is_dir():
					continue
				ext = os.path.splitext(info.filename)[1].lower()
				if ext in SUPPORTED_EXTS:
					yield z.open(info)
	else:
		yield path


def infer_file(session: requests.Session, url: str, fpath):
	files = {"file": (os.path.basename(fpath) if isinstance(fpath, str) else "zip_member", open(fpath, 'rb') if isinstance(fpath, str) else fpath)}
	data = {"view": "unknown"}
	resp = session.post(url, files=files, data=data, timeout=60)
	resp.raise_for_status()
	return resp.json()


def main():
	parser = argparse.ArgumentParser(description="Batch inference client for CXR API")
	parser.add_argument("input", help="Folder or zip file path")
	parser.add_argument("--api", default="http://localhost:8000/v1/infer")
	args = parser.parse_args()

	session = requests.Session()
	start = time.time()
	count = 0
	for item in iter_files(args.input):
		try:
			res = infer_file(session, args.api, item)
			print(res)
			count += 1
		except Exception as e:
			print(f"Error on {item}: {e}", file=sys.stderr)
	elapsed = time.time() - start
	print(f"Processed {count} files in {elapsed:.2f}s")


if __name__ == "__main__":
	main()