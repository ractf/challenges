FROM alpine AS builder

RUN mkdir -p /opt
RUN apk add --update git alpine-sdk ncurses-dev bash linux-headers
ADD toybox /opt/toybox
WORKDIR /opt/toybox
RUN make CFLAGS=-static

WORKDIR /opt
RUN git clone https://github.com/mkj/dropbear.git
WORKDIR /opt/dropbear
RUN ./configure --disable-zlib --disable-syslog --enable-static --disable-wtmp --disable-lastlog
ADD localoptions.h .
RUN make PROGRAMS="dropbear"

WORKDIR /opt
ADD disabled.c /opt/disabled.c
RUN gcc -Os -static disabled.c -o disabled

RUN mkdir -p /opt/newfs/opt/ /opt/newfs/etc/
RUN cp /opt/toybox/toybox /opt/newfs/opt/toybox
RUN cp /opt/dropbear/dropbear /opt/newfs/opt/dropbear
RUN cp /opt/disabled /opt/newfs/opt/disabled
RUN adduser -h /home/ractf -s /bin/sh -D ractf
ADD motd /opt/newfs/etc/motd

WORKDIR /opt/newfs
RUN mkdir -p usr/bin bin sbin lib tmp run var srv media home/ractf root etc/dropbear
RUN for cmd in $(opt/toybox --long); do \
        ln -s /opt/toybox $cmd; \
    done

WORKDIR /opt/newfs/bin
RUN for cmd in 'ls' 'cat' 'tail' 'head' 'dir' 'less' 'more' 'vi' 'vim' 'grep'; do \
        ln -s /opt/disabled $cmd; \
    done
ADD flag.txt /opt/newfs/home/ractf/flag.txt
RUN chown -R ractf:ractf /opt/newfs/home/ractf/
RUN chmod -R +x /opt/newfs/home/ractf/
RUN chmod -x /opt/newfs/home/ractf/flag.txt
# Throw away this builder container now

FROM scratch
COPY --from=0 /opt/newfs/ /
EXPOSE 22
CMD echo "root:x:0:0:root:/root:" > /etc/passwd; echo "ractf:x:1000:1000:Linux User,,,:/home/ractf:/bin/sh" >> /etc/passwd; \
    echo "root:!::0:::::" > /etc/shadow; echo -n "ractf:" >> /etc/shadow; echo "8POlNixzDSThy" | mkpasswd -m sha512 >> /etc/shadow; \
    echo ":18834:0:99999:7:::" >> /etc/shadow; /opt/dropbear -R -F
