import rsa

import random


prime_pool = []
for _ in range(10):
    prime_pool.append(rsa.get_prime(512))


def get_prime():
    return random.choice(prime_pool)


def gen_challenge():
    r = random.randint(0, 4)

    if r == 0:
        p = get_prime()
        q = get_prime()
        have = {'p': p, 'q': q}
        need = {'n': p * q}
    elif r == 1:
        p = get_prime()
        q = get_prime()
        n = p * q

        have = {'p': p, 'n': n}
        need = {'q': q}
    elif r == 2:
        p = get_prime()
        q = get_prime()
        e = 65537
        phi = (p - 1) * (q - 1)
        d = rsa.modinv(e, phi)

        have = {'p': p, 'q': q, 'e': e}
        need = {'d': d}
    elif r == 3:
        p = get_prime()
        q = get_prime()
        e = 65537
        phi = (p - 1) * (q - 1)
        d = rsa.modinv(e, phi)

        pt = random.getrandbits(128)
        state = rsa.solve_for(p=p, q=q, e=e)
        ct = rsa.encrypt(state, pt, as_bytes=False)

        have = {'p': p, 'q': q, 'e': e, 'pt': pt}
        need = {'ct': ct}
    elif r == 4:
        p = get_prime()
        q = get_prime()
        e = 65537
        phi = (p - 1) * (q - 1)
        d = rsa.modinv(e, phi)

        pt = random.getrandbits(256)
        state = rsa.solve_for(p=p, q=q, e=e)
        ct = rsa.encrypt(state, pt, as_bytes=False)

        have = {'p': p, 'phi': phi, 'e': e, 'ct': ct}
        d = state[4]
        need = {'pt': pow(ct, d, p * q)}
    else:
        return {}, {}

    return have, need


def _main():
    for _ in range(100):
        have, need = gen_challenge()
        for i in have:
            print(f'{i}: {have[i]}')
        for i in need:
            print(f'{i}: ?')

        pt = have.pop('pt', None)
        ct = have.pop('ct', None)
        state = rsa.solve_for(**have)

        print(state)

        for i in need:
            if i in 'nepqd':
                val = state['nepqd'.index(i)]
            elif i == 'pt':
                val = rsa.decrypt(state, ct, False)
            elif i == 'ct':
                val = rsa.encrypt(state, pt, False)

            if str(val) != str(need[i]):
                print(need[i])
                print(val)
                print('---------------')

                #quit()

        print()
