FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5002

ENTRYPOINT ["/usr/bin/python" , "/app/app.py"]
