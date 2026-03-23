from __future__ import annotations


class LinkSupervisor:
    def __init__(self, timeout_ticks: int, prolonged_disconnect_ticks: int) -> None:
        self.timeout_ticks = timeout_ticks
        self.prolonged_disconnect_ticks = prolonged_disconnect_ticks
        self._ticks_since_activity = 0
        self._ticks_in_degraded = 0
        self._link_ok = True
        self._prolonged_disconnect_emitted = False

    @property
    def link_ok(self) -> bool:
        return self._link_ok

    def observe_link_activity(self) -> None:
        self._ticks_since_activity = 0
        self._ticks_in_degraded = 0
        self._link_ok = True
        self._prolonged_disconnect_emitted = False

    def advance(self) -> str:
        if self._link_ok:
            self._ticks_since_activity += 1
            if self._ticks_since_activity >= self.timeout_ticks:
                self._link_ok = False
                self._ticks_in_degraded = 0
                self._prolonged_disconnect_emitted = False
                return "heartbeat_lost"
            return "ok"

        self._ticks_in_degraded += 1
        if (
            not self._prolonged_disconnect_emitted
            and self._ticks_in_degraded >= self.prolonged_disconnect_ticks
        ):
            self._prolonged_disconnect_emitted = True
            return "prolonged_disconnect"
        return "degraded_wait"

    def restore(self) -> None:
        self._ticks_since_activity = 0
        self._ticks_in_degraded = 0
        self._link_ok = True
        self._prolonged_disconnect_emitted = False
