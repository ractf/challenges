FROM alpine AS builder

RUN mkdir -p /opt
RUN apk add --update git alpine-sdk ncurses-dev bash linux-headers
RUN git clone https://github.com/landley/toybox.git /opt/toybox
WORKDIR /opt/toybox
ADD .config .
RUN make CFLAGS=-static

WORKDIR /opt
RUN git clone https://github.com/mkj/dropbear.git
WORKDIR /opt/dropbear
RUN ./configure --disable-zlib --disable-syslog --enable-static --disable-wtmp --disable-lastlog
ADD localoptions.h .
RUN make PROGRAMS="dropbear"

RUN mkdir -p /opt/chall
WORKDIR /opt/chall
ADD main.c .
ADD aes.c .
ADD aes.h .
RUN gcc -Os -static aes.c main.c -o program

RUN mkdir -p /opt/newfs/opt/ /opt/newfs/etc/
RUN cp /opt/toybox/toybox /opt/newfs/opt/toybox
RUN cp /opt/dropbear/dropbear /opt/newfs/opt/dropbear
RUN adduser -h /home/ractf -s /bin/sh -D ractf
ADD motd /opt/newfs/etc/motd

WORKDIR /opt/newfs
RUN mkdir -p usr/bin bin sbin lib tmp run var srv media home/ractf root etc/dropbear
RUN for cmd in $(opt/toybox --long); do \
        ln -s /opt/toybox $cmd; \
    done

RUN cp /opt/chall/program /opt/newfs/home/ractf/program
ADD flag.txt /opt/newfs/home/ractf/flag.txt
RUN head -c 16 /dev/random > /opt/newfs/home/ractf/keyfile
RUN chown -R ractf:ractf /opt/newfs/home/ractf/
RUN chmod -R +x /opt/newfs/home/ractf/

RUN chown root:root /opt/newfs/home/ractf/flag.txt /opt/newfs/home/ractf/program /opt/newfs/home/ractf/keyfile
RUN chmod 700 /opt/newfs/home/ractf/flag.txt /opt/newfs/home/ractf/keyfile
RUN chmod u+s /opt/newfs/home/ractf/program
# Throw away this builder container now

FROM scratch
COPY --from=0 /opt/newfs/ /
EXPOSE 22
CMD echo "root:x:0:0:root:/root:" > /etc/passwd; echo "ractf:x:1000:1000:Linux User,,,:/home/ractf:/bin/sh" >> /etc/passwd; echo "root:!::0:::::" > /etc/shadow; echo "ractf:`echo "1WiUm2dnheQas" | mkpasswd -m sha512`:18834:0:99999:7:::" >> /etc/shadow; /opt/dropbear -R -F
