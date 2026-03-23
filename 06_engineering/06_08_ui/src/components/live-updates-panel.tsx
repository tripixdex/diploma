import { ActivitySquare } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { LiveFrame } from "@/lib/types";
import { summarizeLiveFrame } from "@/lib/presenters";

export function LiveUpdatesPanel({
  frames,
  wsState,
}: {
  frames: LiveFrame[];
  wsState: "connecting" | "live" | "idle";
}) {
  return (
    <Card className="h-full min-w-0 overflow-hidden">
      <CardHeader>
        <CardDescription>Короткие live-обновления с необязательными сырыми деталями</CardDescription>
        <CardTitle className="flex items-center gap-2">
          <ActivitySquare className="h-5 w-5 text-primary" />
          Живая активность
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 min-w-0">
        <Badge variant={wsState === "live" ? "success" : wsState === "connecting" ? "info" : "warning"}>
          {wsState === "live" ? "live" : wsState === "connecting" ? "подключение" : "idle"}
        </Badge>
        <div className="max-h-[32rem] space-y-3 overflow-y-auto pr-1">
          {frames.length === 0 ? (
            <div className="rounded-2xl bg-secondary/50 p-4 text-sm text-muted-foreground">Live-кадры ещё не получены.</div>
          ) : (
            frames.map((frame, index) => {
              const summary = summarizeLiveFrame(frame);
              return (
                <div
                  key={`${String(frame["msg_id"] ?? frame["type"] ?? "frame")}-${index}`}
                  className="min-w-0 rounded-2xl border border-white/70 bg-white/70 p-4"
                >
                  <div className="flex items-center gap-2">
                    <Badge
                      variant={
                        summary.tone === "success"
                          ? "success"
                          : summary.tone === "warning"
                            ? "warning"
                            : summary.tone === "critical"
                              ? "critical"
                              : summary.tone === "info"
                                ? "info"
                                : "neutral"
                      }
                    >
                      {String(frame["type"] ?? frame["category"] ?? "live")}
                    </Badge>
                    <div className="min-w-0 text-sm font-semibold text-foreground">{summary.title}</div>
                  </div>
                  <div className="mt-2 text-sm text-foreground">{summary.summary}</div>
                  <div className="mt-1 text-sm text-muted-foreground">{summary.detail}</div>
                  <details className="mt-3">
                    <summary className="cursor-pointer text-xs font-semibold text-primary">Показать сырой кадр</summary>
                    <pre className="mt-2 overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-slate-950 p-3 font-mono text-xs text-slate-100">
                      {JSON.stringify(frame, null, 2)}
                    </pre>
                  </details>
                </div>
              );
            })
          )}
        </div>
      </CardContent>
    </Card>
  );
}
