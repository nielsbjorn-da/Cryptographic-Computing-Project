import ecdsa
import random
from Crypto.Hash import SHA256


######################################################################################################################

class threshold_ecdsa():
    def __init__(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator
        self.alice = server("Alice", self.order)
        self.bob = server("Bob", self.order)

    def key_generation(self):
        secret_key = random.randint(0, self.order)
        secret_share_of_secret_key_for_server1 = random.randint(0, self.order)
        secret_share_of_secret_key_for_server2 = (secret_key - secret_share_of_secret_key_for_server1) % self.order
        self.alice.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server1)
        self.bob.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server2)
        public_key = self.open_curve_point(self.convert(secret_share_of_secret_key_for_server1),
                                           self.convert(secret_share_of_secret_key_for_server2))

        return public_key

    def rand_mul(self):
        random_triple_for_server1 = []
        random_triple_for_server2 = []

        a = random.randint(0, self.order)
        secret_share_of_a_for_server1 = random.randint(0, self.order)
        secret_share_of_a_for_server2 = (a - secret_share_of_a_for_server1) % self.order

        b = random.randint(0, self.order)
        secret_share_of_b_for_server1 = random.randint(0, self.order)
        secret_share_of_b_for_server2 = (b - secret_share_of_b_for_server1) % self.order

        c = a * b % self.order
        secret_share_of_c_for_server1 = random.randint(0, self.order)
        secret_share_of_c_for_server2 = (c - secret_share_of_c_for_server1) % self.order

        random_triple_for_server1.append(secret_share_of_a_for_server1)
        random_triple_for_server1.append(secret_share_of_b_for_server1)
        random_triple_for_server1.append(secret_share_of_c_for_server1)

        random_triple_for_server2.append(secret_share_of_a_for_server2)
        random_triple_for_server2.append(secret_share_of_b_for_server2)
        random_triple_for_server2.append(secret_share_of_c_for_server2)

        return random_triple_for_server1, random_triple_for_server2

    def open(self, secret_share_for_server1, secret_share_for_server2):
        opened_value = (secret_share_for_server1 + secret_share_for_server2) % self.order
        return opened_value

    def open_curve_point(self, secret_share_of_curve_point_server1, secret_share_of_curve_point_server2):
        opened_curve_point = secret_share_of_curve_point_server1 + secret_share_of_curve_point_server2
        return opened_curve_point

    def convert(self, secret_share):
        secret_curve_point = secret_share * self.generator
        return secret_curve_point

    def user_independent_preprocessing(self):
        # Step 1
        random_triple_for_server1, random_triple_for_server2 = self.rand_mul()
        secret_share_of_a_for_server1 = random_triple_for_server1[0]
        secret_share_of_a_for_server2 = random_triple_for_server2[0]
        secret_share_of_b_for_server1 = random_triple_for_server1[1]
        secret_share_of_b_for_server2 = random_triple_for_server2[1]
        secret_share_of_c_for_server1 = random_triple_for_server1[2]
        secret_share_of_c_for_server2 = random_triple_for_server2[2]

        # Step 2
        c = self.open(secret_share_of_c_for_server1, secret_share_of_c_for_server2)

        # Step 3
        secret_share_of_k_inverse_for_server1 = secret_share_of_a_for_server1
        secret_share_of_k_inverse_for_server2 = secret_share_of_a_for_server2

        # Step 4
        c_inverse = pow(c, -1, self.order)
        secret_shared_curve_point_of_k_inverse_for_server1 = self.convert(secret_share_of_b_for_server1) * c_inverse
        secret_shared_curve_point_of_k_inverse_for_server2 = self.convert(secret_share_of_b_for_server2) * c_inverse

        # Step 5
        return secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2

    def user_dependent_preprocessing(self):
        # Step 1
        secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2 = self.user_independent_preprocessing()
        secret_share_of_secret_key_for_server1 = self.alice.get_secret_share_of_secret_key()
        secret_share_of_secret_key_for_server2 = self.bob.get_secret_share_of_secret_key()

        # Step 2
        random_triple_for_server1, random_triple_for_server2 = self.rand_mul()
        secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = self.mult_two_wires(
            secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2,
            secret_share_of_secret_key_for_server1, secret_share_of_secret_key_for_server2, random_triple_for_server1, random_triple_for_server2)

        # Step 3
        return secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime

    def mult_two_wires(self, x_a, x_b, y_a, y_b, rand_triple_a, rand_triple_b):
        d_a = self.alice.add_wires(x_a, rand_triple_a[0])
        e_a = self.alice.add_wires(y_a, rand_triple_a[1])

        d_b = self.bob.add_wires(x_b, rand_triple_b[0])
        e_b = self.bob.add_wires(y_b, rand_triple_b[1])

        d_opened_a = self.alice.open(d_a, d_b)
        e_opened_a = self.alice.open(e_a, e_b)

        d_opened_b = self.bob.open(d_b, d_a)
        e_opened_b = self.bob.open(e_b, e_a)

        w_a = rand_triple_a[2]
        mult_1_a = self.alice.mult_with_constant(x_a, e_opened_a)
        mult_2_a = self.alice.mult_with_constant(y_a, d_opened_a)
        z_a = (w_a + mult_1_a + mult_2_a - (e_opened_a * d_opened_a))  # % self.alice.order

        w_b = rand_triple_b[2]
        mult_1_b = self.bob.mult_with_constant(x_b, e_opened_b)
        mult_2_b = self.bob.mult_with_constant(y_b, d_opened_b)
        z_b = (w_b + mult_1_b + mult_2_b)  # % self.bob.order #no e*d?
        return z_a, z_b

    def sign(self, message):
        secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = self.user_dependent_preprocessing()

        # Step 1
        R = self.open_curve_point(secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2)

        # Step 2
        r_x = R.x()

        # Step 3
        secret_share_of_signature_for_server1 = (hash_SHA256(message, self.order) * secret_share_of_k_inverse_for_server1) + (r_x * secret_share_of_secret_key_for_server1_prime)
        secret_share_of_signature_for_server2 = (hash_SHA256(message, self.order) * secret_share_of_k_inverse_for_server2) + (r_x * secret_share_of_secret_key_for_server2_prime)

        # Step 4
        s = self.open(secret_share_of_signature_for_server1, secret_share_of_signature_for_server2)
        return r_x, s

    def verify(self, message, r_x, s, pk):
        message_hash = hash_SHA256(message, self.order)
        s_inverse = pow(s, -1, self.order)
        y = message_hash * self.generator + r_x * pk
        curve_point = s_inverse * y
        return r_x == curve_point.x()

######################################################################################################################

class user:
    def __init__(self):
        self.wallet = 1000

######################################################################################################################

class server:
    def __init__(self, name, order):
        self.secret_share_of_secret_key = None
        self.name = name
        self.order = order

    def set_secret_share_of_secret_key(self, secret_share_of_secret_key):
        self.secret_share_of_secret_key = secret_share_of_secret_key

    def get_secret_share_of_secret_key(self):
        return self.secret_share_of_secret_key

    def open(self, x_a, x_b):
        return (x_a + x_b) % self.order

    def add_wires(self, x_a, y_a):
        return (x_a + y_a)  # % self.order

    def mult_with_constant(self, x_a, c):
        return x_a * c  # % self.order

######################################################################################################################

def hash_SHA256(message, order):
    h = SHA256.new()
    h.update(message)
    e = h.hexdigest()
    e = bin(int(e, 16))[2:]
    L_n = order.bit_length()
    z = e[:L_n]
    z = int(z)
    return z
