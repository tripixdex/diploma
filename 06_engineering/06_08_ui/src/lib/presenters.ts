import type { BackendRecord, LiveFrame } from "@/lib/types";

type Tone = "neutral" | "info" | "success" | "warning" | "critical";

export type HumanSummary = {
  title: string;
  summary: string;
  detail: string;
  tone: Tone;
};

export type StateStory = {
  stateLabel: string;
  modeLabel: string;
  explanation: string;
  nextStep: string;
};

const REASON_LABELS: Record<string, string> = {
  heartbeat_lost: "Связь с контуром управления потеряна.",
  link_degraded: "Связь прервалась, поэтому система ушла в безопасный деградированный режим.",
  invalid_command: "Команда не соответствует текущему контракту.",
  illegal_transition: "Такой переход между состояниями сейчас запрещён.",
  manual_command_accepted: "Ручная команда принята и обработана.",
  manual_command_outside_manual_mode: "Ручное движение разрешено только в режиме MANUAL.",
  manual_command_blocked_by_safety: "Ручное движение заблокировано логикой безопасности.",
  unsupported_mode_request: "Запрошенный режим не поддерживается в этом MVP.",
  unsupported_operator_request: "Команда не поддерживается операторским контуром.",
  unsupported_reset_action: "Такой тип сброса не поддерживается текущим контрактом.",
  mode_request_not_allowed_in_current_state: "Режим нельзя менять из текущего состояния.",
  clear_safe_stop: "Запрошена попытка снять safe stop.",
};

function startCaseToken(value: string): string {
  return value
    .toLowerCase()
    .split(/[_\s-]+/)
    .filter(Boolean)
    .map((part) => part[0].toUpperCase() + part.slice(1))
    .join(" ");
}

export function humanizeEnum(value: string | null | undefined): string {
  if (!value) {
    return "Unknown";
  }
  if (value === "AUTO_LINE") return "Auto line";
  if (value === "SAFE_STOP") return "Safe stop";
  if (value === "ESTOP_LATCHED") return "Emergency stop latched";
  if (value === "DISCONNECTED_DEGRADED") return "Disconnected / degraded";
  return startCaseToken(value);
}

export function humanizeReason(value: unknown): string {
  if (typeof value !== "string" || value.length === 0) {
    return "Причина не указана.";
  }
  return REASON_LABELS[value] ?? `${startCaseToken(value)}.`;
}

export function describeState(state: string | null | undefined, mode: string | null | undefined): StateStory {
  const normalizedState = state ?? "UNAVAILABLE";
  const normalizedMode = mode ?? "UNKNOWN";

  switch (normalizedState) {
    case "IDLE":
      return {
        stateLabel: "Готов к команде",
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Система запущена, связи активны, движение сейчас не выполняется.",
        nextStep: "Выберите режим работы и отправьте команду mode.",
      };
    case "MANUAL":
      return {
        stateLabel: "Ручное управление активно",
        modeLabel: "Manual",
        explanation: "Оператор может отправлять небольшие ручные команды движения и сразу наблюдать результат.",
        nextStep: "Отправьте короткую manual-команду и смотрите события, телеметрию и live updates.",
      };
    case "AUTO_LINE":
      return {
        stateLabel: "Автоматический режим активен",
        modeLabel: "Auto line",
        explanation: "Система находится в автоматическом режиме движения по линии внутри software-only MVP.",
        nextStep: "Наблюдайте статус и события; ручная команда здесь не является основной.",
      };
    case "SAFE_STOP":
      return {
        stateLabel: "Движение остановлено безопасно",
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Логика безопасности заблокировала движение. Сначала нужно понять причину остановки.",
        nextStep: "Проверьте последний alert/event и только затем пробуйте reset path, если контракт это допускает.",
      };
    case "ESTOP_LATCHED":
      return {
        stateLabel: "Аварийный стоп зафиксирован",
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Сработал аварийный стоп. Нормальная работа продолжаться не должна.",
        nextStep: "На software-only демо это только индикация. В hardware phase потребуется подтверждённая процедура сброса.",
      };
    case "DISCONNECTED_DEGRADED":
      return {
        stateLabel: "Связь потеряна, режим деградации",
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Heartbeat или link supervision перестали подтверждаться, поэтому система ограничила поведение.",
        nextStep: "Наблюдайте alert и ждите восстановления связи; не ожидайте нормального движения до восстановления контура.",
      };
    case "FAULT":
      return {
        stateLabel: "Обнаружена ошибка",
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Система зарегистрировала fault и больше не считает контур нормальным.",
        nextStep: "Сначала посмотрите последний event/fault, затем переходите к диагностике причины.",
      };
    default:
      return {
        stateLabel: humanizeEnum(normalizedState),
        modeLabel: humanizeEnum(normalizedMode),
        explanation: "Статус получен, но для этого состояния ещё нет отдельного человеко-понятного сценария.",
        nextStep: "Проверьте события и live updates, чтобы понять последнее действие системы.",
      };
  }
}

export function summarizeRecord(record: BackendRecord): HumanSummary {
  if (record.type === "audit") {
    const result = String(record.payload?.result ?? "unknown");
    const requestedMode = record.payload?.requested_mode;
    const reason = record.payload?.reason;
    return {
      title: result === "accepted" ? "Команда принята" : result === "rejected" ? "Команда отклонена" : "Проверка команды",
      summary:
        typeof requestedMode === "string"
          ? `Запрошен режим ${humanizeEnum(requestedMode)}`
          : humanizeReason(reason),
      detail: humanizeReason(reason),
      tone: result === "accepted" ? "success" : result === "rejected" ? "warning" : "info",
    };
  }

  if (record.type === "alarm") {
    return {
      title: "Предупреждение безопасности",
      summary: humanizeReason(record.payload?.reason),
      detail: `Состояние: ${humanizeEnum(record.state)}. Режим: ${humanizeEnum(record.mode)}.`,
      tone: record.severity === "critical" ? "critical" : "warning",
    };
  }

  if (record.type === "fault") {
    return {
      title: "Ошибка контура",
      summary: humanizeReason(record.payload?.reason),
      detail: "Backend получил fault-сообщение от edge-контура.",
      tone: "critical",
    };
  }

  if (record.category === "command") {
    return {
      title: "Команда отправлена",
      summary: `Источник: ${record.source}. Целевое состояние: ${humanizeEnum(record.state)}.`,
      detail:
        typeof record.payload?.requested_mode === "string"
          ? `Запрошенный режим: ${humanizeEnum(String(record.payload.requested_mode))}.`
          : "Команда зафиксирована backend-слоем и ждёт реакцию edge.",
      tone: "info",
    };
  }

  if (record.category === "telemetry") {
    return {
      title: "Снимок телеметрии",
      summary: `Линейная: ${String(record.payload?.linear ?? "n/a")}, угловая: ${String(record.payload?.angular ?? "n/a")}.`,
      detail: `Получено в состоянии ${humanizeEnum(record.state)}.`,
      tone: "neutral",
    };
  }

  return {
    title: humanizeEnum(record.type),
    summary: `Состояние ${humanizeEnum(record.state)}, режим ${humanizeEnum(record.mode)}.`,
    detail: humanizeReason(record.payload?.reason ?? record.payload?.result),
    tone: "neutral",
  };
}

export function summarizeLiveFrame(frame: LiveFrame): HumanSummary {
  const type = String(frame.type ?? "");
  if (type === "ws_status") {
    return {
      title: "Live stream подключён",
      summary: "Backend WebSocket активен и передаёт свежие обновления.",
      detail: "Теперь новые события и статусы должны появляться без ручного refresh.",
      tone: "success",
    };
  }
  if (type === "ws_keepalive") {
    return {
      title: "Keepalive",
      summary: "Соединение живо, новых доменных событий в этом кадре нет.",
      detail: "Это служебный heartbeat кадр WebSocket.",
      tone: "info",
    };
  }
  if (typeof frame.category === "string") {
    return summarizeRecord(frame as unknown as BackendRecord);
  }
  return {
    title: "Сырое live-сообщение",
    summary: "Кадр не распознан как status/event/command/telemetry.",
    detail: "Откройте debug details, если нужно увидеть полный JSON.",
    tone: "neutral",
  };
}
