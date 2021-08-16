FROM debian:10

RUN mkdir -p /srv/challenge
WORKDIR /srv/challenge

RUN apt update && apt-get install -y openssl libgmp-dev socat libssl-dev python3 && rm -rf /var/lib/apt/lists/* && ln -s /usr/bin/python3 /usr/bin/python
RUN echo "ractf{W3lComE_t0_Th3_LA_B3d_n_br3Akfast}" > /srv/challenge/flag.txt
ADD main /srv/challenge
ADD pubkey.pem /srv/challenge
ADD libcrypto.so.1.0.0 /usr/lib

RUN adduser --system --shell /bin/sh ractf
USER ractf

CMD ["socat", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge/main,stderr"]
