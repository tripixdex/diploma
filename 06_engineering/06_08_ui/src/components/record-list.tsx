import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { BackendRecord } from "@/lib/types";

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
    <Card className="h-full">
      <CardHeader>
        <CardDescription>{description}</CardDescription>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        {records.length === 0 ? (
          <div className="rounded-2xl bg-secondary/50 p-4 text-sm text-muted-foreground">No records yet.</div>
        ) : (
          records.map((record) => (
            <div key={record.msg_id} className="rounded-2xl border border-white/70 bg-white/70 p-4">
              <div className="flex items-center justify-between gap-3">
                <div className="text-sm font-semibold">{record.type}</div>
                <Badge variant={badgeForSeverity(record.severity)}>{record.severity}</Badge>
              </div>
              <div className="mt-2 text-sm text-muted-foreground">
                state={record.state} mode={record.mode}
              </div>
              <div className="mt-2 break-all font-mono text-xs text-muted-foreground">
                {JSON.stringify(record.payload)}
              </div>
            </div>
          ))
        )}
      </CardContent>
    </Card>
  );
}
