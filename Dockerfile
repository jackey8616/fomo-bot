FROM python:3.13-slim

LABEL maintainer=clooooode<clode@clo5de.info>

WORKDIR /app

EXPOSE 8090

VOLUME ["/app/.env"]

COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["python3", "src/main.py", "--env-file-path", ".env"]