# get base image
FROM ubuntu:20.04

# install dependencies
RUN apt-get update -y
RUN apt-get install python3-pip -y

WORKDIR /cloudcomputing3/admin-project/

# copy files
COPY . .

# install requirements for flask
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "./app.py"]
