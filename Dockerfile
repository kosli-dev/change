FROM python:3.7-alpine

RUN apk update
#Needed for libgit2-dev
RUN apk add build-base cmake libffi-dev
RUN apk add libgit2-dev=1.1.0-r1

# Needed for file based sha
RUN apk add openssl
# Needed to install approval tests from git egg. See requirements.txt
RUN apk add git

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ARG IMAGE_COMMIT_SHA
ENV IMAGE_SHA=${IMAGE_COMMIT_SHA}

COPY tests/ tests/
ADD tests/data/test_source_repo.tar.gz /

COPY cdb/ cdb/
COPY commands commands/
COPY env_vars env_vars/
COPY fingerprinters fingerprinters/
COPY main.py .

ENV PYTHONPATH="/app"
ENTRYPOINT [""]
CMD ["python", "main.py"]
