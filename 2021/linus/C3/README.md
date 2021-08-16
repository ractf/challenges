# Name: Call&Response

# Brief

Agent,

We're working a major case. We've been called in to covertly investigate a foreign govt agency, the GDGS, by a private organisation. We've finished performing initial reconnaissance of the target building and it's surrounding areas. We know they have a wireless network which they use to carry out live activities. Gaining access here would be substiantial. Problem is, they've somewhat competently secured it using WPA2 EAP-PEAP authentication which means gaining a packet capture of the handshake process is useless as the authentication exchange is carried out over a TLS 1.2 session. Nonetheless, we setup an access point with same ESSID as the target and managed to trick an employee's device into attempting to connect to our AP. In the process, we've obtained an username and certain auth values. We're not entirely sure what we need to do with them.

Can you take a look and help us recover the password?

```
username:	PrinceAli
c:	c3:ae:5e:f9:dc:0e:22:fb
r:	6c:52:1e:52:72:cc:7a:cb:0e:99:5e:4e:1c:3f:ab:d0:bc:39:54:8e:b0:21:e4:d0
```

> Flag format is ractf{recovered_password}
