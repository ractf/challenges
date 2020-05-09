FROM python:3.8

RUN mkdir /srv/raro
ADD . /srv/raro/

RUN python3 -m pip install -r /srv/raro/requirements.txt

RUN chmod -R 755 /srv/raro
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["python3", "/srv/raro/main.py"]
