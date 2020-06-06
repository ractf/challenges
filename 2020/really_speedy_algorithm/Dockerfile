FROM python:3.8

RUN mkdir /srv/challenge
ADD . /srv/challenge/

RUN chmod -R 755 /srv/challenge
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["python3", "/srv/challenge/server.py"]
