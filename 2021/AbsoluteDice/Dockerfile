FROM i386/debian
WORKDIR /srv

RUN apt update && apt install socat -y && rm -rf /var/lib/apt/lists/*
ADD AbsoluteDice /srv/challenge
ADD flag.txt /srv/flag.txt
RUN chmod +x /srv/challenge

EXPOSE 5000
CMD ["socat", "-s", "tcp-l:5000,reuseaddr,fork", "exec:/srv/challenge,stderr"]
