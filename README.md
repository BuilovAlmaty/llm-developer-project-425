# AI-агент службы поддержки

[![hexlet-check](https://github.com/BuilovAlmaty/llm-developer-project-425/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/BuilovAlmaty/llm-developer-project-425/actions)

Help Desk-агент на Yandex AI Studio: почтовый агент (IMAP/SMTP) принимает обращения сотрудников, ищет ответы в корпоративной базе знаний (RAG), а при необходимости создаёт тикеты и сохраняет переписку в YDB Serverless. Проект предусматривает MCP-инструмент, workflow по расписанию, защиту от prompt injection и утечек персональных данных, а также наблюдаемость.

Учебный проект Хекслета: https://ru.hexlet.io/programs/llm-developer

## Стек

- **Yandex AI Studio / YandexGPT** — агент `help-desk` и Responses API.
- **Yandex Cloud IAM** — сервисный аккаунт `ai-studio-sa` и управление доступом.
- **Yandex Lockbox** — хранение параметров подключения и секретов.
- **YDB Serverless** — хранение тикетов и переписки (следующие этапы).
- **Cloud Functions, MCP Hub, Workflows** — почтовая интеграция, инструменты и фоновые задачи (следующие этапы).

## Установка

```bash
git clone https://github.com/BuilovAlmaty/llm-developer-project-425.git
cd llm-developer-project-425
```

### Настройка Yandex Cloud

Создан сервисный аккаунт `ai-studio-sa` с ролями:

- `functions.functionInvoker`
- `serverless.mcpGateways.invoker`
- `lockbox.payloadViewer`
- `ai.languageModels.user`
- `ydb.editor`

В Yandex Lockbox созданы секреты:

- `ydb-endpoint` — адрес подключения к YDB;
- `ydb-database` — путь к базе данных.

В Yandex AI Studio создан агент `help-desk` на базе YandexGPT. Идентификаторы агента, сервисного аккаунта и секретов указываются в локальном `.env`; значения секретов в репозитории не хранятся.

Пример переменных окружения (без секретных значений):

```dotenv
FOLDER_ID=
SA_ID=
AGENT_ID=
YDB_ENDPOINT_SECRET_ID=
YDB_DATABASE_SECRET_ID=
```

Авторизация Cloud Functions будет выполняться через сервисный аккаунт и временные IAM-токены.

## Использование

Пока агент `help-desk` доступен для тестирования в интерфейсе Yandex AI Studio. Почтовый канал, MCP-инструмент и RAG будут подключены на следующих этапах.

---

<details>
<summary>Автоматические тесты Хекслета</summary>

Тесты запускаются на каждый коммит. За запуск отвечает файл `.github/workflows/hexlet-check.yml` — не удаляйте и не переименовывайте ни его, ни репозиторий.

</details>

## О Хекслете

[Хекслет](https://ru.hexlet.io/) — школа программирования: авторские программы обучения с практикой, поддержкой наставников и реальными проектами, которые остаются в резюме. Этот репозиторий — один из таких проектов.
