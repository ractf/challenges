FROM python:3.8

RUN mkdir /srv/quarantine
ADD . /srv/quarantine/

RUN python3 -m pip install -r /srv/quarantine/requirements.txt

RUN chmod -R 755 /srv/quarantine
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["python3", "/srv/quarantine/app.py"]
