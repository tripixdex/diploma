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

function outcomeLabel(status: CommandOutcome["status"] | undefined) {
  if (status === "accepted") return "принято";
  if (status === "rejected") return "отклонено";
  if (status === "dispatched") return "отправлено";
  return "нет данных";
}

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
        <CardDescription>Операторский контур управления</CardDescription>
        <CardTitle>Отправка команд по шагам</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Шаг 1. Выберите режим</div>
          <div className="text-sm text-muted-foreground">Сначала выберите, в каком режиме система должна работать до любых команд движения.</div>
          <div className="flex gap-3">
            <select
              className="h-10 flex-1 rounded-xl border border-input bg-white/85 px-3 text-sm"
              value={mode}
              onChange={(event) => setMode(event.target.value)}
            >
              <option value="MANUAL">MANUAL / Ручной</option>
              <option value="AUTO_LINE">AUTO_LINE / Автолиния</option>
              <option value="UNSUPPORTED_MODE">Неподдерживаемый режим для проверки отказа</option>
            </select>
            <Button onClick={() => void onMode(mode)}>
              <SendHorizontal className="mr-2 h-4 w-4" />
              Отправить режим
            </Button>
          </div>
          <div className="text-xs text-muted-foreground">
            Текущее состояние по контракту: <span className="font-semibold text-foreground">{humanizeEnum(currentStatus?.state)}</span>
          </div>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Шаг 2. Отправьте ручное движение</div>
          <div className="text-sm text-muted-foreground">
            Используйте только после перехода системы в <span className="font-semibold text-foreground">MANUAL</span>.
          </div>
          <div className="grid grid-cols-2 gap-3">
            <Input value={linear} onChange={(event) => setLinear(event.target.value)} placeholder="Линейная скорость, м/с" />
            <Input value={angular} onChange={(event) => setAngular(event.target.value)} placeholder="Угловая скорость, рад/с" />
          </div>
          <div className="grid grid-cols-2 gap-3 text-xs text-muted-foreground">
            <div>Рекомендованное demo-значение: `0.15 м/с`</div>
            <div>Рекомендованное demo-значение: `0.00 рад/с`</div>
          </div>
          <Button className="w-full" variant="secondary" onClick={() => void onManual(Number(linear), Number(angular))}>
            Отправить ручное движение
          </Button>
        </div>

        <div className="space-y-3">
          <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">Шаг 3. Контур сброса</div>
          <div className="text-sm text-muted-foreground">
            Используйте только когда контракт и текущее состояние явно разрешают попытку восстановления.
          </div>
          <Button
            className="w-full"
            variant="outline"
            onClick={() => void onReset("clear_safe_stop", currentStatus?.state ?? "IDLE")}
          >
            <RotateCcw className="mr-2 h-4 w-4" />
            Попробовать clear_safe_stop
          </Button>
        </div>

        <div className="rounded-2xl bg-secondary/60 p-4 text-sm">
          <div className="flex flex-wrap items-center gap-2">
            <div className="font-semibold text-foreground">Последний итог команды</div>
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
              {outcomeLabel(lastOutcome?.status)}
            </Badge>
          </div>
          <div className="mt-2 text-sm text-foreground">
            {lastOutcome?.title ?? "Команда ещё не отправлялась."}
          </div>
          <div className="mt-1 text-sm text-muted-foreground">{lastOutcome?.detail ?? "Начните с mode-команды, чтобы запустить операторский сценарий."}</div>
          <div className="mt-4 border-t border-border/70 pt-3">
            <div className="font-semibold text-foreground">Квитанция публикации</div>
            <div className="mt-2 text-xs text-muted-foreground">
              `отправлено` означает только то, что backend опубликовал команду. `принято` или `отклонено` решает edge-логика позже.
            </div>
            <details className="mt-2">
              <summary className="cursor-pointer text-xs font-semibold text-primary">Показать сырую квитанцию</summary>
              <pre className="mt-2 overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-white/80 p-3 font-mono text-xs text-muted-foreground">
                {lastDispatch ? JSON.stringify(lastDispatch, null, 2) : "Публикации ещё не было."}
              </pre>
            </details>
          </div>
          <div className="mt-3 text-xs text-muted-foreground">
            Типовые причины отклонения: {humanizeReason("manual_command_outside_manual_mode")} {humanizeReason("unsupported_mode_request")}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
