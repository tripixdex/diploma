import { Activity, ShieldAlert, Wifi } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { BackendHealth, BackendRecord } from "@/lib/types";
import { describeState, humanizeEnum, summarizeRecord } from "@/lib/presenters";

function severityVariant(severity?: string) {
  if (severity === "critical") return "critical";
  if (severity === "warning") return "warning";
  return "info";
}

export function DashboardHeader({
  status,
  health,
  latestEvent,
  wsState,
}: {
  status: BackendRecord | null;
  health: BackendHealth | null;
  latestEvent: BackendRecord | null;
  wsState: "connecting" | "live" | "idle";
}) {
  const state = status?.state ?? "UNAVAILABLE";
  const mode = status?.mode ?? "UNKNOWN";
  const story = describeState(state, mode);
  const alertSummary = latestEvent ? summarizeRecord(latestEvent) : null;

  return (
    <div className="grid gap-4 lg:grid-cols-[1.7fr,1fr]">
      <Card className="min-w-0 overflow-hidden">
        <CardHeader className="pb-4">
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <CardDescription>AGV Denford Human UI</CardDescription>
              <CardTitle className="mt-1 text-3xl font-extrabold tracking-tight">{story.stateLabel}</CardTitle>
              <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">{story.explanation}</p>
            </div>
            <Badge variant={wsState === "live" ? "success" : wsState === "connecting" ? "info" : "warning"}>
              {wsState === "live" ? "Live stream active" : wsState === "connecting" ? "Connecting" : "Stream idle"}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl bg-slate-950 px-5 py-4 text-white">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-300">What is happening now</div>
            <div className="mt-2 text-2xl font-bold">{story.modeLabel}</div>
            <div className="mt-2 text-sm text-slate-300">{story.nextStep}</div>
          </div>
          <div className="rounded-2xl bg-white/70 px-5 py-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
              <Wifi className="h-4 w-4" />
              System links
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              <Badge variant={health?.mqtt_bridge_connected ? "success" : "warning"}>MQTT ingest</Badge>
              <Badge variant={health?.command_bridge_connected ? "success" : "warning"}>Command bridge</Badge>
              <Badge variant="neutral">{health?.storage_mode ?? "unknown storage"}</Badge>
            </div>
            <div className="mt-3 text-sm text-muted-foreground">
              Contract state: <span className="font-semibold text-foreground">{humanizeEnum(state)}</span>
            </div>
          </div>
          <div className="min-w-0 rounded-2xl bg-white/70 px-5 py-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
              <ShieldAlert className="h-4 w-4" />
              Latest important update
            </div>
            <div className="mt-3 flex items-center gap-3">
              <Badge variant={severityVariant(latestEvent?.severity)}>{latestEvent?.severity ?? "stable"}</Badge>
              <div className="min-w-0 text-sm font-medium">{alertSummary?.title ?? "System stable"}</div>
            </div>
            <div className="mt-2 text-sm text-muted-foreground">{alertSummary?.summary ?? "No active alert."}</div>
          </div>
        </CardContent>
      </Card>

      <Card className="min-w-0">
        <CardHeader>
          <CardDescription>How to use this screen</CardDescription>
          <CardTitle className="flex items-center gap-2 text-xl">
            <Activity className="h-5 w-5 text-primary" />
            Operator flow
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm text-muted-foreground">
          <p>1. Сначала посмотрите верхнюю карточку состояния, чтобы понять текущий режим и безопасно ли движение.</p>
          <p>2. Затем отправьте mode-команду. После этого смотрите, появилась ли отметка о принятии или отклонении.</p>
          <p>3. Только потом отправляйте manual motion и наблюдайте telemetry, events и live updates.</p>
        </CardContent>
      </Card>
    </div>
  );
}
