FROM python:3.8-alpine

RUN mkdir /srv/challenge
ADD . /srv/challenge/

RUN apk add socat

RUN chmod -R 755 /srv/challenge
RUN adduser -Ss /bin/bash ractf
USER ractf
WORKDIR /srv/challenge

CMD ["socat", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/gen.py,stderr"]
