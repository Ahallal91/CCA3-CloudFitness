# get base image
FROM ubuntu:20.04

# install dependencies
RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y

# copy files
COPY requirements.txt requirements.txt
COPY admin-project /cloudcomputing3/admin-project/

# install requirements for flask
RUN pip install -r requirements.txt
WORKDIR /cloudcomputing3/admin-project/

CMD ["gunicorn3", "-b", "0.0.0.0:5000" "app:app", "--workers=1"]