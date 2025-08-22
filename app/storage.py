from pathlib import Path
from typing import Tuple
import uuid

from .config import settings


class LocalStorage:
	def __init__(self, base_dir: Path) -> None:
		self.base_dir = base_dir

	def save_bytes(self, data: bytes, suffix: str = ".png") -> Tuple[str, str]:
		name = f"{uuid.uuid4().hex}{suffix}"
		path = self.base_dir / name
		path.write_bytes(data)
		return str(path), f"{settings.BASE_URL}/static/{name}"


storage = LocalStorage(settings.STATIC_DIR)