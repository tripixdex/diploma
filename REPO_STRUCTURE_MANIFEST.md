# Repo Structure Manifest

## Active Structure

### Active engineering zone
- `06_engineering/06_00_contract/` — действующий системный контракт V1.
- `06_engineering/06_01_sim_twin/` — действующий functional twin и Stage 2 evidence.
- `06_engineering/06_02_edge/` — hardware-agnostic edge MVP.
- `06_engineering/06_03_transport/` — локальный MQTT transport contour.
- `06_engineering/06_04_backend/` — backend MVP с MQTT ingest, REST и WebSocket.
- `06_engineering/06_05_operator/` — минимальный operator-facing contour.
- `06_engineering/06_06_integration/` — repeatable software-only integration evidence и freeze artifacts.
- `06_engineering/06_07_polish/` — polished demo package и pre-hardware preparation docs.
- `06_engineering/06_08_ui/` — human UI для software-only MVP.
- `06_engineering/06_01_hardware/` — hardware survey zone; hardware-specific runtime пока не является источником реализованной логики.
- `06_engineering/06_02_software/`, `06_engineering/06_03_server/`, `06_engineering/06_04_testing/`, `06_engineering/06_05_deployment/` — legacy placeholder zones; не считать их текущим source of truth без отдельных evidenced artifacts.

### Reports
- `99_reports/execution/` — stage-by-stage execution reports.
- `99_reports/audit/` — репозиторные аудиты и выборки по фактическому состоянию.
- `99_reports/planning/` — рабочие планы и операционные planning-документы.

### References and supporting material
- `01_admin/` — административные шаблоны и чеклисты.
- `02_methodology/` — методические и нормативные материалы.
- `05_sources/` — источники и технические референсы.
- `07_media/` — изображения, схемы, презентационные материалы.
- `08_obsidian_vault/` — knowledge base и заметки.
- `10_tools/` — служебные инструменты по документам и вспомогательным операциям.

## Archive / Legacy / Diploma History

- `03_nirs/` — завершенный НИРС и его история.
- `04_vkr/` — история и текущие черновики ВКР-текста.
- `09_archive/` — raw dump, legacy versions, duplicates, старый административный контекст.

## Root Policy

- Корень репозитория должен содержать только короткие верхнеуровневые entrypoint-документы.
- Активные рабочие markdown-файлы нельзя оставлять в корне, если им подходит зона `06_engineering/` или `99_reports/`.
- Аудиты и временные выводы по состоянию проекта должны попадать в `99_reports/audit/`.
- Операционные планы и meta-документы по ведению проекта должны попадать в `99_reports/planning/`.

## Moved Active Files

- `goal.md` -> `99_reports/planning/PROJECT_MASTER_GOAL.md`
- `reorg_and_vkr_plan.md` -> `99_reports/planning/REPOSITORY_REORG_AND_VKR_PLAN.md`
- `AGV_PROJECT_IMPLEMENTATION_FILES.md` -> `99_reports/audit/AGV_PROJECT_IMPLEMENTATION_FILES_AUDIT.md`
- `CODEx_AUDIT_REPORT.md` -> `99_reports/audit/CODEX_REPOSITORY_AUDIT_REPORT.md`

## File Placement Rules

### Put files into `06_engineering/06_00_contract/` when
- документ фиксирует границы системы, state model, I/O, MQTT contract или acceptance logic;
- документ меняет инженерный контракт, а не историю проекта.

### Put files into `06_engineering/06_01_sim_twin/` when
- файл относится к functional twin, сценариям twin, локальному demo, in-memory publish flow или twin evidence.

### Put files into `99_reports/execution/` when
- документ описывает ход stage, gate status, validation, readiness to close.

### Put files into `99_reports/audit/` when
- документ проводит инвентаризацию, hygiene-аудит, hardcode/modularity audit или доказательное обследование репозитория.

### Put files into `99_reports/planning/` when
- документ задает рабочую дисциплину, roadmap, reorg-план, meta-goal, но не является contract doc.

### Do not move aggressively when
- документ относится к `03_nirs/`, `04_vkr/` или `09_archive/`;
- есть риск сломать исторические ссылки и контекст дипломной истории.
