import { ActivitySquare } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { LiveFrame } from "@/lib/types";

export function LiveUpdatesPanel({
  frames,
  wsState,
}: {
  frames: LiveFrame[];
  wsState: "connecting" | "live" | "idle";
}) {
  return (
    <Card className="h-full">
      <CardHeader>
        <CardDescription>Live WebSocket updates</CardDescription>
        <CardTitle className="flex items-center gap-2">
          <ActivitySquare className="h-5 w-5 text-primary" />
          Stream panel
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <Badge variant={wsState === "live" ? "success" : wsState === "connecting" ? "info" : "warning"}>{wsState}</Badge>
        <div className="space-y-3">
          {frames.length === 0 ? (
            <div className="rounded-2xl bg-secondary/50 p-4 text-sm text-muted-foreground">No live frames received yet.</div>
          ) : (
            frames.map((frame, index) => (
              <div key={`${String(frame["msg_id"] ?? frame["type"] ?? "frame")}-${index}`} className="rounded-2xl bg-slate-950 px-4 py-3 font-mono text-xs text-slate-100">
                {JSON.stringify(frame)}
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}
