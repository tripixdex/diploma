from __future__ import annotations

from edge_commands import invalid_command, manual_drive, request_manual_mode, startup_ok
from edge_runtime import EdgeRuntime


def main() -> None:
    runtime = EdgeRuntime()
    print("AGV Denford edge MVP demo")

    runtime.handle_command(startup_ok())
    runtime.handle_command(request_manual_mode())
    runtime.handle_command(manual_drive(runtime.config.demo_manual_linear, runtime.config.demo_manual_angular))

    print("Advancing heartbeat ticks to force degraded behavior")
    for tick in range(1, runtime.config.heartbeat_timeout_ticks + 1):
        print(f"[demo] heartbeat_tick={tick}")
        runtime.heartbeat_tick()

    print("Trying locally unsafe motion command after link loss")
    runtime.handle_command(manual_drive(runtime.config.demo_manual_linear, runtime.config.demo_manual_angular))

    print("Submitting explicit invalid command for contract-level rejection")
    runtime.handle_command(invalid_command("unsupported_operator_request"))

    snapshot = runtime.snapshot()
    print("final_snapshot")
    print(snapshot)
    print(f"edge_records={len(runtime.adapter.records)}")


if __name__ == "__main__":
    main()
