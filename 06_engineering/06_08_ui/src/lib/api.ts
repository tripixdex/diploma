import type { BackendHealth, BackendRecord, CommandReceipt } from "@/lib/types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8011";
const WS_URL = import.meta.env.VITE_WS_LIVE_URL ?? "ws://127.0.0.1:8011/ws/live";

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${path} (${response.status})`);
  }
  return response.json() as Promise<T>;
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`POST failed: ${path} (${response.status}) ${detail}`);
  }
  return response.json() as Promise<T>;
}

export const backendApi = {
  wsUrl: WS_URL,
  health: () => getJson<BackendHealth>("/health"),
  currentStatus: async () => (await getJson<{ status: BackendRecord | null }>("/api/status/current")).status,
  recentEvents: async (limit = 8) => (await getJson<{ events: BackendRecord[] }>(`/api/events/recent?limit=${limit}`)).events,
  recentCommands: async (limit = 8) => (await getJson<{ commands: BackendRecord[] }>(`/api/commands/recent?limit=${limit}`)).commands,
  recentTelemetry: async (limit = 6) =>
    (await getJson<{ telemetry: BackendRecord[] }>(`/api/telemetry/recent?limit=${limit}`)).telemetry,
  sendMode: (requestedMode: string, corrId?: string) =>
    postJson<CommandReceipt>("/api/control/mode", { requested_mode: requestedMode, corr_id: corrId }),
  sendManual: (linear: number, angular: number, durationMs = 500, corrId?: string) =>
    postJson<CommandReceipt>("/api/control/manual", {
      linear,
      angular,
      duration_ms: durationMs,
      corr_id: corrId,
    }),
  sendReset: (resetAction: string, state: string, corrId?: string) =>
    postJson<CommandReceipt>("/api/control/reset", {
      reset_action: resetAction,
      state,
      corr_id: corrId,
    }),
};
