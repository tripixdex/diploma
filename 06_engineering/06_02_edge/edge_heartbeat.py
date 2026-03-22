from __future__ import annotations


class LinkSupervisor:
    def __init__(self, timeout_ticks: int) -> None:
        self.timeout_ticks = timeout_ticks
        self._ticks_since_activity = 0
        self._link_ok = True

    @property
    def link_ok(self) -> bool:
        return self._link_ok

    def observe_link_activity(self) -> None:
        self._ticks_since_activity = 0
        self._link_ok = True

    def advance(self) -> bool:
        if not self._link_ok:
            return False
        self._ticks_since_activity += 1
        if self._ticks_since_activity >= self.timeout_ticks:
            self._link_ok = False
            return True
        return False

    def restore(self) -> None:
        self._ticks_since_activity = 0
        self._link_ok = True
