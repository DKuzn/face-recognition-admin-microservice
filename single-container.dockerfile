FROM ubuntu:22.04

RUN apt-get update
RUN apt install -y python3-dev default-libmysqlclient-dev build-essential
RUN apt install -y pip
RUN apt install -y git
WORKDIR /root/
RUN mkdir face-recognition-admin-microservice
WORKDIR /root/face-recognition-admin-microservice
COPY FRAMS /root/face-recognition-admin-microservice/FRAMS
COPY main.py /root/face-recognition-admin-microservice
COPY requirements.txt /root/face-recognition-admin-microservice
RUN pip install -r requirements.txt
RUN pip cache purge
RUN apt-get clean

ENTRYPOINT ["gunicorn", "main:app", "-b 0.0.0.0:80", "-w 4", "-k uvicorn.workers.UvicornWorker", "-t 0"]