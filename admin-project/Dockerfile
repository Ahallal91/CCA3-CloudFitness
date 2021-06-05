# get base image
FROM python:3.7

RUN apt-get update
RUN apt-get install -y gunicorn
RUN apt-get install -y python-gevent

# set ENV variables
ENV FLASK_ENV=production

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ARG API_GATEWAY_KEY

ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION
ENV API_GATEWAY_KEY $API_GATEWAY_KEY

ADD ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

# copy files
COPY . ./admin-project
WORKDIR /admin-project

# start gunicorn web server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "application:application", "--workers=5"]
