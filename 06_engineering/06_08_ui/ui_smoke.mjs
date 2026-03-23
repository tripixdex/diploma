const API_BASE = process.env.UI_SMOKE_API_BASE ?? "http://127.0.0.1:8011";
const WS_URL = process.env.UI_SMOKE_WS_URL ?? "ws://127.0.0.1:8011/ws/live";

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getJson(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`GET ${path} failed: ${response.status}`);
  }
  return response.json();
}

async function postJson(path, body) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw new Error(`POST ${path} failed: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

async function main() {
  const liveFrames = [];
  const ws = new WebSocket(WS_URL);
  const connected = new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });
  ws.onmessage = (event) => {
    liveFrames.push(JSON.parse(String(event.data)));
  };

  await connected;
  await sleep(1000);

  const initialStatus = await getJson("/api/status/current");
  const initialEvents = await getJson("/api/events/recent?limit=8");
  const initialTelemetry = await getJson("/api/telemetry/recent?limit=6");

  const modeReceipt = await postJson("/api/control/mode", {
    requested_mode: "MANUAL",
    corr_id: `ui-smoke-mode-${Date.now()}`,
  });
  await sleep(1500);

  const manualReceipt = await postJson("/api/control/manual", {
    linear: 0.15,
    angular: 0.0,
    duration_ms: 500,
    corr_id: `ui-smoke-manual-${Date.now()}`,
  });

  await sleep(7000);

  const commands = await getJson("/api/commands/recent?limit=8");
  const events = await getJson("/api/events/recent?limit=12");
  const telemetry = await getJson("/api/telemetry/recent?limit=8");
  const finalStatus = await getJson("/api/status/current");
  ws.close();

  const summary = {
    initial_state: initialStatus.status?.state ?? null,
    initial_events: initialEvents.events.length,
    initial_telemetry: initialTelemetry.telemetry.length,
    mode_published: modeReceipt.published,
    manual_published: manualReceipt.published,
    commands_seen: commands.commands.length,
    events_seen: events.events.length,
    telemetry_seen: telemetry.telemetry.length,
    live_frames: liveFrames.length,
    final_state: finalStatus.status?.state ?? null,
  };

  console.log("ui_smoke_summary");
  console.log(JSON.stringify(summary, null, 2));

  const ok =
    summary.initial_state !== null &&
    summary.mode_published &&
    summary.manual_published &&
    summary.commands_seen >= 2 &&
    summary.events_seen >= 1 &&
    summary.telemetry_seen >= 1 &&
    summary.live_frames >= 3;

  if (!ok) {
    process.exit(1);
  }
}

main().catch((error) => {
  console.error("ui_smoke_failed", error);
  process.exit(1);
});
