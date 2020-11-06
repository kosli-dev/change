FROM python:3.7-alpine

RUN apk update
#Needed for libgit2-dev
RUN apk add build-base cmake libffi-dev
RUN apk add libgit2-dev=1.0.0-r0
# Needed for file based sha
RUN apk add openssl

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY cdb/ cdb/
COPY tests/ tests/
ADD test_data/test_source_repo.tar.gz /

COPY coverage_entrypoint.sh .

ENV PYTHONPATH="/app"
ENTRYPOINT [""]
CMD ["python", "server.py"]
