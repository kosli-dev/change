FROM python:3.7-alpine

RUN apk update
#Needed for libgit2-dev
RUN apk add build-base cmake libffi-dev
RUN apk add libgit2-dev=1.0.0-r0
# Needed for file based sha
RUN apk add openssl
# Needed to install approval tests from git egg
RUN apk add git

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY cdb/ cdb/
COPY tests/ tests/
COPY integration_tests/ integration_tests/
ADD test_data/test_source_repo.tar.gz /

COPY unit_coverage_entrypoint.sh .
COPY integration_coverage_entrypoint.sh .

ENV PYTHONPATH="/app"
ENTRYPOINT [""]
CMD ["python", "server.py"]
