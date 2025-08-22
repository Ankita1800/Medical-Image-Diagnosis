import threading
import time
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Counters:
	image_uploaded: int = 0
	inference_completed: int = 0
	override_made: int = 0
	report_exported: int = 0


class Metrics:
	def __init__(self) -> None:
		self._lock = threading.Lock()
		self._counters = Counters()
		self._latency_ms_sum: int = 0
		self._latency_ms_count: int = 0
		self._start_time = time.time()

	def inc(self, name: str) -> None:
		with self._lock:
			if not hasattr(self._counters, name):
				raise KeyError(name)
			setattr(self._counters, name, getattr(self._counters, name) + 1)

	def observe_latency_ms(self, value: int) -> None:
		with self._lock:
			self._latency_ms_sum += int(value)
			self._latency_ms_count += 1

	def snapshot(self) -> Dict:
		with self._lock:
			uptime_s = int(time.time() - self._start_time)
			avg_latency_ms = (
				self._latency_ms_sum / self._latency_ms_count if self._latency_ms_count else 0.0
			)
			return {
				"counters": {
					"image_uploaded": self._counters.image_uploaded,
					"inference_completed": self._counters.inference_completed,
					"override_made": self._counters.override_made,
					"report_exported": self._counters.report_exported,
				},
				"performance": {
					"avg_inference_latency_ms": avg_latency_ms,
				},
				"uptime_s": uptime_s,
			}


METRICS = Metrics()