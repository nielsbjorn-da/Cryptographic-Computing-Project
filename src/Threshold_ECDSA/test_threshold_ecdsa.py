from unittest import TestCase
from ..Threshold_ECDSA.threshold_ecdsa import ThresholdEcdsa
from ..BeDOZa_arithmetic.dealer import Dealer


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
