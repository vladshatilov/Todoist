FROM python:3.10-slim
RUN apt update && apt install -y gcc libpq-dev
WORKDIR /code
COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code
CMD python manage.py runserver 0.0.0.0:8000