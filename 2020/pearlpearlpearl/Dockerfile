FROM python:3.8

RUN mkdir /srv/pearlpearlpearl
ADD . /srv/pearlpearlpearl/

RUN chmod -R 755 /srv/pearlpearlpearl
RUN useradd -ms /bin/bash ractf
USER ractf

CMD ["python3", "/srv/pearlpearlpearl/pearlpearlpearl.py"]
