FROM python:3.8-alpine

RUN mkdir /srv/challenge
ADD teleport.py /srv/challenge/teleport.py

RUN apk add socat

RUN chmod -R 755 /srv/challenge
RUN adduser -Ss /bin/bash ractf
USER ractf

CMD ["socat", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/teleport.py"]
