import random
from Crypto.Hash import SHA256
import ecdsa
from src.BeDOZa_arithmetic.util import hash_SHA256
G = ecdsa.SECP256k1.generator
n = ecdsa.curves.SECP256k1.order

def key_generation():
    d_a = random.randint(1, n-1)
    Q_a = d_a * G
    return d_a, Q_a

def sign(message, d_a):
    z = hash_SHA256(message, n)
    r = None
    while True:
        k = random.randint(1, n-1)
        curve_point = k * G
        x_1 = curve_point.x()
        r = x_1 % n
        if r != 0:
            break
    k_inverse = pow(k, -1, n)
    s = k_inverse * (z + r * d_a) % n
    return r, s

def verify(message, s, r, Q_a):
    z = hash_SHA256(message, n)
    s_inverse = pow(s, -1, n)
    u1 = (z * s_inverse) % n
    u2 = (r * s_inverse) % n
    curve_point = u1 * G + u2 * Q_a

    return r == curve_point.x()


if __name__ == '__main__':
    message = "42".encode("utf8")
    d_a, Q_a = key_generation()
    r, s = sign(message, d_a)

    result = verify(message, s, r, Q_a)

    print(result)