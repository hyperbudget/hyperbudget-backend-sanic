FROM python:3.7-alpine3.8

WORKDIR /app

EXPOSE 8000

RUN apk add --update alpine-sdk linux-headers gnupg

RUN pip install --user pipenv

COPY Pipfile /app
COPY Pipfile.lock /app
COPY .python-version /app

RUN /root/.local/bin/pipenv install

COPY .env app.py /app/
COPY hbbackend /app/hbbackend

ENV PYTHONPATH=/app/:$PYTHONPATH

CMD PYTHONPATH=/app:$PYTHONPATH /root/.local/bin/pipenv run python app.py
