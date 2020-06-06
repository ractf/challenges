#!/usr/local/bin/python
import rsa


FLAG = 'ractf{S0m3t1mesS1zeDoesM4773r}'


p = 17
q = rsa.get_prime()
e = 65537

state = rsa.solve_for(p=p, q=q, e=e)

pt = int.from_bytes(FLAG.encode(), 'big')
ct = rsa.encrypt(state, pt, as_bytes=False)


print('n:', state[0])
print('e:', e)
print('ct:', ct)
