# Writeup

Dead simple, throw into asleap and use a well-known wordlist like rockyou or any wpa one that's more than 5k in size of the most popular passwords.

```sh
asleap -C "c3:ae:5e:f9:dc:0e:22:fb" -R "6c:52:1e:52:72:cc:7a:cb:0e:99:5e:4e:1c:3f:ab:d0:bc:39:54:8e:b0:21:e4:d0" -W /usr/share/rockyou.txt
```

This spits out the password of `rainbow6`, just throw that into the flag format. You don't have to do it this way, you can also turn it into a NETNTLM hash and toss in JTR or Hashcat in the format `username::::response:challenge`.

# Flag

`ractf{rainbow6}`
