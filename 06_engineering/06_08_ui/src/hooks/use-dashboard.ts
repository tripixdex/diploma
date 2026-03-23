import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { backendApi } from "@/lib/api";
import type { BackendHealth, BackendRecord, CommandReceipt, LiveFrame } from "@/lib/types";
import { humanizeEnum, humanizeReason } from "@/lib/presenters";

type CommandIntent = {
  corrId: string;
  commandMsgId: string | null;
  label: string;
  timeoutMs: number;
  sentAtMs: number;
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

function timeoutForCommand(kind: "mode" | "manual" | "reset") {
  if (kind === "manual") return 1000;
  if (kind === "reset") return 3000;
  return 2000;
}

function buildRejectedOutcome(label: string, detail: string): CommandOutcome {
  return {
    status: "rejected",
    title: `${label}: отклонено`,
    detail,
  };
}

function describeDispatchError(err: unknown): string {
  if (!(err instanceof Error)) {
    return "Команда отклонена до публикации. Детали ошибки недоступны.";
  }
  const normalized = err.message.replace(/^POST failed:\s*/i, "");
  if (normalized.includes("Разрешены только mode-команды")) return "Backend отверг mode-команду: разрешены только MANUAL и AUTO_LINE.";
  if (normalized.includes("Разрешены только reset-действия")) return "Backend отверг reset-запрос: действие не входит в allowlist.";
  if (normalized.includes("Reset допустим только")) return normalized.split("] ").pop() ?? normalized;
  if (normalized.includes("Числовые поля manual-команды")) return normalized.split("] ").pop() ?? normalized;
  if (normalized.includes("Input should be")) return "Backend отверг команду из-за неверного типа или формата поля.";
  return `Команда отклонена до публикации: ${normalized}`;
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
  const [lastImmediateOutcome, setLastImmediateOutcome] = useState<CommandOutcome | null>(null);
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
      setError(err instanceof Error ? `Не удалось обновить данные: ${err.message}` : "Не удалось обновить данные с backend.");
    }
  }, []);

  const derivedOutcome = useMemo<CommandOutcome | null>(() => {
    if (!lastIntent) {
      return null;
    }
    const linkedCommand =
      recentCommands.find(
        (record) =>
          (lastIntent.commandMsgId !== null && record.msg_id === lastIntent.commandMsgId) || record.corr_id === lastIntent.corrId,
      ) ?? null;
    const auditCorrId = lastIntent.commandMsgId ?? linkedCommand?.msg_id ?? null;
    const matchingEvent =
      recentEvents.find((record) => record.type === "audit" && auditCorrId !== null && record.corr_id === auditCorrId) ?? null;
    if (!matchingEvent) {
      const elapsedMs = Date.now() - lastIntent.sentAtMs;
      const timedOut = elapsedMs > lastIntent.timeoutMs;
      return {
        status: "dispatched",
        title: timedOut ? `${lastIntent.label}: нет подтверждения` : `${lastIntent.label}: отправлено`,
        detail: timedOut
          ? `Команда опубликована, но за ${lastIntent.timeoutMs} мс не пришёл audit-результат от edge. Считать её неподтверждённой, пока не появится accepted/rejected evidence.`
          : "Backend опубликовал команду. Теперь ждите audit-результат от edge, который подтвердит accepted или rejected.",
      };
    }
    const result = String(matchingEvent.payload?.result ?? "");
    if (result === "accepted") {
      return {
        status: "accepted",
        title: `${lastIntent.label}: принято`,
        detail: humanizeReason(matchingEvent.payload?.reason ?? "manual_command_accepted"),
      };
    }
    if (result === "rejected") {
      return {
        status: "rejected",
        title: `${lastIntent.label}: отклонено`,
        detail: humanizeReason(matchingEvent.payload?.reason),
      };
    }
    return {
      status: "dispatched",
      title: `${lastIntent.label}: отправлено`,
      detail: `Последнее связанное событие: ${humanizeEnum(matchingEvent.type)}.`,
    };
  }, [lastIntent, recentCommands, recentEvents]);

  const lastOutcome = lastImmediateOutcome ?? derivedOutcome;

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
      setLastIntent({
        corrId,
        commandMsgId: receipt.msg_id ?? null,
        label: `Команда режима ${humanizeEnum(mode)}`,
        timeoutMs: timeoutForCommand("mode"),
        sentAtMs: Date.now(),
      });
      setLastImmediateOutcome(null);
      setError(null);
    } catch (err) {
      setLastDispatch(null);
      setLastIntent(null);
      const detail = describeDispatchError(err);
      setLastImmediateOutcome(buildRejectedOutcome(`Команда режима ${humanizeEnum(mode)}`, detail));
      setError(detail);
    }
  }, []);

  const sendManual = useCallback(async (linear: number, angular: number) => {
    const corrId = buildCorrId("ui-manual");
    try {
      const receipt = await backendApi.sendManual(linear, angular, 500, corrId);
      setLastDispatch(receipt);
      setLastIntent({
        corrId,
        commandMsgId: receipt.msg_id ?? null,
        label: "Ручное движение",
        timeoutMs: timeoutForCommand("manual"),
        sentAtMs: Date.now(),
      });
      setLastImmediateOutcome(null);
      setError(null);
    } catch (err) {
      setLastDispatch(null);
      setLastIntent(null);
      const detail = describeDispatchError(err);
      setLastImmediateOutcome(buildRejectedOutcome("Ручное движение", detail));
      setError(detail);
    }
  }, []);

  const sendReset = useCallback(async (action: string, state: string) => {
    const corrId = buildCorrId("ui-reset");
    try {
      const receipt = await backendApi.sendReset(action, state, corrId);
      setLastDispatch(receipt);
      setLastIntent({
        corrId,
        commandMsgId: receipt.msg_id ?? null,
        label: "Команда сброса",
        timeoutMs: timeoutForCommand("reset"),
        sentAtMs: Date.now(),
      });
      setLastImmediateOutcome(null);
      setError(null);
    } catch (err) {
      setLastDispatch(null);
      setLastIntent(null);
      const detail = describeDispatchError(err);
      setLastImmediateOutcome(buildRejectedOutcome("Команда сброса", detail));
      setError(detail);
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
