FROM python:3.7-alpine3.8

WORKDIR /app

COPY . /app

RUN apk add --update alpine-sdk linux-headers gnupg

RUN pip install --user pipenv
RUN /root/.local/bin/pipenv install

EXPOSE 8000

CMD ["/root/.local/bin/pipenv", "run", "python", "app.py"]
