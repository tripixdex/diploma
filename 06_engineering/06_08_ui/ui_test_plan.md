# UI Test Plan

## Stage 7F Checks
- UI dev server успешно стартует.
- UI читает текущее состояние через backend REST.
- UI читает последние события, команды и телеметрию через backend REST.
- UI получает live-обновления через backend WebSocket.
- UI отправляет `mode`, `manual` и `reset` команды через backend REST.
- UI не выдаёт `accepted` только по факту dispatch; итог команды меняется только по audit/evidence path.
- Невалидные mode/manual/reset входы отклоняются backend-валидацией и это видно на основном экране.
- Основная поверхность экрана использует русский язык последовательно.
- Длинные live/debug сообщения не разрывают карточки и страницу по ширине.
- Затяжная потеря связи приводит не только к `DISCONNECTED_DEGRADED`, но и к последующему `SAFE_STOP`.

## Вне Scope
- pixel-perfect cross-browser QA;
- production asset pipeline hardening;
- authentication/authorization;
- hardware-phase UI behavior.

## Обязательная проверка перед closeout
- `ui_demo_stack.py` поднимает backend + broker + edge без ручной правки файлов.
- Vite UI стартует и отдаёт приложение.
- backend REST остаётся рабочим.
- backend WebSocket остаётся рабочим.
- Stage 7 integration runner проходит повторный запуск без ручной чистки порта.
- manual QA подтверждает, что новый пользователь понимает порядок действий без чтения backend docs.
