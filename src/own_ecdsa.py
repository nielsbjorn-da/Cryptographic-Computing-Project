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
    r_x = 0
    while r_x == 0:
        # Pick random cryptographic random
        k = random.randint(1, EC.n - 1)

        # Calculating point on curve.
        curve_point = k * EC.generator

        r_x = curve_point.x() % EC.n

    k_inverse = pow(k, -1, EC.n)
    s = k_inverse * (message_hash + r_x * sk) % EC.n

    return r_x, s


def verify_signature(message, s, r_x, pk, EC: EllipticCurve):
    # SOME STEPS TO VERIFY CURVE POINT
    # TODO

    # SOME STEPS TO VERIFY r AND s.
    # TODO

    # Hash the message
    message_hash = hash_SHA256(message)

    # Find S inverse
    s_inverse = pow(s, -1, EC.n)
    curve_point = (message_hash * s_inverse) % EC.n * EC.generator + (r_x * s_inverse) % EC.n * pk

    return r_x == curve_point.x()

def create_generator():
    EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)
    return EC

if __name__ == '__main__':
    EC = create_generator()

    message = b'Det var sku et godt link christian (kakadue)'

    # Generate a random int as secret key
    sk = random.randint(1, EC.n - 1)

    # Create a public key
    pk = sk * EC.generator

    # Sign message
    r_x, s = sign_message(message=message, sk=sk, EC=EC)

    # Verify signature on message
    result = verify_signature(message=message, s=s, pk=pk, r_x=r_x, EC=EC)

    print("Message:", message.decode('ascii'), "verification on signature is:", result)
    print(EC.n)
