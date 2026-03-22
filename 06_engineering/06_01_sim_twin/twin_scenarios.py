from __future__ import annotations

from dataclasses import dataclass

from twin_events import (
    auto_line_complete,
    clear_safe_stop,
    estop_reset,
    estop_triggered,
    heartbeat_lost,
    invalid_command,
    link_restored,
    manual_command,
    obstacle_detected,
    request_auto_line_mode,
    request_manual_mode,
    startup_ok,
)
from twin_runtime import TwinRuntime


@dataclass(slots=True)
class ScenarioResult:
    name: str
    preconditions: str
    trigger: str
    expected_transition: str
    actual_transition: str
    expected_published_evidence: str
    actual_published_evidence: str
    passed: bool
    notes: str


def _format_topics(runtime: TwinRuntime) -> str:
    return ", ".join(message.topic for message in runtime.publisher.messages)


def _has_topics(runtime: TwinRuntime, topics: list[str]) -> bool:
    actual_topics = {message.topic for message in runtime.publisher.messages}
    return all(topic in actual_topics for topic in topics)


def run_basic_demo(runtime: TwinRuntime) -> None:
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(manual_command(0.2, 0.0))
    runtime.handle(obstacle_detected())
    runtime.handle(clear_safe_stop())


def run_auto_line_and_docking(runtime: TwinRuntime) -> None:
    runtime.handle(startup_ok())
    runtime.handle(request_auto_line_mode())
    runtime.handle(auto_line_complete())


def run_estop_cycle(runtime: TwinRuntime) -> None:
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(estop_triggered())
    runtime.handle(estop_reset())


def run_link_loss_cycle(runtime: TwinRuntime) -> None:
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(heartbeat_lost())
    runtime.handle(link_restored())


def run_invalid_command_cycle(runtime: TwinRuntime) -> None:
    runtime.handle(startup_ok())
    runtime.handle(invalid_command("mode_request_not_allowed_in_current_state"))


def execute_startup_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "IDLE" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="startup",
        preconditions="Runtime created in INIT, no active e-stop, no startup fault.",
        trigger="startup_ok",
        expected_transition="INIT -> IDLE",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_manual_mode_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(manual_command(0.2, 0.0))
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "MANUAL" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/state/telemetry",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="manual mode",
        preconditions="Runtime in IDLE after startup, no obstacle, no e-stop, link healthy.",
        trigger="mode_manual_requested + manual_command",
        expected_transition="IDLE -> MANUAL, manual command accepted in MANUAL",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + telemetry + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_auto_line_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_auto_line_mode())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "AUTO_LINE" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/state/telemetry",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="auto_line mode",
        preconditions="Runtime in IDLE after startup, line preconditions valid, no blocking safety input.",
        trigger="mode_auto_line_requested",
        expected_transition="IDLE -> AUTO_LINE",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + telemetry + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_obstacle_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(obstacle_detected())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "SAFE_STOP" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/event/alarm",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="obstacle",
        preconditions="Runtime in MANUAL.",
        trigger="obstacle_detected",
        expected_transition="MANUAL -> SAFE_STOP",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + alarm + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_estop_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(estop_triggered())
    runtime.handle(estop_reset())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "IDLE" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/event/alarm",
            "agv/denford/v1/event/fault",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="estop",
        preconditions="Runtime in MANUAL, reset path available after latch.",
        trigger="estop_triggered + estop_reset_accepted",
        expected_transition="MANUAL -> ESTOP_LATCHED -> IDLE",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + alarm + fault + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_loss_link_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_manual_mode())
    runtime.handle(heartbeat_lost())
    runtime.handle(link_restored())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "IDLE" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/event/alarm",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="loss_link",
        preconditions="Runtime in MANUAL, link initially healthy.",
        trigger="heartbeat_lost + link_restored_and_safe",
        expected_transition="MANUAL -> DISCONNECTED_DEGRADED -> IDLE",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + alarm + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_docking_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(request_auto_line_mode())
    runtime.handle(auto_line_complete())
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "IDLE" and _has_topics(
        runtime,
        [
            "agv/denford/v1/event/audit",
            "agv/denford/v1/state/status",
            "agv/denford/v1/state/telemetry",
            "agv/denford/v1/health/heartbeat",
        ],
    )
    return ScenarioResult(
        name="docking",
        preconditions="Runtime in AUTO_LINE with logical docking completion event available.",
        trigger="auto_line_complete",
        expected_transition="AUTO_LINE -> IDLE",
        actual_transition=actual_transition,
        expected_published_evidence="audit + state/status + telemetry + heartbeat",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_invalid_command_scenario() -> ScenarioResult:
    runtime = TwinRuntime()
    runtime.handle(startup_ok())
    runtime.handle(invalid_command("mode_request_not_allowed_in_current_state"))
    actual_transition = " | ".join(f"{prev} -> {curr}" for _, prev, curr, _ in runtime.transition_log)
    passed = runtime.state.value == "IDLE" and _has_topics(runtime, ["agv/denford/v1/event/audit"])
    return ScenarioResult(
        name="invalid command rejection",
        preconditions="Runtime in IDLE, invalid operator command injected.",
        trigger="invalid_command",
        expected_transition="No state change; remain in IDLE",
        actual_transition=actual_transition,
        expected_published_evidence="audit rejection",
        actual_published_evidence=_format_topics(runtime),
        passed=passed,
        notes=f"final_state={runtime.state.value}",
    )


def execute_all_mandatory_scenarios() -> list[ScenarioResult]:
    return [
        execute_startup_scenario(),
        execute_manual_mode_scenario(),
        execute_auto_line_scenario(),
        execute_obstacle_scenario(),
        execute_estop_scenario(),
        execute_loss_link_scenario(),
        execute_docking_scenario(),
        execute_invalid_command_scenario(),
    ]
