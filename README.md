# Greetings traveller

## В директории new_admin_panel_sprint_1 устанавливаем виртуальное окуружение:

python -m venv venv
source venv/bin/Activate
pip install -r requirements.txt

## Для запуска в катологи movies_admin/config , sqlite_to_postgres и tests/check_consistency
## необходимо положить файл .env.
## В файле movies_admin/config/.env необходимо указать параметры подключения и некоторые параметры Djnago приложения, пример:
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
DB_PORT=5432
DEBUG=True
SECRET_KEY=ll

## В файле sqlite_to_postgres/.env указываем параметры подключения:
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
DB_PORT=5432

## В файле tests/check_consistency/.env указываем параметры подключения:
DB_NAME=movies_database
DB_USER=app
DB_PASSWORD=123qwe
DB_PORT=5432

## Запуск тестов:
Переходим в директоию tests/check_consistency/ и запускаем pytest


Мы рады, что вы приступили к выполнению 1 задания из курса Middle Python-разработчик.
 
Описание структуры и порядок выполнения проекта:
1. `schema_design` - раздел c материалами для архитектуры базы данных.
2. `movies_admin` - раздел с материалами для панели администратора.
3. `sqlite_to_postgres` - раздел с материалами по миграции данных.

Напоминаем, что все три части работы нужно сдавать на ревью одновременно.

Успехов!
