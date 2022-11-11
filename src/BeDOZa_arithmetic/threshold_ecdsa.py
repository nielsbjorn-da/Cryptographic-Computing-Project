import random

import ecdsa
from bob import Bob
from alice import Alice
from dealer import Dealer
from util import mult_two_wires

from src.own_ecdsa import EllipticCurve


class threshold_ecdsa():
    def __init__(self):
        self.EC = EllipticCurve(generator=ecdsa.curves.SECP256k1.generator)
        sk_a, sk_b, pk = self.key_gen()
        self.alice = Alice()
        self.alice.sk_a = sk_a
        self.bob = Bob()
        self.bob.sk_b = sk_b
        self.dealer = Dealer

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

        return secret_share_alice, secret_share_bob, pk

    def user_independent_preprocessing(self):
        #Step 1
        dealer = Dealer(order=self.EC.p)
        alice = self.alice
        bob = self.bob
        alice.randomness_from_dealer, bob.randomness_from_dealer = dealer.create_u_v_w()

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

        #Step 5
        print("hej, user independent finish")

    def user_dependent_preprocessing(self):
        alice = self.alice
        bob = self.bob
        rand_alice, rand_bob = self.dealer.create_u_v_w()
        sk_prime_a, sk_prime_b = mult_two_wires(alice, bob, alice.k_inverse, bob.k_inverse, alice.sk_a, bob.sk_b, rand_alice, rand_bob)
        
        alice.sk_prime_a = sk_prime_a
        bob.sk_prime_b = sk_prime_b

    def sign_message(self, message):
        self.user_independent_preprocessing()
        self.user_dependent_preprocessing()
        pass
