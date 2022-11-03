import math
import random
from Crypto.Hash import SHA256
import ecdsa.curves


class EllipticCurve():
    def __init__(self, generator):
        self.generator = generator
        self.n = self.generator.order()
        self.p = self.generator.curve().p()
        #        self.h = self.generator.curve().h()
        self.a = self.generator.curve().a()
        self.b = self.generator.curve().b()
        self.x = self.generator.x()
        self.y = self.generator.y()


def hash_SHA256(message):
    h = SHA256.new()
    h.update(message)

    message_hash = h.hexdigest()
    message_hash_int = int(message_hash, 16)
    message_hash_binary = format(message_hash_int, 'b')
    n_bit_length = EC.n.bit_length()
    hash = message_hash_binary[:n_bit_length]
    hash = int(hash)

    return hash


def sign_message(message, sk, EC: EllipticCurve):
    # Hash the message
    message_hash = hash_SHA256(message)

    # Compute r
    # If r is zero choose another cryptographic random k.
    r = 0
    while r == 0:
        # Pick random cryptographic random
        k = getRandomK(EC)

        # Calculating point on curve.
        curve_point = k * EC.generator

        r = curve_point.x() % EC.n

    s = pow(k, -1, EC.n) * (message_hash + r * sk) % EC.n

    return s, r


def getRandomK(EC: EllipticCurve):
    max_int = EC.n - 1
    random_int = random.randint(1, max_int)
    return random_int


def verify_signature(message, s, r_x, pk):
    # Hash the message
    message_hash = hash_SHA256(message)

    # Find S inverse
    s_inverse = pow(s, -1, EC.n)
    curve_point = (message_hash * s_inverse) % EC.n * EC.generator + (r_x * s_inverse) % EC.n * pk

    return r_x == curve_point.x()


if __name__ == '__main__':
    EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)

    message = b'Det var sku et godt link christian (kakadue)'

    # Generate a random int as secret key
    sk = getRandomK(EC=EC)

    # Create a public key
    pk = sk * EC.generator

    # Sign message
    s, r = sign_message(message=message, sk=sk, EC=EC)

    # Verify signature on message
    result = verify_signature(message=message, s=s, pk=pk, r_x=r)
    print("Message:", message.decode('ascii'), "verification on signature is:", result)
