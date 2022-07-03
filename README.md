# ToDo app
## Description
The application allows you to manage tasks divided into boards and categories.
The boards are used to organize the sharing of tasks between users.

### Back - Python 3.10, Django, DRF, Postgres, JWT
### Front - Angular, Router

All endpoints can be viewed in swagger by running the application
Telegram bot [@TodoistSkybot](https://t.me/todoskybot ) to manage tasks via telegram.
How the bot works:
1. Send any message to initialize the bot
2. Send a repeat message to receive the authorization code
3. Enter the authorization code in the application or in swagger at the address `PATCH /bot/verify`
4. Using the bot, you can view and add new goals (goals)

#### Quick start: 
- Pull the repository 
>git clone https://github.com/vladshatilov/Todoist.git
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
- `docker-compose up --build -d`
##### Frontend will be on http://localhost
##### Backend: `python manage.py makemigrations`, `python manage.py migrate `
- Load fixtures: `python manage.py loadall` 
- and finally: `python manage.py runserver`

##### P.S.
To launch the bot, you need to register your bot in Telegram via @BotFather.
Next, write the received token in .env to the BOT_TOKEN variable