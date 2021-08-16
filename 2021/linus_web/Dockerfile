FROM alpine

# Configure SSH
RUN apk add --update openssh py3-pip runuser && rm -rf /tmp/* /var/cache/apk/*
RUN rm -rf /etc/ssh/ssh_host_rsa_key /etc/ssh/ssh_host_dsa_key
RUN python3 -m pip install Flask gunicorn
ADD sshd_config /etc/ssh/sshd_config
RUN echo -e "\n" | ssh-keygen -A
RUN mkdir /var/run/sshd
EXPOSE 42069
EXPOSE 5000

# Add our users
RUN adduser -D -s /bin/sh dev
RUN adduser -D -s /bin/sh admin
RUN echo "dev:7d5e56eb6fff922a0ba628f617ba4b361dcdd2d990dedc4795a70e4199391ae8" | chpasswd
RUN echo "admin:passwordqwertyuiop" | chpasswd
RUN echo "root:ubisoft" | chpasswd
RUN cp /etc/shadow /etc/shadow-backup.bak
RUN chown admin:admin /etc/shadow-backup.bak /opt
RUN chmod 660 /etc/shadow-backup.bak

# Fetch and set ffmpeg
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz -P /opt/
RUN tar -xf /opt/ffmpeg-git-amd64-static.tar.xz -C /opt/
RUN ls /opt/ -la
RUN ln -sf /opt/ffmpeg-git-20210724-amd64-static/ffmpeg /usr/local/bin/ffmpeg
RUN chown -R dev:dev /opt/ffmpeg-git-20210724-amd64-static

# Add webapp
ADD webapp /home/dev/
ADD root.txt /root/
RUN chown -R dev:dev /home/dev/templates /home/dev/static /home/dev/uploads
RUN chmod u+s /bin/su

WORKDIR /home/dev/
ENTRYPOINT /usr/sbin/sshd && runuser -l dev -c "gunicorn -b 0.0.0.0:5000 --timeout 200 wsgi:app"
