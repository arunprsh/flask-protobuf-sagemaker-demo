FROM ubuntu:latest

MAINTAINER Arun Shankar (arunprsh@amazon.com)

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY ./requirements.txt /flask-app/requirements.txt
COPY ./templates /flask-app/templates
COPY *.py /flask-app/
COPY *.proto /flask-app/
COPY *.jpg /flask-app/
COPY generate_definitions.sh /flask-app/generate_definitions.sh
WORKDIR /flask-app
RUN pip install -r requirements.txt

COPY ./app.py /flask-app/app.py

EXPOSE 8080

ENTRYPOINT ["python", "app.py"]