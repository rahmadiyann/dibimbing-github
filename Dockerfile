FROM python:3.8-slim-buster

ARG MYNAME="Rian"
ARG PORT=8000

WORKDIR /app

COPY . /app

EXPOSE $PORT

RUN pip install -r requirements.txt

CMD ["python", "app.py"]