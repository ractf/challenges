#!/bin/bash

FLAG="ractf{DreadingPirates}"

rm /root/original-ks.cfg

dnf update -y
dnf install epel-release nginx libsodium-devel -y
dnf groupinstall "Development Tools" -y

cat <<EOF > /etc/yum.repos.d/tor.repo
[tor]
name=Tor for Enterprise Linux $releasever - \$basearch
baseurl=https://rpm.torproject.org/centos/\$releasever/\$basearch
enabled=1
gpgcheck=1
gpgkey=https://rpm.torproject.org/centos/public_gpg.key
cost=100
EOF

dnf install tor -y

mkdir -p /etc/ractf/tor /etc/ractf/tor/authorized_clients /usr/share/nginx/tor

cat <<EOF > /etc/tor/torrc
ControlSocket /run/tor/control
ControlSocketsGroupWritable 1
CookieAuthentication 1
CookieAuthFile /run/tor/control.authcookie
CookieAuthFileGroupReadable 1
HiddenServiceDir /etc/ractf/tor
HiddenServiceVersion 3
HiddenServicePort 80 127.0.0.1
EOF

git clone https://github.com/cathugger/mkp224o.git /etc/ractf/mkp224o
cd /etc/ractf/mkp224o && ./autogen.sh && ./configure && make
DOMAIN=$(/etc/ractf/mkp224o/mkp224o filter ractf -t 4 -v -n 1 -d /etc/ractf/generated -q 2>/dev/null)
mv /etc/ractf/generated/$DOMAIN/* /etc/ractf/tor
chown -R toranon /etc/ractf/tor
chmod 700 /etc/ractf/tor


systemctl enable --now tor.service
systemctl restart tor.service

cat <<EOF > /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 2048;
    server_names_hash_bucket_size 128;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80 default_server;
        listen       [::]:80 default_server;
        server_name  _;
        root         /usr/share/nginx/html;
    }
    
    server {
        listen       80;
        listen       [::]:80;
        server_name  $DOMAIN;
        root         /usr/share/nginx/tor;
    }
}
EOF

rm -rf /usr/share/nginx
mkdir /usr/share/nginx/{html,tor}/assets -p

touch /usr/share/nginx/html/favicon.ico

ln -s /usr/share/nginx/html/favicon.ico /usr/share/nginx/tor/favicon.ico



IP=$(curl -s ip.me)

systemctl enable --now nginx.service
systemctl restart nginx.service

echo "---
Hidden Service: $DOMAIN
Real IP: $IP
You need to copy the 'content' folder to /usr/share/nginx, then submit this IP to Shodan
---
"
