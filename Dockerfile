FROM python:3.10-slim
RUN apt update
WORKDIR /code
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD python manage.py runserver 0.0.0.0:8000