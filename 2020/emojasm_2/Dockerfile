FROM python:3
ADD emojasm /emojasm
ADD flasksite /flasksite
RUN pip install flask

RUN useradd -ms /bin/bash ractf
USER ractf

CMD [ "python", "-m", "flasksite" ]
