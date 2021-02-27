# Docker image for building doc site
FROM merkely/change

WORKDIR /docs

# install sphinx
ADD requirements.txt /docs
RUN pip3 install -r requirements.txt
