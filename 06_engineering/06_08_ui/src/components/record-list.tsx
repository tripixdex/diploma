import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { BackendRecord } from "@/lib/types";
import { humanizeEnum, summarizeRecord } from "@/lib/presenters";

function badgeForSeverity(severity: string) {
  if (severity === "critical") return "critical";
  if (severity === "warning") return "warning";
  if (severity === "info") return "info";
  return "neutral";
}

export function RecordList({
  title,
  description,
  records,
}: {
  title: string;
  description: string;
  records: BackendRecord[];
}) {
  return (
    <Card className="h-full min-w-0 overflow-hidden">
      <CardHeader>
        <CardDescription>{description}</CardDescription>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {records.length === 0 ? (
          <div className="rounded-2xl bg-secondary/50 p-4 text-sm text-muted-foreground">No records yet.</div>
        ) : (
          records.map((record) => (
            <div key={record.msg_id} className="min-w-0 rounded-2xl border border-white/70 bg-white/70 p-4">
              {(() => {
                const summary = summarizeRecord(record);
                return (
                  <>
              <div className="flex items-center justify-between gap-3">
                <div className="min-w-0 text-sm font-semibold">{summary.title}</div>
                <Badge variant={badgeForSeverity(record.severity)}>{record.severity}</Badge>
              </div>
              <div className="mt-2 text-sm text-foreground">{summary.summary}</div>
              <div className="mt-1 text-sm text-muted-foreground">{summary.detail}</div>
              <div className="mt-2 text-xs text-muted-foreground">
                State: {humanizeEnum(record.state)}. Mode: {humanizeEnum(record.mode)}.
              </div>
              <details className="mt-3">
                <summary className="cursor-pointer text-xs font-semibold text-primary">Show raw details</summary>
                <pre className="mt-2 overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-secondary/55 p-3 font-mono text-xs text-muted-foreground">
                  {JSON.stringify(record.payload, null, 2)}
                </pre>
              </details>
                  </>
                );
              })()}
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
