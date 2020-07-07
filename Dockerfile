FROM python:3.7-alpine

RUN apk update

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY cdb/ cdb/
COPY tests/ tests/

COPY coverage_entrypoint.sh .

ENTRYPOINT [""]
CMD ["python", "server.py"]

