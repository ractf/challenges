FROM python:3.9-buster

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN groupadd flag
RUN useradd --password 999999 -G flag -s /bin/bash admin
RUN useradd -r -s /bin/bash web

RUN echo "ractf{dj4ng0_lfi}" > /flag.txt
RUN chown root:flag /flag.txt
RUN chmod 640 /flag.txt
RUN chmod 644 /etc/shadow



CMD gunicorn -w 4 -b 0.0.0.0:80 notebook.wsgi:application

EXPOSE 80
