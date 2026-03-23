import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { backendApi } from "@/lib/api";
import type { BackendHealth, BackendRecord, CommandReceipt, LiveFrame } from "@/lib/types";
import { humanizeEnum, humanizeReason } from "@/lib/presenters";

type CommandIntent = {
  corrId: string;
  label: string;
};

type CommandOutcome = {
  status: "idle" | "dispatched" | "accepted" | "rejected";
  title: string;
  detail: string;
};

type DashboardState = {
  health: BackendHealth | null;
  currentStatus: BackendRecord | null;
  recentEvents: BackendRecord[];
  recentCommands: BackendRecord[];
  recentTelemetry: BackendRecord[];
  liveFrames: LiveFrame[];
  wsState: "connecting" | "live" | "idle";
  lastDispatch: CommandReceipt | { published: false; topic: string; payload: string; qos: number; retain: false } | null;
  lastOutcome: CommandOutcome | null;
  error: string | null;
  refresh: () => Promise<void>;
  sendMode: (mode: string) => Promise<void>;
  sendManual: (linear: number, angular: number) => Promise<void>;
  sendReset: (action: string, state: string) => Promise<void>;
};

function buildCorrId(prefix: string) {
  return `${prefix}-${Date.now()}`;
}

export function useDashboard(): DashboardState {
  const [health, setHealth] = useState<BackendHealth | null>(null);
  const [currentStatus, setCurrentStatus] = useState<BackendRecord | null>(null);
  const [recentEvents, setRecentEvents] = useState<BackendRecord[]>([]);
  const [recentCommands, setRecentCommands] = useState<BackendRecord[]>([]);
  const [recentTelemetry, setRecentTelemetry] = useState<BackendRecord[]>([]);
  const [liveFrames, setLiveFrames] = useState<LiveFrame[]>([]);
  const [wsState, setWsState] = useState<"connecting" | "live" | "idle">("connecting");
  const [lastDispatch, setLastDispatch] = useState<CommandReceipt | { published: false; topic: string; payload: string; qos: number; retain: false } | null>(null);
  const [lastIntent, setLastIntent] = useState<CommandIntent | null>(null);
  const [error, setError] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const refresh = useCallback(async () => {
    try {
      const [nextHealth, nextStatus, nextEvents, nextCommands, nextTelemetry] = await Promise.all([
        backendApi.health(),
        backendApi.currentStatus(),
        backendApi.recentEvents(),
        backendApi.recentCommands(),
        backendApi.recentTelemetry(),
      ]);
      setHealth(nextHealth);
      setCurrentStatus(nextStatus);
      setRecentEvents(nextEvents);
      setRecentCommands(nextCommands);
      setRecentTelemetry(nextTelemetry);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "unknown_refresh_error");
    }
  }, []);

  const lastOutcome = useMemo<CommandOutcome | null>(() => {
    if (!lastIntent) {
      return null;
    }
    const matchingEvent = recentEvents.find((record) => record.corr_id === lastIntent.corrId) ?? null;
    if (!matchingEvent) {
      return {
        status: "dispatched",
        title: `${lastIntent.label} sent`,
        detail: "The backend published the command. Now wait for an audit/event result from the edge runtime.",
      };
    }
    const result = String(matchingEvent.payload?.result ?? "");
    if (result === "accepted") {
      return {
        status: "accepted",
        title: `${lastIntent.label} accepted`,
        detail: humanizeReason(matchingEvent.payload?.reason ?? "manual_command_accepted"),
      };
    }
    if (result === "rejected") {
      return {
        status: "rejected",
        title: `${lastIntent.label} rejected`,
        detail: humanizeReason(matchingEvent.payload?.reason),
      };
    }
    return {
      status: "dispatched",
      title: `${lastIntent.label} sent`,
      detail: `Latest linked event: ${humanizeEnum(matchingEvent.type)}.`,
    };
  }, [lastIntent, recentEvents]);

  useEffect(() => {
    void refresh();
    const timer = window.setInterval(() => {
      void refresh();
    }, 5000);
    return () => window.clearInterval(timer);
  }, [refresh]);

  useEffect(() => {
    const ws = new WebSocket(backendApi.wsUrl);
    wsRef.current = ws;
    setWsState("connecting");
    ws.onopen = () => setWsState("live");
    ws.onclose = () => setWsState("idle");
    ws.onerror = () => setWsState("idle");
    ws.onmessage = (event) => {
      const frame = JSON.parse(String(event.data)) as LiveFrame;
      setLiveFrames((prev) => [frame, ...prev].slice(0, 16));
      if (frame.type === "ws_status") {
        setWsState("live");
        return;
      }
      if (frame.type === "ws_keepalive") {
        setWsState("idle");
        return;
      }
      const record = frame as unknown as BackendRecord;
      if (record.category === "status") {
        setCurrentStatus(record);
        return;
      }
      if (record.category === "telemetry") {
        setRecentTelemetry((prev) => [record, ...prev].slice(0, 6));
        return;
      }
      if (record.category === "command") {
        setRecentCommands((prev) => [record, ...prev].slice(0, 8));
        return;
      }
      if (record.category === "event") {
        setRecentEvents((prev) => [record, ...prev].slice(0, 8));
      }
    };

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, []);

  const sendMode = useCallback(async (mode: string) => {
    const corrId = buildCorrId("ui-mode");
    try {
      const receipt = await backendApi.sendMode(mode, corrId);
      setLastDispatch(receipt);
      setLastIntent({ corrId, label: `Mode ${humanizeEnum(mode)}` });
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "mode_dispatch_error");
    }
  }, []);

  const sendManual = useCallback(async (linear: number, angular: number) => {
    const corrId = buildCorrId("ui-manual");
    try {
      const receipt = await backendApi.sendManual(linear, angular, 500, corrId);
      setLastDispatch(receipt);
      setLastIntent({ corrId, label: "Manual motion" });
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "manual_dispatch_error");
    }
  }, []);

  const sendReset = useCallback(async (action: string, state: string) => {
    const corrId = buildCorrId("ui-reset");
    try {
      const receipt = await backendApi.sendReset(action, state, corrId);
      setLastDispatch(receipt);
      setLastIntent({ corrId, label: "Reset request" });
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "reset_dispatch_error");
    }
  }, []);

  return useMemo(
    () => ({
      health,
      currentStatus,
      recentEvents,
      recentCommands,
      recentTelemetry,
      liveFrames,
      wsState,
      lastDispatch,
      lastOutcome,
      error,
      refresh,
      sendMode,
      sendManual,
      sendReset,
    }),
    [
      currentStatus,
      error,
      health,
      lastDispatch,
      lastOutcome,
      liveFrames,
      recentCommands,
      recentEvents,
      recentTelemetry,
      refresh,
      sendManual,
      sendMode,
      sendReset,
      wsState,
    ],
  );
}
