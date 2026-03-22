from __future__ import annotations

from typing import Protocol

from edge_models import EdgeRecord


class EdgeAdapterProtocol(Protocol):
    def publish(self, record: EdgeRecord) -> None:
        ...
