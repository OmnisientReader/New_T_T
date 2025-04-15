#!/bin/bash

# Название корневой папки проекта
PROJECT_ROOT_DIR="restaurant_booking_api"

# --- Создание корневой папки проекта ---
echo "Creating project root directory: ${PROJECT_ROOT_DIR}"
mkdir -p "${PROJECT_ROOT_DIR}"
cd "${PROJECT_ROOT_DIR}" || exit # Переходим в папку проекта или выходим, если не удалось

# --- Создание основных файлов и папок в корне ---
echo "Creating root files and directories..."
touch .env.example
touch .gitignore
touch Dockerfile
touch README.md
touch alembic.ini
touch docker-compose.yml
touch requirements.txt

mkdir -p app
mkdir -p alembic/versions # Папка для версий миграций
mkdir -p app/tests        # Папка для тестов

# --- Создание структуры внутри папки 'app' ---
echo "Creating structure inside 'app' directory..."
touch app/__init__.py
touch app/main.py

mkdir -p app/core
touch app/core/__init__.py
touch app/core/config.py
touch app/core/database.py

mkdir -p app/models
touch app/models/__init__.py
touch app/models/base.py
touch app/models/table.py
touch app/models/reservation.py

mkdir -p app/schemas
touch app/schemas/__init__.py
touch app/schemas/table.py
touch app/schemas/reservation.py

mkdir -p app/services
touch app/services/__init__.py
touch app/services/table.py
touch app/services/reservation.py

mkdir -p app/routers
touch app/routers/__init__.py
touch app/routers/table.py
touch app/routers/reservation.py

# --- Создание структуры внутри папки 'alembic' ---
# Alembic init обычно создает env.py и script.py.mako,
# создадим их пустыми для полноты структуры
echo "Creating structure inside 'alembic' directory..."
touch alembic/env.py
touch alembic/script.py.mako
# Создадим пустой файл в versions, чтобы git отслеживал папку (необязательно)
touch alembic/versions/.gitkeep

# --- Создание структуры внутри папки 'app/tests' ---
echo "Creating structure inside 'app/tests' directory..."
touch app/tests/__init__.py
touch app/tests/conftest.py # Файл для pytest фикстур
touch app/tests/test_tables.py
touch app/tests/test_reservations.py

# --- Завершение ---
echo "--------------------------------------"
echo "Project structure created successfully in '${PROJECT_ROOT_DIR}' directory."
echo "Use 'tree' command (if installed) to view the structure:"
echo "cd ${PROJECT_ROOT_DIR} && tree"
echo "--------------------------------------"

# Возвращаемся в исходный каталог (необязательно)
# cd ..

exit 0
