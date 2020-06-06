FROM python:3.8-alpine

RUN mkdir /srv/challenge
ADD . /srv/challenge/

RUN apk add socat

RUN chmod -R 755 /srv/challenge
RUN adduser -Ss /bin/bash ractf
USER ractf

RUN touch /home/ractf/flag.txt
RUN echo "ractf{Puff3rf1sh??}" > /home/ractf/flag.txt

CMD ["socat", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/pybo.py"]
