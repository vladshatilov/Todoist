### ToDo app
#### Back - Python 3.10, Django, DRF, Postgres, JWT
#### Front - React, Router

#### Quick start: 
- Create .env and fill it with 
- DB_HOST=localhost
- POSTGRES_NAME=<base_name>
- DB_PORT=5432
- POSTGRES_USER=<user>
- POSTGRES_PASSWORD=<password>
- DB_ENGINE=django.db.backends.engine
- DB_NAME=<db_name>
- DB_USER=<db_user>
- DB_PASSWORD=<db_pass>
- Step into market-postgres
- `docker-compose up --build -d`
##### Frontend will be on http://localhost:3000
##### Backend: `python manage.py makemigrations`, `python manage.py migrate `
- Load fixtures: `python manage.py loadall` 
- and finally: `python manage.py runserver`