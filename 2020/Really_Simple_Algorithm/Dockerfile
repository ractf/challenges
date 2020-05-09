FROM python:3.8

RUN mkdir /srv/challenge
ADD . /srv/challenge/

RUN apm install socat

RUN chmod -R 755 /srv/challenge
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["socat", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/gen.py"]
