FROM python:3.7-alpine3.8

WORKDIR /app

EXPOSE 8000

RUN apk add --update alpine-sdk linux-headers gnupg

RUN pip install --user pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
COPY .python-version /app

RUN /root/.local/bin/pipenv install

COPY .env app.py hbbackend /app/

CMD ["/root/.local/bin/pipenv", "run", "python", "app.py"]
