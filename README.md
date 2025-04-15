# Restaurant Booking API

Простой RESTful API для управления столиками и бронированиями в ресторане, построенный с использованием FastAPI, SQLAlchemy (async), Alembic и PostgreSQL, работающий в Docker-контейнерах.

## Описание

Этот API предоставляет эндпоинты для:

*   Создания, получения списка, получения деталей и удаления столиков.
*   Создания, получения списка, получения деталей и удаления бронирований.
*   Автоматической проверки конфликтов при создании бронирования для предотвращения двойного бронирования столика на одно и то же время.

## Технологический Стек

*   **Веб-фреймворк:** [FastAPI](https://fastapi.tiangolo.com/)
*   **База данных:** [PostgreSQL](https://www.postgresql.org/) (версия 15 Alpine)
*   **ORM / Работа с БД:** [SQLAlchemy](https://www.sqlalchemy.org/) (с поддержкой asyncio)
*   **Драйвер БД:** [asyncpg](https://github.com/MagicStack/asyncpg)
*   **Миграции БД:** [Alembic](https://alembic.sqlalchemy.org/en/latest/)
*   **Валидация данных / Настройки:** [Pydantic](https://docs.pydantic.dev/) / [Pydantic-Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
*   **ASGI Сервер:** [Uvicorn](https://www.uvicorn.org/)
*   **Контейнеризация:** [Docker](https://www.docker.com/) / [Docker Compose](https://docs.docker.com/compose/)
*   **Язык:** Python 3.10+

## Возможности

*   Полностью асинхронная работа.
*   Автоматическая валидация данных запросов и ответов с помощью Pydantic.
*   Автоматическая интерактивная документация API (Swagger UI и ReDoc).
*   Управление схемой базы данных с помощью миграций Alembic.
*   Простая настройка и запуск с использованием Docker Compose.
*   Проверка конфликтов при бронировании.

## Предварительные Требования

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (обычно устанавливается вместе с Docker Desktop)

## Установка и Запуск

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <url-вашего-репозитория>
    cd New_T_T/restaurant_booking_api
    ```

2.  **Создайте файл `.env`:**
    В корневой директории проекта (`New_T_T/restaurant_booking_api`) создайте файл с именем `.env`. Этот файл будет содержать переменные окружения для конфигурации базы данных и приложения.

    Скопируйте и вставьте следующее содержимое в ваш `.env` файл, заменив значения `user` и `password` на желаемые учетные данные для PostgreSQL:

    ```.env
    # PostgreSQL Settings
    POSTGRES_USER=user         # Замените на ваше имя пользователя
    POSTGRES_PASSWORD=password   # Замените на ваш пароль
    POSTGRES_DB=restaurant_db
    POSTGRES_HOST=db           # Имя сервиса БД из docker-compose.yml
    POSTGRES_PORT=5432         # Внутренний порт контейнера БД

    # Полный URL для SQLAlchemy (Alembic и приложение его используют)
    # Этот URL будет использоваться приложением и Alembic для подключения к БД внутри Docker сети.
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
    ```

3.  **Соберите и запустите контейнеры:**
    Выполните команду в корневой директории проекта:
    ```bash
    docker-compose up --build
    ```
    *   `--build`: Эта опция пересобирает образ приложения, если вы внесли изменения в `Dockerfile` или код приложения (при первом запуске она обязательна).
    *   Эта команда скачает образ PostgreSQL, соберет образ для вашего FastAPI приложения, создаст и запустит оба контейнера (`db` и `app`).
    *   При запуске сервис `app` дождется готовности базы данных, применит миграции Alembic (`alembic upgrade head`) и запустит Uvicorn сервер.

4.  **Проверка работы:**
    *   API будет доступен по адресу: `http://localhost:8000`
    *   Интерактивная документация Swagger UI: `http://localhost:8000/docs`
    *   Альтернативная документация ReDoc: `http://localhost:8000/redoc`

## Миграции Базы Данных (Alembic)

Миграции используются для управления изменениями схемы базы данных по мере развития приложения.

*   **Применение миграций:** Миграции автоматически применяются при старте контейнера `app` благодаря команде `alembic upgrade head` в `docker-compose.yml`.
*   **Создание новой миграции:** Если вы изменили модели SQLAlchemy (в `app/models/`), вам нужно сгенерировать новый файл миграции:
    ```bash
    # Запустите эту команду из корневой папки проекта на вашем хосте
    docker-compose exec app alembic revision --autogenerate -m "Краткое описание изменений"
    ```
    Эта команда выполнит `alembic revision ...` внутри работающего контейнера `app`. Она сравнит текущее состояние моделей с состоянием базы данных и создаст новый файл миграции в `alembic/versions/`. Проверьте сгенерированный файл перед применением.
*   **Применение миграций вручную (если нужно):**
    ```bash
    # Запустите эту команду из корневой папки проекта на вашем хосте
    docker-compose exec app alembic upgrade head
    ```
*   **Откат миграции:**
    ```bash
    # Откатиться на одну миграцию назад
    docker-compose exec app alembic downgrade -1
    ```

## Тестирование

Проект включает набор интеграционных тестов, написанных с использованием `pytest` и `httpx`. Тесты проверяют основной функционал API эндпоинтов для столиков и бронирований.

**Запуск тестов:**

1.  **Убедитесь, что приложение запущено** с помощью `docker-compose up` (можно в фоновом режиме: `docker-compose up -d`). Тесты выполняются путем отправки реальных HTTP-запросов к работающему приложению внутри Docker-сети.

2.  Выполните следующую команду в **новом** терминале в корневой директории проекта (`New_T_T/restaurant_booking_api`):

    ```bash
    docker-compose exec app pytest app/tests
    ```

    *   `docker-compose exec app`: Выполняет команду внутри работающего контейнера `app`.
    *   `pytest app/tests`: Запускает `pytest`, указывая ему директорию с тестами внутри контейнера.

Вы увидите вывод `pytest`, показывающий результаты выполнения тестов.
    
## API Эндпоинты

Подробное описание всех эндпоинтов, параметров и схем доступно в интерактивной документации:

*   **Swagger UI:** `http://localhost:8000/docs`
*   **ReDoc:** `http://localhost:8000/redoc`

**Основные ресурсы:**

*   **Столики (`/tables`)**
    *   `POST /tables/`: Создать новый столик.
    *   `GET /tables/`: Получить список столиков.
    *   `GET /tables/{table_id}`: Получить детали столика по ID.
    *   `DELETE /tables/{table_id}`: Удалить столик по ID.
*   **Бронирования (`/reservations`)**
    *   `POST /reservations/`: Создать новое бронирование (с проверкой конфликтов).
    *   `GET /reservations/`: Получить список бронирований.
    *   `GET /reservations/{reservation_id}`: Получить детали бронирования по ID.
    *   `DELETE /reservations/{reservation_id}`: Удалить бронирование по ID.

## Переменные Окружения (`.env`)

*   `POSTGRES_USER`: Имя пользователя для базы данных PostgreSQL.
*   `POSTGRES_PASSWORD`: Пароль для пользователя PostgreSQL.
*   `POSTGRES_DB`: Имя базы данных PostgreSQL.
*   `POSTGRES_HOST`: Хост (имя сервиса Docker), где запущена база данных.
*   `POSTGRES_PORT`: Порт, который слушает PostgreSQL внутри контейнера.
*   `DATABASE_URL`: Полная строка подключения к базе данных в формате SQLAlchemy (`postgresql+asyncpg://...`), используемая приложением и Alembic. Может быть задана явно или будет сконструирована из отдельных компонентов `POSTGRES_*`, если не задана.

## Структура Проекта


restaurant_booking_api/

│ ├── app/ # Исходный код FastAPI приложения

│ │ ├── core/ # Конфигурация, подключение к БД

│ │ ├── models/ # Модели SQLAlchemy (ORM)

│ │ ├── routers/ # Обработчики API эндпоинтов

│ │ ├── schemas/ # Схемы Pydantic (валидация, сериализация)

│ │ ├── services/ # Бизнес-логика

│ │ └── main.py # Точка входа в приложение

│ ├── alembic/ # Конфигурация и скрипты Alembic

│ │ └── versions/ # Файлы миграций

│ ├── .env # Переменные окружения (локально)

│ ├── alembic.ini # Конфигурация Alembic

│ ├── docker-compose.yml # Конфигурация Docker Compose

│ ├── Dockerfile # Инструкции для сборки Docker-образа приложения

│ └── requirements.txt # Зависимости Python

└── README.md # Этот файл



## Остановка Приложения

Чтобы остановить контейнеры, нажмите `Ctrl+C` в терминале, где запущен `docker-compose up`. Чтобы удалить контейнеры и сеть (но сохранить том с данными БД):

```bash
docker-compose down

Чтобы удалить и том с данными ( ВНИМАНИЕ: все данные БД будут потеряны!):

docker-compose down -v



## Тестирование с Postman

Для удобства ручного тестирования API предоставляется коллекция Postman.

1.  Скачайте файл коллекции: `Restaurant_Booking_API.postman_collection.json`.
2.  Запустите приложение с помощью `docker-compose up`.
3.  Откройте Postman и импортируйте скачанный файл (`Import` -> `Upload Files`).
4.  В импортированной коллекции "Restaurant Booking API" уже настроена переменная `baseUrl` на `http://localhost:8000`.
5.  Вы можете выполнять запросы к эндпоинтам API. Для запросов, требующих ID (например, `/tables/:table_id`), не забудьте подставить актуальный ID в параметрах запроса (вкладка "Params" или непосредственно в URL) после создания соответствующего ресурса (столика или бронирования).
