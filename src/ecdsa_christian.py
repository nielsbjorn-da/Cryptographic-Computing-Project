import random
from Crypto.Hash import SHA512
import own_ecdsa


# I STOLE THIS: https://rosettacode.org/wiki/Modular_inverse#Python
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def hashSHA512(message):
    h = SHA512.new()
    h.update(message)
    return h.hexdigest()


def sign(message, d_a, n, G):
    e = hashSHA512(message)
    e = bin(int(e, 16))[2:]
    L_n = n.bit_length()
    z = e[:L_n]
    z = int(z)
    r = None
    while True:
        k = random.randint(1, n-1)
        curve_point = k * G
        x_1 = curve_point.x()
        r = x_1 % n
        if r != 0:
            break
    k_inverse = modinv(k, n)
    s = k_inverse * (z + r * d_a) % n
    return r, s

def verify(message, s, r, G, Q_a):
    # SOME STEPS TO VERIFY CURVE POINT
    # Yada, yada, yada.

    # SOME STEPS TO VERIFY r AND s.
    # Yada, yada, yada.

    e = hashSHA512(message)
    e = bin(int(e, 16))[2:]
    L_n = n.bit_length()
    z = e[:L_n]
    z = int(z)
    s_inverse = modinv(s, n)
    u1 = (z * s_inverse) % n
    u2 = (r * s_inverse) % n
    curve_point = u1 * G + u2 * Q_a

    return r == curve_point.x()


if __name__ == '__main__':

    n = ecdsa.curves.SECP256k1.order
    d_a = random.randint(1, n-1)
    G = ecdsa.SECP256k1.generator
    Q_a = d_a * G

    message = "42".encode("utf8")

    r, s = sign(message, d_a, n, G)

    result = verify(message, s, r, G, Q_a)

    print(result)
