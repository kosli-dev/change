# Docker image for building doc site
FROM merkely/change

WORKDIR /docs
RUN apk add make git

# install sphinx
ADD requirements.txt /docs
RUN pip3 install -r requirements.txt
