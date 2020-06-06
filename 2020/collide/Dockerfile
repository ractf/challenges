FROM node:10

RUN mkdir /srv/challenge

ADD . /srv/challenge/

WORKDIR /srv/challenge/

RUN npm i body-parser express

RUN chmod -R 755 /srv/challenge
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["node", "index.js"]
