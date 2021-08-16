# missingtools
Flag: `ractf{std0ut_1s_0v3rr4ted_spl1t_sha}` (specified in flag.txt)

Please run the container per user, it's very small.

## To test
`docker build -t missingtools .`

`docker run -p 2222:22 -it missingtools`

`ssh ractf@127.0.0.1`, password `8POlNixzDSThy`

## Walkthrough
![demo](demo.mp4)

The shell is limited such that the solver cannot write the contents of flag.txt to standard out.
However, sha256sum is provided. By splitting the file into small parts and then hashing, they can be looked up and "reversed".

Solver can use `echo *` as a workaround for `ls`, and so can easily enumerate the tools they have by looking at `echo $PATH`.

I hope this makes it less of a guessing game.
