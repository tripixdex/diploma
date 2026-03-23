import { RefreshCcw } from "lucide-react";

import { ControlPanel } from "@/components/control-panel";
import { DashboardHeader } from "@/components/dashboard-header";
import { LiveUpdatesPanel } from "@/components/live-updates-panel";
import { RecordList } from "@/components/record-list";
import { TelemetryPanel } from "@/components/telemetry-panel";
import { Button } from "@/components/ui/button";
import { useDashboard } from "@/hooks/use-dashboard";

export default function App() {
  const {
    health,
    currentStatus,
    recentEvents,
    recentCommands,
    recentTelemetry,
    liveFrames,
    wsState,
    lastDispatch,
    error,
    refresh,
    sendMode,
    sendManual,
    sendReset,
    lastOutcome,
  } = useDashboard();

  return (
    <main className="mx-auto max-w-7xl overflow-x-clip px-6 py-8">
      <div className="mb-8 flex items-center justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-[0.24em] text-muted-foreground">Stage 7F</p>
          <h1 className="mt-2 text-4xl font-extrabold tracking-tight">Операторский экран AGV Denford MVP</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
            Один экран для всего software-only контура: выберите режим, отправьте команду движения и сразу увидьте, была ли она только опубликована, принята или отклонена.
          </p>
        </div>
        <Button variant="outline" onClick={() => void refresh()}>
          <RefreshCcw className="mr-2 h-4 w-4" />
          Обновить снимок
        </Button>
      </div>

      <DashboardHeader
        status={currentStatus}
        health={health}
        latestEvent={recentEvents[0] ?? null}
        wsState={wsState}
      />

      {error ? (
        <div className="mt-6 rounded-2xl border border-critical/20 bg-critical/10 px-5 py-4 text-sm text-critical">
          {error}
        </div>
      ) : null}

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.1fr,1fr]">
        <ControlPanel
          currentStatus={currentStatus}
          lastDispatch={lastDispatch}
          lastOutcome={lastOutcome}
          onMode={sendMode}
          onManual={sendManual}
          onReset={sendReset}
        />
        <TelemetryPanel telemetry={recentTelemetry} />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1fr,1fr,1fr]">
        <RecordList title="Последние события" description="Audit, alarm и признаки деградации" records={recentEvents} />
        <RecordList title="Последние команды" description="Команды, которые backend увидел на входе" records={recentCommands} />
        <LiveUpdatesPanel frames={liveFrames} wsState={wsState} />
      </div>
    </main>
  );
}
