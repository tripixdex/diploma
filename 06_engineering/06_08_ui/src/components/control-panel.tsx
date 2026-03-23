import { useState } from "react";
import { RotateCcw, SendHorizontal } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { BackendRecord, CommandReceipt } from "@/lib/types";
import { humanizeEnum, humanizeReason } from "@/lib/presenters";

type CommandOutcome = {
  status: "idle" | "dispatched" | "accepted" | "rejected";
  title: string;
  detail: string;
};

export function ControlPanel({
  currentStatus,
  lastDispatch,
  lastOutcome,
  onMode,
  onManual,
  onReset,
}: {
  currentStatus: BackendRecord | null;
  lastDispatch: CommandReceipt | { published: false; topic: string; payload: string; qos: number; retain: false } | null;
  lastOutcome: CommandOutcome | null;
  onMode: (mode: string) => Promise<void>;
  onManual: (linear: number, angular: number) => Promise<void>;
  onReset: (action: string, state: string) => Promise<void>;
}) {
  const [mode, setMode] = useState("MANUAL");
  const [linear, setLinear] = useState("0.15");
  const [angular, setAngular] = useState("0.00");

  return (
    <Card className="h-full min-w-0">
      <CardHeader>
        <CardDescription>Operator controls</CardDescription>
        <CardTitle>Send commands step by step</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 1. Choose system mode</div>
          <div className="text-sm text-muted-foreground">Pick how the robot should behave before sending any motion command.</div>
          <div className="flex gap-3">
            <select
              className="h-10 flex-1 rounded-xl border border-input bg-white/85 px-3 text-sm"
              value={mode}
              onChange={(event) => setMode(event.target.value)}
            >
              <option value="MANUAL">MANUAL</option>
              <option value="AUTO_LINE">AUTO_LINE</option>
              <option value="UNSUPPORTED_MODE">UNSUPPORTED_MODE</option>
            </select>
            <Button onClick={() => void onMode(mode)}>
              <SendHorizontal className="mr-2 h-4 w-4" />
              Send mode
            </Button>
          </div>
          <div className="text-xs text-muted-foreground">
            Current contract state: <span className="font-semibold text-foreground">{humanizeEnum(currentStatus?.state)}</span>
          </div>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 2. Send manual motion</div>
          <div className="text-sm text-muted-foreground">
            Use only after the system has moved into <span className="font-semibold text-foreground">Manual</span>.
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Input value={linear} onChange={(event) => setLinear(event.target.value)} placeholder="Linear speed, m/s" />
            <Input value={angular} onChange={(event) => setAngular(event.target.value)} placeholder="Angular rate, rad/s" />
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs text-muted-foreground">
            <div>Suggested demo value: `0.15 m/s`</div>
            <div>Suggested demo value: `0.00 rad/s`</div>
          </div>
          <Button className="w-full" variant="secondary" onClick={() => void onManual(Number(linear), Number(angular))}>
            Send manual motion
          </Button>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Step 3. Reset path</div>
          <div className="text-sm text-muted-foreground">
            Use only when the contract and current state clearly allow a recovery attempt.
          </div>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => void onReset("clear_safe_stop", currentStatus?.state ?? "IDLE")}
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Try reset / clear safe stop
          </Button>
        </div>

        <div className="rounded-2xl bg-secondary/60 p-4 text-sm">
          <div className="flex flex-wrap items-center gap-2">
            <div className="font-semibold text-foreground">Latest command outcome</div>
            <Badge
              variant={
                lastOutcome?.status === "accepted"
                  ? "success"
                  : lastOutcome?.status === "rejected"
                    ? "warning"
                    : lastOutcome?.status === "dispatched"
                      ? "info"
                      : "neutral"
              }
            >
              {lastOutcome?.status ?? "idle"}
            </Badge>
          </div>
          <div className="mt-2 text-sm text-foreground">
            {lastOutcome?.title ?? "No command sent yet."}
          </div>
          <div className="mt-1 text-sm text-muted-foreground">{lastOutcome?.detail ?? "Send a mode command to begin the operator flow."}</div>
          <div className="mt-4 border-t border-border/70 pt-3">
            <div className="font-semibold text-foreground">Transport receipt</div>
            <div className="mt-2 text-xs text-muted-foreground">
              `dispatched` means the backend published the command. `accepted` or `rejected` is decided later by edge logic.
            </div>
            <details className="mt-2">
              <summary className="cursor-pointer text-xs font-semibold text-primary">Show raw publish receipt</summary>
              <pre className="mt-2 overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-white/80 p-3 font-mono text-xs text-muted-foreground">
                {lastDispatch ? JSON.stringify(lastDispatch, null, 2) : "No command published yet."}
              </pre>
            </details>
          </div>
          <div className="mt-3 text-xs text-muted-foreground">
            Common rejection reasons: {humanizeReason("manual_command_outside_manual_mode")} {humanizeReason("unsupported_mode_request")}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
