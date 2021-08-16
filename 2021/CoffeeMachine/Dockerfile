FROM python:3.8-buster

WORKDIR /app

ADD coffeemachine.jar /app/.
ADD app.py /app/.
ADD requirements.txt /app/.

RUN pip install -r requirements.txt
RUN pip install gunicorn

RUN adduser --system --shell /bin/bash ractf

RUN apt update && apt install -y openjdk-11-jre-headless

USER ractf

#EXPOSE 80
#CMD gunicorn --bind 0.0.0.0:80 -w 4 app:app

EXPOSE 5000
CMD python app.py
