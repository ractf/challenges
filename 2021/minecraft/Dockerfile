FROM docker.io/library/openjdk:16
WORKDIR /app
RUN adduser --system --shell /bin/bash ractf
COPY app /app
COPY entrypoint.sh /app

RUN curl https://papermc.io/api/v2/projects/paper/versions/1.17.1/builds/172/downloads/paper-1.17.1-172.jar --output /app/paper.jar
RUN echo ractf{D1ggyD1ggyH0le} > /flag.txt
RUN mkdir /app/logs
RUN chown -R ractf /app
RUN chown root /app/banned-ips.json /app/banned-players.json /app/ops.json /app/paper.yml /app/permissions.yml /app/server.properties /app/whitelist.json /app/entrypoint.sh /app/bukkit.yml /flag.txt
RUN chmod 644 /app/banned-ips.json /app/banned-players.json /app/ops.json /app/paper.yml /app/permissions.yml /app/server.properties /app/whitelist.json /app/entrypoint.sh /app/bukkit.yml /flag.txt

USER ractf

EXPOSE 25565
CMD [ "bash", "entrypoint.sh" ]
