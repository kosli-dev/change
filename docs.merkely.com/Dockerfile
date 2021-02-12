# Docker image for building doc site
FROM merkely/change

#install sphinx

WORKDIR /docs
ADD requirements.txt /docs
RUN pip3 install -r requirements.txt
