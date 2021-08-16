#!/bin/sh
ssh 20
ssh-keygen -A
/usr/sbin/sshd -D -e
