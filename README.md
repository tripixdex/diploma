# Diploma Workspace

Этот репозиторий содержит архивную дипломную историю и активный инженерный контур проекта `AGV Denford`.

Главное честное состояние на сейчас: здесь доказан `software-only MVP`, а не hardware-ready контур.

## Куда смотреть в первую очередь

- [TOP_LEVEL_TRUTH_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/TOP_LEVEL_TRUTH_BASELINE.md)
- [SOFTWARE_RUNTIME_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_RUNTIME_BASELINE.md)
- [MASTER_EXECUTION_REPORT.md](/Users/vladgurov/Desktop/study/7sem/diploma/99_reports/execution/MASTER_EXECUTION_REPORT.md)
- [SYSTEM_SCOPE.md](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_00_contract/SYSTEM_SCOPE.md)
- [RELEASE_MANIFEST.md](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_06_integration/release_manifest.md)
- [MVP_FREEZE_MANIFEST.md](/Users/vladgurov/Desktop/study/7sem/diploma/06_engineering/06_07_polish/mvp_freeze_manifest.md)
- [REPO_STRUCTURE_MANIFEST.md](/Users/vladgurov/Desktop/study/7sem/diploma/REPO_STRUCTURE_MANIFEST.md)

## Что реально есть

- Единый Python packaging/dependency baseline в [pyproject.toml](/Users/vladgurov/Desktop/study/7sem/diploma/pyproject.toml).
- Единый software-only setup/run baseline в [SOFTWARE_RUNTIME_BASELINE.md](/Users/vladgurov/Desktop/study/7sem/diploma/SOFTWARE_RUNTIME_BASELINE.md).
- Контракт системы в `06_engineering/06_00_contract/`.
- Functional twin в `06_engineering/06_01_sim_twin/`.
- Hardware-agnostic edge MVP в `06_engineering/06_02_edge/`.
- Реальный локальный MQTT transport в `06_engineering/06_03_transport/`.
- Backend MVP с `FastAPI`, MQTT ingest, dev/demo storage, REST и WebSocket в `06_engineering/06_04_backend/`.
- Operator path и human UI для software-only demo в `06_engineering/06_05_operator/` и `06_engineering/06_08_ui/`.
- Repeatable integration evidence и polished demo package в `06_engineering/06_06_integration/` и `06_engineering/06_07_polish/`.

## Что нельзя заявлять

- Что Webots уже реализован и доказан.
- Что PostgreSQL уже внедрён и проверен как текущий runtime storage path.
- Что Docker Compose deployment уже существует и валидирован.
- Что Mosquitto deployment уже доказан как deployment baseline.
- Что есть hardware readiness, Raspberry Pi binding или доказанная безопасность на реальном AGV.

## Верхнеуровневая структура

- `03_nirs` — завершённый НИРС и его история.
- `04_vkr` — история и текущие черновики ВКР-текста.
- `05_sources` — база источников и технических референсов.
- `06_engineering` — активная инженерная зона software-only MVP.
- `07_media` — схемы, изображения и презентационные материалы.
- `09_archive` — старые, сырые и второстепенные материалы.
- `99_reports` — execution reports, audits и planning artifacts.
