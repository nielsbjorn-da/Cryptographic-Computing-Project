import math
import random
from Crypto.Hash import SHA256
import ecdsa.curves


def hashSHA256(message):
    h = SHA256.new()
    h.update(message)
    return h.hexdigest()


def sign(message, sk, p, generator, n):
    k = getRandomK(p)
    r_x = generator.x() * k
    message_hash = hashSHA256(message)
    s = (int(message_hash, 16) + sk * r_x) * pow(k, -1, n)
    s = s % n
    return s, r_x


def getRandomK(order):
    randomint = random.randint(1, order)
    return randomint


def verify(message, s, r_x, n, generator, pk, p):
    hash_message = hashSHA256(message)
    s_inverse = pow(int(s), -1, n)
    assert int(hash_message, 16) < p
    y = int(hash_message, 16) * generator.x() + r_x * pk
    random_point = y * s_inverse

    return r_x == random_point


if __name__ == '__main__':
    n = ecdsa.curves.SECP256k1.order
    p = ecdsa.curves.SECP256k1.curve.p()
    assert n < p
    generator = ecdsa.curves.SECP256k1.generator
    sk = getRandomK(p)

    pk = sk * generator.x()

    message = b'hello'

    s, r_x = sign(message, sk, p, generator, n)

    result = verify(message, s, r_x, n, generator, pk, p)
    print(result)
