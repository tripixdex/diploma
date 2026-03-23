import { Gauge, Route } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { BackendRecord } from "@/lib/types";

export function TelemetryPanel({ telemetry }: { telemetry: BackendRecord[] }) {
  const latest = telemetry[0];
  return (
    <Card className="h-full">
      <CardHeader>
        <CardDescription>Telemetry snapshot</CardDescription>
        <CardTitle>Latest motion evidence</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {latest ? (
          <>
            <div className="grid gap-3 md:grid-cols-2">
              <div className="rounded-2xl bg-slate-950 px-5 py-4 text-white">
                <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-slate-300">
                  <Gauge className="h-4 w-4" />
                  Linear
                </div>
                <div className="mt-2 text-2xl font-bold">{String(latest.payload.linear ?? "n/a")}</div>
              </div>
              <div className="rounded-2xl bg-white/70 px-5 py-4">
                <div className="flex items-center gap-2 text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  <Route className="h-4 w-4" />
                  Angular
                </div>
                <div className="mt-2 text-2xl font-bold">{String(latest.payload.angular ?? "n/a")}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="info">{latest.state}</Badge>
              <span className="text-sm text-muted-foreground">{latest.ts}</span>
            </div>
          </>
        ) : (
          <div className="rounded-2xl bg-secondary/50 p-4 text-sm text-muted-foreground">No telemetry observed yet.</div>
        )}
      </CardContent>
    </Card>
  );
}
