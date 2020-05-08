FROM python:3.8

RUN mkdir /srv/quarantine
ADD . /srv/quarantine/

RUN python3 -m pip install -r /srv/quarantine/requirements.txt

CMD ["python3", "/srv/quarantine/app.py"]
