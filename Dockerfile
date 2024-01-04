FROM python:3-alpine3.15
WORKDIR /app
COPY . /app/
RUN apk update && apk upgrade
RUN apk add musl-dev gcc python3-dev build-base linux-headers
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./app.py