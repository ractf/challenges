import random
import math


def isprime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    s, r = 0, n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def get_prime(bits=512):
    while True:
        n = random.getrandbits(bits)
        # apply a mask to set MSB and LSB to 1
        n |= (1 << bits - 1) | 1

        if isprime(n):
            return n


def modinv(a, m):
    if math.gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def find_factor_pair(n, max_v=1<<16):
    for i in range(3, min(max_v, int(math.sqrt(n))) + 1, 2):
        if n % i == 0:
            return i, n // i
    return None, None


def solve_for(n=None, e=None, p=None, q=None, d=None, phi=None):
    if p is None and phi is not None:
        if phi % (q - 1) != 0:
            raise ValueError('(q - 1) not a factor of phi!')
        p = (phi // (q - 1)) + 1

    if q is None and phi is not None:
        if phi % (p - 1) != 0:
            raise ValueError('(p - 1) not a factor of phi!')
        q = (phi // (p - 1)) + 1

    if n is not None:
        if p is None and q is not None:
            if n % q != 0:
                raise ValueError('q not a factor of n!')
            p = n // q
        if q is None and p is not None:
            if n % p != 0:
                raise ValueError('p not a factor of n!')
            q = n // p

    if n is not None and p is None and q is None:
        p, q = find_factor_pair(n)
        if p is None:
            raise ValueError('No factors found for n!')

    if n is None and p is not None and q is not None:
        n = p * q

    if p is not None and q is not None and d is None:
        phi = (p - 1) * (q - 1)
        if e is not None:
            d = modinv(e, phi)

    return n, e, p, q, d


def decrypt(values, ct, as_bytes=True):
    n, e, p, q, d = values
    if d is None or n is None:
        raise ValueError('Both d and n required to decrypt!')

    if isinstance(ct, (bytes, bytearray)):
        ct = int.from_bytes(ct, 'big')
    pt = pow(ct, d, n)

    if not as_bytes:
        return pt
    return int.to_bytes(pt, 256, 'big').strip(b'\0')


def encrypt(values, pt, as_bytes=True):
    n, e, p, q, d = values
    if d is None or n is None:
        raise ValueError('Both e and n required to encrypt!')

    if isinstance(pt, (bytes, bytearray)):
        pt = int.from_bytes(pt, 'big')
    ct = pow(pt, e, n)

    if not as_bytes:
        return ct
    return int.to_bytes(ct, 256, 'big').strip(b'\0')


def _main():
    p = get_prime(512)
    q = get_prime(512)
    e = 65537

    n = p * q
    phi = (p - 1) * (q - 1)
    d = modinv(e, phi)

    pt = int.from_bytes(b'Hello, friends', 'big')

    # enc
    ct = pow(pt, e, n)
    ct = pow(ct, e, n)

    # dec
    pt = pow(ct, d, n)
    pt = pow(pt, d, n)

    pt = int.to_bytes(pt, 256, 'big').strip(b'\0')

    print(pt)

    quit()

