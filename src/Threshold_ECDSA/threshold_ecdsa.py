import ecdsa
import random
from src.BeDOZa_arithmetic.util import hash_SHA256
from src.BeDOZa_arithmetic.alice import Alice
from src.BeDOZa_arithmetic.bob import Bob
from src.BeDOZa_arithmetic.dealer import Dealer
from src.BeDOZa_arithmetic.util import mult_two_wires


class threshold_ecdsa():
    def __init__(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator
        self.alice = Alice(order=self.order)
        self.bob = Bob(order=self.order)
        self.dealer = Dealer(order=self.order)

    def key_generation(self):
        secret_key = random.randint(0, self.order)
        secret_share_of_secret_key_for_server1 = random.randint(0, self.order)
        secret_share_of_secret_key_for_server2 = (secret_key - secret_share_of_secret_key_for_server1) % self.order
        self.alice.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server1)
        self.bob.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server2)
        public_key = self.open_curve_point(self.convert(secret_share_of_secret_key_for_server1),
                                           self.convert(secret_share_of_secret_key_for_server2))

        return public_key

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
        random_triple_for_server1, random_triple_for_server2 = self.dealer.rand_mul()
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
        random_triple_for_server1, random_triple_for_server2 = self.dealer.rand_mul()
        secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = mult_two_wires(
            self.alice, self.bob,
            secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2,
            secret_share_of_secret_key_for_server1, secret_share_of_secret_key_for_server2, random_triple_for_server1,
            random_triple_for_server2)

        # Step 3
        return secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime

    def sign(self, message):
        secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = self.user_dependent_preprocessing()

        # Step 1
        R = self.open_curve_point(secret_shared_curve_point_of_k_inverse_for_server1,
                                  secret_shared_curve_point_of_k_inverse_for_server2)

        # Step 2
        r_x = R.x()

        # Step 3
        secret_share_of_signature_for_server1 = (hash_SHA256(message,
                                                             self.order) * secret_share_of_k_inverse_for_server1) + (
                                                            r_x * secret_share_of_secret_key_for_server1_prime)
        secret_share_of_signature_for_server2 = (hash_SHA256(message,
                                                             self.order) * secret_share_of_k_inverse_for_server2) + (
                                                            r_x * secret_share_of_secret_key_for_server2_prime)

        # Step 4
        s = self.open(secret_share_of_signature_for_server1, secret_share_of_signature_for_server2)
        return r_x, s

    def verify(self, message, r_x, s, pk):
        message_hash = hash_SHA256(message, self.order)
        s_inverse = pow(s, -1, self.order)
        y = message_hash * self.generator + r_x * pk
        curve_point = s_inverse * y
        return r_x == curve_point.x()
