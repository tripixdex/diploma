from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


def _load_shared_constants_module():
    module_name = "sim_twin_constants_for_transport"
    if module_name in sys.modules:
        return sys.modules[module_name]
    constants_path = Path(__file__).resolve().parents[1] / "06_01_sim_twin" / "constants.py"
    spec = importlib.util.spec_from_file_location(module_name, constants_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load shared constants from {constants_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


SIM_CONSTANTS = _load_shared_constants_module()


@dataclass(frozen=True, slots=True)
class TopicPolicy:
    topic: str
    qos: int
    retain: bool


@dataclass(frozen=True, slots=True)
class BrokerConfig:
    host: str = "127.0.0.1"
    port: int = 18884
    keepalive: int = 30


@dataclass(frozen=True, slots=True)
class ClientConfig:
    edge_client_id: str = "agv-denford-edge"
    operator_client_id: str = "agv-denford-operator"
    observer_client_id: str = "agv-denford-observer"
    late_observer_client_id: str = "agv-denford-observer-late"


BROKER_CONFIG = BrokerConfig()
CLIENT_CONFIG = ClientConfig()

TOPIC_POLICY_BY_KIND = {
    "status": TopicPolicy(SIM_CONSTANTS.TOPIC_STATE_STATUS, qos=1, retain=True),
    "telemetry": TopicPolicy(SIM_CONSTANTS.TOPIC_STATE_TELEMETRY, qos=0, retain=False),
    "alarm": TopicPolicy(SIM_CONSTANTS.TOPIC_EVENT_ALARM, qos=1, retain=False),
    "fault": TopicPolicy(SIM_CONSTANTS.TOPIC_EVENT_FAULT, qos=1, retain=False),
    "audit": TopicPolicy(SIM_CONSTANTS.TOPIC_EVENT_AUDIT, qos=1, retain=False),
    "heartbeat": TopicPolicy(SIM_CONSTANTS.TOPIC_HEALTH_HEARTBEAT, qos=0, retain=False),
}

COMMAND_TOPIC_POLICIES = (
    TopicPolicy(SIM_CONSTANTS.TOPIC_CMD_MANUAL, qos=1, retain=False),
    TopicPolicy(SIM_CONSTANTS.TOPIC_CMD_MODE, qos=1, retain=False),
    TopicPolicy(SIM_CONSTANTS.TOPIC_CMD_RESET, qos=1, retain=False),
)

OBSERVED_TOPIC_POLICIES = (
    TOPIC_POLICY_BY_KIND["status"],
    TOPIC_POLICY_BY_KIND["telemetry"],
    TOPIC_POLICY_BY_KIND["alarm"],
    TOPIC_POLICY_BY_KIND["fault"],
    TOPIC_POLICY_BY_KIND["audit"],
    TOPIC_POLICY_BY_KIND["heartbeat"],
)
