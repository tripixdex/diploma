import { Activity, ShieldAlert, Wifi } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { BackendHealth, BackendRecord } from "@/lib/types";

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
  const alertText = latestEvent ? `${latestEvent.type}: ${String(latestEvent.payload?.reason ?? latestEvent.payload?.result ?? "update")}` : "No active alert";

  return (
    <div className="grid gap-4 lg:grid-cols-[1.7fr,1fr]">
      <Card className="overflow-hidden">
        <CardHeader className="pb-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <CardDescription>AGV Denford Human UI</CardDescription>
              <CardTitle className="mt-1 text-3xl font-extrabold tracking-tight">{state}</CardTitle>
            </div>
            <Badge variant={wsState === "live" ? "success" : wsState === "connecting" ? "info" : "warning"}>
              {wsState === "live" ? "Live stream active" : wsState === "connecting" ? "Connecting" : "Stream idle"}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="grid gap-6 lg:grid-cols-3">
          <div className="rounded-2xl bg-slate-950 px-5 py-4 text-white">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-300">Mode</div>
            <div className="mt-2 text-2xl font-bold">{mode}</div>
          </div>
          <div className="rounded-2xl bg-white/70 px-5 py-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
              <Wifi className="h-4 w-4" />
              Backend links
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              <Badge variant={health?.mqtt_bridge_connected ? "success" : "warning"}>MQTT ingest</Badge>
              <Badge variant={health?.command_bridge_connected ? "success" : "warning"}>Command bridge</Badge>
              <Badge variant="neutral">{health?.storage_mode ?? "unknown storage"}</Badge>
            </div>
          </div>
          <div className="rounded-2xl bg-white/70 px-5 py-4">
            <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
              <ShieldAlert className="h-4 w-4" />
              Latest alert
            </div>
            <div className="mt-3 flex items-center gap-3">
              <Badge variant={severityVariant(latestEvent?.severity)}>{latestEvent?.severity ?? "stable"}</Badge>
              <div className="text-sm font-medium">{alertText}</div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardDescription>Frozen software-only MVP</CardDescription>
          <CardTitle className="flex items-center gap-2 text-xl">
            <Activity className="h-5 w-5 text-primary" />
            Honest demo contour
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm text-muted-foreground">
          <p>The UI reads backend truth, shows live updates, and sends minimal commands through the existing contract path.</p>
          <p>Rejected actions and degraded behavior remain visible instead of being hidden by frontend optimism.</p>
        </CardContent>
      </Card>
    </div>
  );
}
