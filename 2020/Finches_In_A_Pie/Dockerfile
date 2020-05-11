FROM alpine:3.7

RUN mkdir /srv/challenge
ADD . /srv/challenge/

RUN apm install socat

RUN chmod -R 755 /srv/challenge
RUN useradd -ms /bin/bash ractf
USER ractf

RUN touch /home/ractf/flag.txt
RUN echo "ractf{B4k1ng_4_p1E!}" > /home/ractf/flag.txt

CMD ["socat", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/stolen_pie"]
