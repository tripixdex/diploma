# CODEx Audit Report

## 1. Executive Summary

- Репозиторий фактически является не product/software-репозиторием, а рабочим архивом НИРС -> ВКР по теме цифровой модернизации `AGV Denford`.
- Фактическая зрелость: сильная документальная и источниковая база, слабая подтвержденная инженерная реализация в самом репозитории.
- На базе репозитория можно строить ВКР, но только если честно позиционировать текущий статус как `архитектура + первичные техдоки + НИРС + заготовка ВКР`, а не как уже реализованную `edge + cloud` систему.
- Главный технический актив: первичные материалы по `AGV Denford` и старой Denford/CIM-инфраструктуре, плюс уже собранный НИРС с архитектурой `Raspberry Pi + MQTT + сервер`.
- Главный технический дефицит: отсутствуют подтвержденные собственные `edge`-код, `MQTT`-обмен, backend, UI, конфиги стенда и результаты испытаний.

## 2. Repository Inventory

| Path | Type | Purpose | VERIFIED / INFERRED / MISSING VALUE | Relevance to VKR |
|---|---|---|---|---|
| `README.md` | Markdown | Корневой навигатор по новой структуре репозитория | VERIFIED | Medium |
| `03_nirs/final/НИРС_Итоговый_Основная_часть_v5_ужато_форматированием_FIXED_removed.pdf` | PDF | Основной содержательный результат НИРС | VERIFIED | High |
| `03_nirs/final/НИРС_Приложение_А_Рисунки_v1_FIXED.pdf` | PDF | Графическая база НИРС: IDEF0, схема, алгоритмы | VERIFIED | High |
| `03_nirs/intermediate/Промежуточный отчет ... AGV Denford.pdf` | PDF | Более ранний аналитический материал с расширенным обзором вариантов | VERIFIED | Medium |
| `03_nirs/source_docx/*` | DOCX | Исходники НИРС и рабочие версии документов | VERIFIED | Medium |
| `04_vkr/01_outline/vkr_concept_passport.md` | Markdown | Концепт паспорта ВКР, цели, гипотеза, ожидаемый результат | VERIFIED | High |
| `04_vkr/01_outline/nirs_to_vkr_matrix.md` | Markdown | Gap-analysis между НИРС и ВКР | VERIFIED | High |
| `04_vkr/02_rpz/vkr_writing_plan.md` | Markdown | План заполнения разделов ВКР | VERIFIED | High |
| `04_vkr/02_rpz/vkr_minimum_scope.md` | Markdown | Формулировка минимально достаточного объема ВКР | VERIFIED | High |
| `04_vkr/00_drafts/РПЗ_ВКР_AGV_Cloud_Draft.docx` | DOCX | Черновик пояснительной записки ВКР | VERIFIED | Medium |
| `05_sources/README.md` | Markdown | Карта источников и указание опорных первичных материалов | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/AGV Manual.pdf` | PDF | Первичный manual по AGV Denford, подтверждает исходный объект | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/Инструкция по запуску системы (Редакция 6).pdf` | PDF | Порядок запуска лаборатории ГПС, включая робокар | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/описание подключений.pdf` | PDF | Краткая схема линий/портов и заметка про интерфейсные платы/Raspberry Pi | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/РПЗ Зубков Разработка серверной части системы управления ГПС.pdf` | PDF | Смежная ВКР по серверной части ГПС, не текущая реализация | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../Agv.ini` | INI | Исторические конфиги старой Denford/CIM-инфраструктуры AGV | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../AGV.log` | Logs | Исторические логи старой системы AGV/CIM | VERIFIED | Medium |
| `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../Фото/*.jpg` | Images | Фотографии AGV и стенда | VERIFIED | High |
| `05_sources/05_00_raw_knowledge_base/Подборка КП и ВКР /2021/Григорьев (Ток.ГПМ)/Программы/*.py` | Python | Чужие/смежные скрипты для GPIO/serial на Raspberry Pi | VERIFIED | Medium |
| `05_sources/05_00_raw_knowledge_base/Подборка КП и ВКР /2021/Масный (Склад)/Warehouse/*` | C# project | Чужой/смежный проект с `MQTTnet` и Yandex Cloud | VERIFIED | Medium |
| `05_sources/05_01_primary_denford` | Directory | Должен содержать curated первичные материалы, сейчас пуст | MISSING VALUE | High |
| `05_sources/05_02_secondary_research` | Directory | Должен содержать curated вторичные исследования, сейчас пуст | MISSING VALUE | Medium |
| `05_sources/05_03_related_theses` | Directory | Должен содержать curated смежные ВКР, сейчас пуст | MISSING VALUE | Medium |
| `06_engineering/06_01_hardware` | Directory | Должен содержать hardware-проектирование, сейчас фактически пуст | MISSING VALUE | High |
| `06_engineering/06_02_software` | Directory | Должен содержать собственный software stack, сейчас фактически пуст | MISSING VALUE | High |
| `06_engineering/06_03_protocols_and_interfaces` | Directory | Должен содержать спецификации интерфейсов/MQTT, сейчас пуст | MISSING VALUE | High |
| `06_engineering/06_04_testing` | Directory | Должен содержать испытания, сейчас пуст | MISSING VALUE | High |
| `07_media/07_01_images` | Directory | Должен содержать рабочие изображения/схемы, сейчас пуст | MISSING VALUE | Medium |
| `07_media/07_02_diagrams` | Directory | Должен содержать схемы/диаграммы, сейчас пуст | MISSING VALUE | High |
| `07_media/07_03_presentations` | Directory | Должен содержать материалы защиты, сейчас пуст | MISSING VALUE | Medium |
| `08_obsidian_vault/03_Sources/AGV_Manual.md` | Markdown | Краткая карточка первичного источника | VERIFIED | Medium |
| `08_obsidian_vault/04_Denford_System/AGV_Denford.md` | Markdown | Краткое описание объекта автоматизации | VERIFIED | Medium |
| `08_obsidian_vault/04_Denford_System/Denstep.md` | Markdown | Краткая заметка по старому контроллеру | VERIFIED | Medium |
| `08_obsidian_vault/05_Engineering/MQTT_Interface.md` | Markdown | Намерение формализовать MQTT-интерфейс, без реализации | VERIFIED | High |
| `10_tools/document_formatting/fix_nirs.py` | Python | Авторский утилитарный код для правки `.docx` оформления | VERIFIED | Low |
| `10_tools/document_formatting/fix_nirs_v5.py` | Python | Улучшенная версия утилиты форматирования `.docx` | VERIFIED | Low |
| `report.md` | Markdown | Внутренний аналитический обзор репозитория | VERIFIED | Medium |
| `09_archive/*` | Archive | Сырые/старые/дублированные материалы, часть мусора и legacy | VERIFIED | Low |

## 3. Implemented Components

### Edge / onboard control

- Что найдено:
  - В `03_nirs` и `04_vkr` подробно описан целевой бортовой контур на `Raspberry Pi`.
  - В `05_sources/05_00_raw_knowledge_base/описание подключений.pdf` есть заметка про платы `4вх/4вых + E-stop` и фраза, что два устройства ГПМ могут управляться одним `Raspberry Pi`.
  - В `05_sources/.../Григорьев (Ток.ГПМ)/Программы/TestGPIOonly.py` есть смежный пример GPIO-кода на Raspberry Pi.
- Чем подтверждено:
  - `03_nirs/final/НИРС_...pdf`
  - `05_sources/05_00_raw_knowledge_base/описание подключений.pdf`
  - `05_sources/05_00_raw_knowledge_base/Подборка КП и ВКР /2021/Григорьев (Ток.ГПМ)/Программы/TestGPIOonly.py`
- Степень готовности:
  - Для текущего проекта как собственной реализации: `NOT VERIFIED`.
  - Как архитектурный замысел и внешние референсы: `VERIFIED`.
- Что не доказано:
  - Нет собственного edge-кода управления AGV.
  - Нет GPIO mapping текущего прототипа.
  - Нет схемы интерфейсной платы.
  - Нет исполняемого onboard service, systemd/unit, setup, requirements.

### MQTT / transport

- Что найдено:
  - `MQTT` последовательно выбран как базовый транспорт в НИРС и планах ВКР.
  - Есть заметка `08_obsidian_vault/05_Engineering/MQTT_Interface.md`, но она описывает только то, что должно быть формализовано.
  - В сыром архиве есть смежный C# проект `Warehouse` с зависимостью `MQTTnet` и кодом для Yandex Cloud.
- Чем подтверждено:
  - `03_nirs/final/НИРС_...pdf`
  - `08_obsidian_vault/05_Engineering/MQTT_Interface.md`
  - `05_sources/.../Warehouse/Warehouse/packages.config`
  - `05_sources/.../Warehouse/Warehouse/YaClass.cs`
- Степень готовности:
  - Для текущего проекта как собственной реализации: `NOT VERIFIED`.
  - Как обоснованный выбранный протокол и наличие смежных примеров: `VERIFIED`.
- Что не доказано:
  - Нет таблицы MQTT-топиков.
  - Нет схемы payload/ACK/QoS.
  - Нет брокера, docker-compose, mosquitto config, paho client, тестовых publish/subscribe-скриптов.

### Server / backend

- Что найдено:
  - Есть смежная ВКР Зубкова по серверной части ГПС.
  - В планах ВКР текущего проекта серверный контур фигурирует как обязательная часть архитектуры.
- Чем подтверждено:
  - `05_sources/05_00_raw_knowledge_base/РПЗ Зубков Разработка серверной части системы управления ГПС.pdf`
  - `04_vkr/01_outline/vkr_concept_passport.md`
- Степень готовности:
  - Собственный backend текущего проекта: `NOT VERIFIED`.
  - Наличие теоретической и смежной базы: `VERIFIED`.
- Что не доказано:
  - Нет исходников backend.
  - Нет API, БД, схемы хранения, брокера, deployment-конфигов.
  - Нет серверных логов именно текущего прототипа.

### Telemetry / storage

- Что найдено:
  - Телеметрия и журналирование описаны как целевые функции cloud-контура.
  - В исторических Denford/CIM-архивах есть старые `AGV.log` и другие логи.
- Чем подтверждено:
  - `03_nirs/final/НИРС_...pdf`
  - `05_sources/.../TechDoc от Ненашева/.../AGV.log`
- Степень готовности:
  - Телеметрия именно текущего `edge + cloud` решения: `NOT VERIFIED`.
  - Историческое наличие логирования в legacy-системе: `VERIFIED`.
- Что не доказано:
  - Нет формата телеметрии.
  - Нет хранилища данных.
  - Нет примеров собранной телеметрии текущего прототипа.

### Operator UI

- Что найдено:
  - UI постоянно упоминается в целевой архитектуре и планах.
  - В текущем репозитории нет собственного web UI, desktop UI или даже mockup-а именно под AGV Denford.
  - Смежный `Warehouse`-проект содержит WinForms UI, но относится к другой работе.
- Чем подтверждено:
  - `03_nirs/final/НИРС_...pdf`
  - `04_vkr/02_rpz/vkr_minimum_scope.md`
  - `05_sources/.../Warehouse/Warehouse/Form1.cs`
- Степень готовности:
  - Собственный UI текущего проекта: `NOT VERIFIED`.
  - Наличие смежных UI-референсов: `VERIFIED`.
- Что не доказано:
  - Нет экрана оператора.
  - Нет веб-панели.
  - Нет командного интерфейса текущего прототипа.

### Safety logic

- Что найдено:
  - В НИРС и планах ВКР repeatedly фиксируется принцип: критическая безопасность должна оставаться локально на борту.
  - В `описание подключений.pdf` и legacy `Agv.ini` есть упоминания `E-Stop` и `safety bit`.
  - В промежуточном отчете есть описание аппаратного E-Stop и реакции на потерю связи как целевого решения.
- Чем подтверждено:
  - `03_nirs/intermediate/Промежуточный отчет ... AGV Denford.pdf`
  - `05_sources/05_00_raw_knowledge_base/описание подключений.pdf`
  - `05_sources/.../Agv.ini`
- Степень готовности:
  - Формулировка требований и архитектурный принцип: `VERIFIED`.
  - Реально реализованная safety logic текущего прототипа: `NOT VERIFIED`.
- Что не доказано:
  - Нет схемы цепи E-Stop текущей модернизации.
  - Нет таблицы safe states.
  - Нет верифицированных сценариев `obstacle / estop / loss_link`.

### Tests / scripts

- Что найдено:
  - Есть авторские Python-скрипты форматирования `.docx` в `10_tools/document_formatting`.
  - Есть смежные/архивные испытательные и эксплуатационные материалы Denford/CIM в сыром архиве.
  - Раздел `06_engineering/06_04_testing` пуст.
- Чем подтверждено:
  - `10_tools/document_formatting/fix_nirs.py`
  - `10_tools/document_formatting/fix_nirs_v5.py`
  - `05_sources/.../Final Testing Procedures/Testing AGV.doc`
  - `05_sources/.../AGV.log`
- Степень готовности:
  - Авторские инженерные тесты текущего прототипа: `NOT VERIFIED`.
  - Служебные скрипты по документам: `VERIFIED`.
  - Исторические испытательные артефакты старой системы: `VERIFIED`.
- Что не доказано:
  - Нет unit/integration tests.
  - Нет smoke tests MQTT/broker.
  - Нет протоколов испытаний текущей модернизации.

## 4. Evidence for VKR

### Основа технического проектирования

- `03_nirs/final/НИРС_Итоговый_Основная_часть_v5_ужато_форматированием_FIXED_removed.pdf`
- `03_nirs/final/НИРС_Приложение_А_Рисунки_v1_FIXED.pdf`
- `05_sources/05_00_raw_knowledge_base/AGV Manual.pdf`
- `05_sources/05_00_raw_knowledge_base/Инструкция по запуску системы (Редакция 6).pdf`
- `05_sources/05_00_raw_knowledge_base/описание подключений.pdf`
- `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../Agv.ini`

### Основа рабочего проектирования

- `04_vkr/02_rpz/vkr_minimum_scope.md`
- `04_vkr/02_rpz/vkr_writing_plan.md`
- `04_vkr/01_outline/nirs_to_vkr_matrix.md`
- `03_nirs/intermediate/Промежуточный отчет ... AGV Denford.pdf`
- `05_sources/05_00_raw_knowledge_base/РПЗ Зубков Разработка серверной части системы управления ГПС.pdf`
- `05_sources/05_00_raw_knowledge_base/Подборка КП и ВКР /2021/Григорьев (Ток.ГПМ)/Программы/TestGPIOonly.py`
- `05_sources/05_00_raw_knowledge_base/Подборка КП и ВКР /2021/Масный (Склад)/Warehouse/Warehouse/YaClass.cs`

### Доказательство реализации

- `10_tools/document_formatting/fix_nirs.py`
- `10_tools/document_formatting/fix_nirs_v5.py`
- `03_nirs/final/НИРС_Итоговый_Основная_часть_v5_ужато_форматированием_FIXED_removed.pdf`

Примечание: это доказательство реализации документального и исследовательского контура, а не полноценной реализации `AGV edge + cloud`.

### Доказательство испытаний

- Исторические артефакты старой системы:
  - `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../Final Testing Procedures/Testing AGV.doc`
  - `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../AGV.log`
  - `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/.../dispatch.log`

Примечание: это не доказательство испытаний вашей модернизации. Для текущей ВКР их можно использовать только как фон/референс.

### Приложение

- `03_nirs/final/НИРС_Приложение_А_Рисунки_v1_FIXED.pdf`
- `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/AGV (тележка)/Фото/*.jpg`
- `05_sources/05_00_raw_knowledge_base/AGV Manual.pdf`

### Графическая часть

- `03_nirs/final/НИРС_Приложение_А_Рисунки_v1_FIXED.pdf`
- Фото AGV из `05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/AGV (тележка)/Фото/`
- Схемные и конфигурационные материалы из `AGV Manual.pdf` и `описание подключений.pdf`

## 5. Critical Gaps

### Чего не хватает для сильной ВКР

- Собственного подтвержденного `edge`-кода.
- Формализованной спецификации `MQTT`-топиков и сообщений.
- Собственного backend/server-контура.
- Собственного операторского интерфейса.
- Реальной hardware-схемы модернизации.
- Наполненного раздела `06_engineering`.

### Чего не хватает для честной демонстрации работоспособности

- Пошагового сценария запуска прототипа.
- Конфигов брокера и клиента.
- Логов обмена командами/телеметрией текущего прототипа.
- Фото/видео фактической сборки.
- Файлов окружения, зависимостей и воспроизводимой сборки.

### Чего не хватает для раздела испытаний

- Матрицы тест-кейсов.
- Таблиц expected/actual.
- Сценариев `manual`, `auto`, `obstacle`, `estop`, `loss_link`.
- Артефактов испытаний: скриншоты, логи, телеметрия, таблицы, выводы.

### Чего не хватает для аппаратной части

- Электрической схемы подключения.
- Таблицы сигналов вход/выход.
- Описания интерфейсной платы.
- Спецификации питания `Raspberry Pi` и исполнительных цепей.
- Перечня датчиков/приводов с фактическим подключением к новому контуру.

## 6. Minimal Defensible VKR Scope

Минимально достаточный контур, который реально можно довести до защиты без расползания темы:

- `AGV Denford` как `legacy`-объект с подтвержденным `as is` состоянием по первичным Denford-докам.
- Бортовой прототип на `Raspberry Pi`, который:
  - принимает команды `manual start/stop/left/right` или их упрощенный эквивалент;
  - публикует базовый статус;
  - переходит в safe state при `estop` или `loss_link`.
- `MQTT` как единственный транспорт без обязательного `ROS2`.
- Минимальный server contour:
  - брокер;
  - логирование команд и статусов;
  - простейший операторский интерфейс или CLI-панель.
- Набор честных испытаний:
  - connect to broker;
  - command delivery;
  - telemetry publish;
  - estop reaction;
  - loss_link reaction.

Это уже достаточно для сильной ВКР, если все перечисленное будет подтверждено файлами, схемами, логами и таблицами испытаний.

## 7. Recommended Next Actions

1. Немедленно заполнить `06_engineering` реальными артефактами: схемы, код, конфиги, тесты.
2. Зафиксировать `MQTT`-спецификацию: топики, payload, QoS, ACK, safe-state при потере связи.
3. Собрать минимальный воспроизводимый прототип `Raspberry Pi + broker + operator client`.
4. Сформировать таблицу I/O для AGV и схему подключения интерфейсной платы.
5. Провести и задокументировать 5-7 сценариев испытаний с логами и фото/видео.
6. Перенести опорные первичные материалы из сырого архива в `05_01_primary_denford`.
7. Отделить в тексте ВКР собственную реализацию от смежных/чужих референсов.
8. Не заявлять backend/UI/telemetry как реализованные, пока не появятся соответствующие файлы и артефакты.

## 8. Verification Log

### Какие команды запускались

- `pwd`
- `rg --files`
- `find . -maxdepth 2 -type d | sort`
- `find 06_engineering -maxdepth 4 \( -type f -o -type d \) | sort`
- `find 07_media -maxdepth 3 \( -type f -o -type d \) | sort`
- `find 08_obsidian_vault -maxdepth 3 \( -type f -o -type d \) | sort`
- `rg --files -g '*.py' -g '*.js' -g '*.ts' -g '*.tsx' -g '*.go' -g '*.rs' -g '*.sh' -g 'Dockerfile*' -g 'docker-compose*' -g '*.yml' -g '*.yaml' -g '*.json' -g '*.toml' -g '*.ini' -g '*.ipynb' -g '*.env*'`
- `rg -n -S "mqtt|raspberry|raspberry pi|ros2|edge|cloud|telemetry|dashboard|ui|backend|broker|mosquitto|paho|fastapi|flask|django|web|telemetr|лог|испыт|test|docker|docker-compose" ...`
- `sed -n '1,220p' ...` по ключевым `.md`, `.py`, `.cs`, `.ini`
- `find 03_nirs -maxdepth 2 -type f | sort`
- `find 04_vkr -maxdepth 3 -type f | sort`
- `find 05_sources -maxdepth 2 -type f | sort`
- `find . \( -iname '*test*' -o -iname '*log*' -o -iname '*.log' -o -iname '*mqtt*' ... \) | sort`
- `git log --oneline --decorate --max-count=5`
- `git status --short`
- `find 05_sources/05_00_raw_knowledge_base -type f | wc -l`
- `find '05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/Technical manuals' -type f | wc -l`
- `find '05_sources/05_00_raw_knowledge_base/TechDoc от Ненашева/Technical manuals 2' -type f | wc -l`
- Python one-liner для подсчета пересечения путей `Technical manuals` / `Technical manuals 2`
- Python с `pypdf` для проверки PDF и извлечения текста из:
  - `AGV Manual.pdf`
  - `Инструкция по запуску системы (Редакция 6).pdf`
  - `описание подключений.pdf`
  - `РПЗ Зубков ... .pdf`
  - `03_nirs/final/*.pdf`
  - `03_nirs/intermediate/*.pdf`

### Какие файлы открывались

- `README.md`
- `03_nirs/README.md`
- `04_vkr/README.md`
- `05_sources/README.md`
- `04_vkr/01_outline/nirs_to_vkr_matrix.md`
- `04_vkr/01_outline/vkr_concept_passport.md`
- `04_vkr/02_rpz/vkr_minimum_scope.md`
- `04_vkr/02_rpz/vkr_writing_plan.md`
- `08_obsidian_vault/00_Dashboard.md`
- `08_obsidian_vault/01_Project/Project_Status.md`
- `08_obsidian_vault/03_Sources/AGV_Manual.md`
- `08_obsidian_vault/04_Denford_System/AGV_Denford.md`
- `08_obsidian_vault/04_Denford_System/Denstep.md`
- `08_obsidian_vault/05_Engineering/MQTT_Interface.md`
- `10_tools/document_formatting/fix_nirs.py`
- `10_tools/document_formatting/fix_nirs_v5.py`
- `report.md`
- `05_sources/.../Agv.ini`
- `05_sources/.../TestGPIOonly.py`
- `05_sources/.../StringSendWork.py`
- `05_sources/.../Warehouse/Warehouse/packages.config`
- `05_sources/.../Warehouse/Warehouse/Form1.cs`
- `05_sources/.../Warehouse/Warehouse/YaClass.cs`

### Что не удалось проверить

- Работоспособность `AGV` как физического стенда: нет доступа к оборудованию.
- Реальное выполнение `edge + cloud` контура: в репозитории нет подтвержденной собственной реализации.
- Содержимое части бинарных `.doc/.docx/.cdr/.dwg/.eps` файлов проверялось только косвенно по именам и структуре, без полноценного визуального разбора.
- Исторические логи и test procedures из сырого архива не верифицировались как относящиеся к текущей ВКР.

## VERIFIED

- Есть сильная база первичных Denford-материалов.
- Есть зрелый НИРС с архитектурой `edge + cloud`.
- Есть каркас ВКР и ясный gap-analysis.
- Есть смежные/исторические материалы по Raspberry Pi, MQTT, серверной части и legacy Denford/CIM.
- Есть утилитарный авторский код по автоматизации оформления документов.

## INFERRED

- Репозиторий готовился как инженерно-документационный хаб для доведения темы до ВКР.
- Часть замысла по `Raspberry Pi + MQTT + server` уже интеллектуально оформлена и может быть быстро доведена до защищаемого прототипа.
- Смежные работы Зубкова/Григорьева/Масного, вероятно, предполагаются как доноры инженерных решений.

## NOT VERIFIED

- Собственный `edge`-код управления AGV.
- Собственный `MQTT`-обмен текущего проекта.
- Собственный backend/server.
- Собственный UI.
- Собственная телеметрия/хранилище.
- Испытания текущей модернизации.
- Физическая сборка прототипа и ее работоспособность.

## DO NOT CLAIM IN VKR

- Не заявлять, что `Raspberry Pi + MQTT + cloud` уже реализованы, если это не подтверждено кодом, конфигами, схемами и логами.
- Не заявлять наличие рабочего backend или web UI.
- Не использовать исторические `AGV.log`, `Testing AGV.doc` и чужие проекты как доказательство собственной апробации.
- Не выдавать смежные студенческие скрипты и C#-проекты из сырого архива за часть текущей реализации.
- Не утверждать наличие завершенного рабочего проектирования: в репозитории оно пока в основном планируется, а не реализовано.
