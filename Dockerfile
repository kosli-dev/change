FROM python:3.7-alpine

RUN apk update

WORKDIR /app/cdb
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY cdb/ .

ENTRYPOINT [""]
CMD ["python", "server.py"]

