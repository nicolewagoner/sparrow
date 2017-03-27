FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
# RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# TODO should be able to specify this to requirements.txt but for some reason
#   it hates me there, with and without version specified
RUN python -m pip install pymongo

EXPOSE 5000

ENTRYPOINT ["/usr/bin/python" , "/app/app.py"]
