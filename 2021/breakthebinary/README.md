# breakthebinary
Flag: `ractf{Curb_Y0ur_M3mOry_Alloc4t10n}` (specified in flag.txt)

Please run the container per user, it's very small. The user should be given the `main.c` source file.

## To test
`docker build -t breakthebinary .`

`docker run -p 2222:22 -it breakthebinary`

`ssh ractf@127.0.0.1`, password `1WiUm2dnheQas`

## Solution
The binary is SUIDed as root, and the flag is owned by root. This makes it impossible to echo the contents of the flag.

What the binary appears to do is read in the flag, allocate some memory, copy the flag into that memory, encrypt it with random, and then copy it back onto the stack and print it out.

The interesting thing to note is that it allocates a whole megabyte of memory.
That, combined with the strong random source (seeded to the microsecond and key is also XORed with some data from /dev/random), should discourage people from trying to attack the encryption.

The trick is to make that allocation fail.

If the allocation fails, the flag is never recopied onto the stack and when the stack value is printed out, it'll just be the flag in cleartext. The user can make the allocation fail with `ulimit -Sv 500000` or so, then run the binary and decode from hex.

