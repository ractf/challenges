FROM python:3.9-buster

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

WORKDIR /app/src

ENV SECRET_KEY=PBh{EVQ8,$$c_j2cHN<)Dq6(fLJ?bFK

CMD gunicorn -w 4 -b 0.0.0.0:80 secretstore.wsgi:application

EXPOSE 80
