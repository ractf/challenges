# militarygrade
Flag: `ractf{int3rEst1ng_M4sk_paTt3rn}` (specified at top of source file)

This container should be run just once, please expose its port 80 somewhere where users can access it.

## To test
`docker build -t militarygrade .`

`docker run -p 8080:80 -it militarygrade`

`curl localhost:8080`

## Solution

Yeah basically the seed for random is the current nanosecond unix timestamp masked by the inverse of `0x7FFFFFFFFEFFFF00` (any bit that's 1, the output will be 0).

This reduces the key space to 2^13, which is easily exhaustible. There are some shenanigans of reseeding, but at that time the state of the RNG is entirely predictable.

Brute force all key/iv pairs in that space, get a value for the encrypted flag and try them all :)

Note: because I use nanoseconds there isn't really an attack vulnerability that's any easier by guessing the time of the box.

UPDATE: a solve script is provided in solution/
