#!/usr/local/bin/python
import rsa


FLAG = 'ractf{JustLikeInTheSimulations}'


p = rsa.get_prime()
q = rsa.get_prime()
e = 65537

state = rsa.solve_for(p=p, q=q, e=e)

pt = int.from_bytes(FLAG.encode(), 'big')

ct = rsa.encrypt(state, FLAG.encode(), as_bytes=False)

print('p:', p)
print('q:', q)
print('e:', e)
print('ct:', ct)
