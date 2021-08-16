FROM python:3.9-buster

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN groupadd flag
RUN useradd --password 999999 -G flag -s /bin/bash admin
RUN useradd -r -s /bin/bash web

RUN echo "ractf{dj4ng0_lfi_rce_not_unintended}" > /flag.txt
RUN chown root:flag /flag.txt
RUN chmod 640 /flag.txt
RUN chmod 644 /etc/shadow
RUN chmod 777 /app

RUN echo "999999\n999999\n" | passwd admin

USER web

EXPOSE 8000

CMD ./entrypoint.sh
