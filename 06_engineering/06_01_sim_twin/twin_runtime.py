from __future__ import annotations

from twin_models import TwinContext, TwinEvent, TwinState
from twin_publishers import InMemoryPublisher
from twin_state_machine import TwinStateMachine


class TwinRuntime:
    def __init__(self) -> None:
        self.publisher = InMemoryPublisher()
        self.context = TwinContext()
        self.state_machine = TwinStateMachine(self.publisher)
        self.transition_log: list[tuple[str, str, str, bool]] = []

    @property
    def state(self) -> TwinState:
        return self.context.state

    def handle(self, event: TwinEvent) -> bool:
        previous = self.context.state
        changed = self.state_machine.apply(self.context, event)
        current = self.context.state
        self.transition_log.append((event.event_type.value, previous.value, current.value, changed))
        print(f"[transition] {event.event_type.value}: {previous.value} -> {current.value} changed={changed}")
        return changed
