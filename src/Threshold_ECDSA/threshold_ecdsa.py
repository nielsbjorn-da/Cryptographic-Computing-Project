import random

import ecdsa

from ..BeDOZa_arithmetic.alice import Alice
from ..BeDOZa_arithmetic.bob import Bob
from ..BeDOZa_arithmetic.dealer import Dealer
import src.BeDOZa_arithmetic.util as util

from src.own_ecdsa import EllipticCurve


class ThresholdEcdsa:
    def __init__(self):
        self.EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)
        self.alice = Alice(123)
        self.bob = Bob(123)
        self.dealer = Dealer(order=self.EC.p)
        self.pk = self.key_gen()

    def convert(self, secret_share):
        secret_curve_point = self.EC.generator * secret_share
        return secret_curve_point

    def open_curve_point(self, secret_share_point_a, secret_share_point_b):
        curve_point = (secret_share_point_a + secret_share_point_b)
        return curve_point

    def key_gen(self):
        # Generate a secret key
        sk = random.randint(0, self.EC.p)

        # Generate secret shares for both alice and bob
        secret_share_alice = random.randint(0, self.EC.p)
        secret_share_bob = (sk - secret_share_alice) % self.EC.p
        # Generate public key
        pk = self.open_curve_point(self.convert(secret_share_alice), self.convert(secret_share_bob))
        self.alice.sk_a, self.bob.sk_b = secret_share_alice, secret_share_bob

        return pk

    def user_independent_preprocessing(self):
        #Step 1

        alice = self.alice
        bob = self.bob
        alice.randomness_from_dealer, bob.randomness_from_dealer = self.dealer.create_u_v_w()

        # Step 2
        c = alice.open(alice.randomness_from_dealer[2], bob.randomness_from_dealer[2])

        #Step 3
        alice.k_inverse = alice.randomness_from_dealer[0]
        bob.k_inverse = bob.randomness_from_dealer[0]

        #Step 4
        c_inverse = pow(c, -1, self.EC.p)  # TODO: n or p
        b_a = alice.randomness_from_dealer[1]
        b_b = bob.randomness_from_dealer[1]
        alice.curve_k_a = alice.convert(b_a) * c_inverse
        bob.curve_k_b = bob.convert(b_b) * c_inverse

        # Step 5
        print("hej, user independent finish")

    def user_dependent_preprocessing(self, random_triple=None):
        alice = self.alice
        bob = self.bob

        if random_triple is not None:
            rand_alice, rand_bob = random_triple
        else:
            rand_alice, rand_bob = self.dealer.create_u_v_w()

        sk_prime_a, sk_prime_b = util.mult_two_wires(alice, bob, alice.k_inverse, bob.k_inverse, alice.sk_a, bob.sk_b,
                                                     rand_alice, rand_bob)

        alice.sk_prime_a = sk_prime_a
        bob.sk_prime_b = sk_prime_b


    def sign_message(self, message):
        self.user_independent_preprocessing()
        self.user_dependent_preprocessing()

        # Step 1
        R = self.open_curve_point(self.alice.curve_k_a, self.bob.curve_k_b)

        # Step 2
        r_x = R.x()
        r_y = R.y()

        # Step 3 - Calculate secret shares of s
        s_alice = self.alice.add_wires(self.alice.mult_with_constant(self.alice.k_inverse, util.hash_SHA256(message, self.EC)), self.alice.mult_with_constant(self.alice.sk_a, r_x))
        s_bob = self.bob.add_wires(self.bob.mult_with_constant(self.bob.k_inverse, util.hash_SHA256(message, self.EC)), self.bob.mult_with_constant(self.bob.sk_b, r_x))
        s = (s_alice + s_bob) % self.EC.p

        return r_x, s

    def verify_signature(self, message, signature, pk):
        message_hash = util.hash_SHA256(message, self.EC)
        r_x, s = signature

        s_inverse = pow(s, -1, self.EC.p)
        curve_point = (message_hash * s_inverse) % self.EC.n * self.EC.generator + (r_x * s_inverse) % self.EC.n * pk

        return r_x == curve_point.x()

