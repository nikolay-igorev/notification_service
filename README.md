# Сервис рассылок

Сервис управления рассылками через внешний API и получения статистики.

### Документация

Документация: http://<your_domain>/docs/

### Docker

Чтобы запустить приложение с помощью Docker:

Создайте файл .env, скопируйте в него содержимое из .env.example и замените.
Замените JWT_TOKEN для внешнего API на свой токен.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://postgres:postgres@localhost:5432/postgres
DATABASE_URL_DOCKER=postgres://postgres:postgres@db:5432/postgres
JWT_TOKEN=token
API_URL=url
```

выполните команду:
```bash
docker-compose up -d --build
```

Запустите миграции, создайте суперпользователя:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Приложение будет доступно по адресу: `http://localhost:8000/`. 

Чтобы запустить тесты:

```bash
docker-compose exec web python manage.py test
```

Чтобы остановить все контейнеры:

```bash
docker-compose down
```

### Установка

Сначала установите Postgres и запустите его.
Установите Redis:
```bash
sudo apt update
sudo apt install redis
```

Создайте файл ```.env``` и скопируйте туда содержимое из ```.env.example```. Измените username, password и dbname для
DATABASE_URl на те, которые используются в вашем локальном Postgres. Замените JWT_TOKEN для внешнего API на свой токен.

```bash
SECRET_KEY=secret
DEBUG_MODE=True
DATABASE_URL=postgres://username:password@localhost:5432/dbname
JWT_TOKEN=token
```

Установите зависимости проекта с помощью pip и активируйте виртуальную среду:

```bash
python -m venv .venv 
```
```bash
.venv\Scripts\Activate.ps1 
```
```bash
pip install -r requirements.txt
```

После этого примените миграции, создайте суперюзера и запустите сервер:

```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver  
```
В другой консоли активировать виртуальную среду и запустить:
```bash
redis-server
python -m celery worker
```
Чтобы запустить тесты:
```bash
python manage.py test 
```
