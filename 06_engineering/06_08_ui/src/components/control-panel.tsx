import { useState } from "react";
import { RotateCcw, SendHorizontal } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import type { BackendRecord, CommandReceipt } from "@/lib/types";

export function ControlPanel({
  currentStatus,
  lastDispatch,
  onMode,
  onManual,
  onReset,
}: {
  currentStatus: BackendRecord | null;
  lastDispatch: CommandReceipt | { published: false; topic: string; payload: string; qos: number; retain: false } | null;
  onMode: (mode: string) => Promise<void>;
  onManual: (linear: number, angular: number) => Promise<void>;
  onReset: (action: string, state: string) => Promise<void>;
}) {
  const [mode, setMode] = useState("MANUAL");
  const [linear, setLinear] = useState("0.15");
  const [angular, setAngular] = useState("0.00");

  return (
    <Card className="h-full">
      <CardHeader>
        <CardDescription>Operator controls</CardDescription>
        <CardTitle>Send minimal commands</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Mode command</div>
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
              Send
            </Button>
          </div>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Manual command</div>
          <div className="grid grid-cols-2 gap-3">
            <Input value={linear} onChange={(event) => setLinear(event.target.value)} placeholder="Linear" />
            <Input value={angular} onChange={(event) => setAngular(event.target.value)} placeholder="Angular" />
          </div>
          <Button className="w-full" variant="secondary" onClick={() => void onManual(Number(linear), Number(angular))}>
            Send manual motion
          </Button>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Reset path</div>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => void onReset("clear_safe_stop", currentStatus?.state ?? "IDLE")}
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Send reset / clear safe stop
          </Button>
        </div>

        <div className="rounded-2xl bg-secondary/60 p-4 text-sm">
          <div className="font-semibold text-foreground">Last dispatch receipt</div>
          <div className="mt-2 break-all font-mono text-xs text-muted-foreground">
            {lastDispatch ? JSON.stringify(lastDispatch) : "No command published yet."}
          </div>
          <div className="mt-2 text-xs text-muted-foreground">
            Publish receipt is not the same as contract acceptance. Rejections appear in events/live updates.
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
