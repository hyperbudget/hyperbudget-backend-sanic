FROM python:3.7-alpine3.8

WORKDIR /app

EXPOSE 8000

RUN apk add --update alpine-sdk linux-headers gnupg

RUN pip install --user pipenv

COPY . /app

RUN /root/.local/bin/pipenv install

CMD ["/root/.local/bin/pipenv", "run", "python", "app.py"]
