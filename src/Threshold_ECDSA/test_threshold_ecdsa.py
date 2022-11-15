from unittest import TestCase

from ..BeDOZa_arithmetic import dealer
from ..Threshold_ECDSA.threshold_ecdsa import ThresholdEcdsa
import src.BeDOZa_arithmetic.util as util


class Test(TestCase):
    # Test for user_independent_preprocessing
    def test_user_independent_preprocessing(self):
        # Initialize threshold ecdsa, dealer and create random triple
        threshold = ThresholdEcdsa()

        # Run method
        threshold.user_independent_preprocessing()
        random_triple_alice = threshold.alice.randomness_from_dealer
        random_triple_bob = threshold.bob.randomness_from_dealer

        # Open c
        c = (random_triple_alice[2] + random_triple_bob[2]) % threshold.EC.p

        # Test alice and bob k-inverse
        self.assertEqual(threshold.alice.k_inverse, random_triple_alice[0])
        self.assertEqual(threshold.bob.k_inverse, random_triple_bob[0])

        # Test curve point k for both alice and bob
        k_alice = (random_triple_alice[1] * threshold.EC.generator) * pow(c, -1, threshold.EC.p)
        k_bob = (random_triple_bob[1] * threshold.EC.generator) * pow(c, -1, threshold.EC.p)

        self.assertEqual(k_alice, threshold.alice.curve_k_a)
        self.assertEqual(k_bob, threshold.bob.curve_k_b)

    def test_user_dependent_preprocessing(self):
        # Initialize threshold ecdsa, dealer and create random triple
        threshold = ThresholdEcdsa()
        pk = threshold.key_gen()
        threshold.user_independent_preprocessing()
        alice, bob = threshold.alice, threshold.bob
        dealer = threshold.dealer

        # Run method
        random_triples = dealer.create_u_v_w()

        threshold.user_dependent_preprocessing(random_triple=random_triples)

        sk1, sk2 = util.mult_two_wires(alice, bob, alice.k_inverse, bob.k_inverse, alice.sk_a, bob.sk_b,
                                       random_triples[0], random_triples[1])

        self.assertEqual(alice.sk_prime_a, sk1)
        self.assertEqual(bob.sk_prime_b, sk2)
