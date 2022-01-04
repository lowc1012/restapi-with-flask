FROM ubuntu:18.04

RUN apt-get update && apt-get install -y --no-install-recommends software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.7 python3-dev python3-pip libpython3.7-dev && ln -s python3.7 /usr/bin/python

RUN mkdir "/app"
COPY ./* /app

WORKDIR /app
RUN python -m pip install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
