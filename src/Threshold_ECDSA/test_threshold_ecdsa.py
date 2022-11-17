from unittest import TestCase
from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
import src.BeDOZa_arithmetic.util as util
from src.BeDOZa_arithmetic.dealer import Dealer
import ecdsa

class Test(TestCase):

    def setUp(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator
        self.dealer = Dealer(self.order)

    def test_signing(self):
        signing_protocol = threshold_ecdsa()
        message = b'hallo hallo'
        pk = signing_protocol.key_generation()
        r_x, signature = signing_protocol.sign(message)
        verify = signing_protocol.verify(message, r_x, signature, pk)
        print("Result of verification:", verify)
        self.assertEqual(verify, True)


    # Test for user_independent_preprocessing
    def test_user_independent_preprocessing(self):
        # Initialize threshold ecdsa, dealer and create random triple
        threshold = threshold_ecdsa()

        # Run method
        threshold.user_independent_preprocessing()
        random_triple_alice, random_triple_bob = self.dealer.rand_mul()

        # Open c
        c = (random_triple_alice[2] + random_triple_bob[2]) % threshold.order

        # Test curve point k for both alice and bob
        k_alice = (random_triple_alice[1] * threshold.generator) * pow(c, -1, threshold.order)
        k_bob = (random_triple_bob[1] * threshold.generator) * pow(c, -1, threshold.order)

        self.assertEqual(k_alice.x(), (threshold.convert(random_triple_alice[1]) * pow(c, -1, threshold.order)).x())
        print("first assert good")
        self.assertEqual(k_bob.x(), (threshold.convert(random_triple_bob[1]) * pow(c, -1, threshold.order)).x())

    # TODO: This test does not make much sense. Essentially just testing mult_two_wires
    # TODO: It is outcommented because a lot of fields in Alice and Bob are not necessary anymore.

    # def test_user_dependent_preprocessing(self):
    #     # Initialize threshold ecdsa, dealer and create random triple
    #     threshold = threshold_ecdsa()
    #     pk = threshold.key_generation()
    #     threshold.user_independent_preprocessing()
    #     alice, bob = threshold.alice, threshold.bob
    #     dealer = threshold.dealer
    #
    #     # Run method
    #     random_triples = dealer.rand_mul()
    #
    #     threshold.user_dependent_preprocessing(random_triple=random_triples)
    #
    #     sk1, sk2 = util.mult_two_wires(alice, bob, alice.k_inverse, bob.k_inverse, alice.sk_a, bob.sk_b,
    #                                    random_triples[0], random_triples[1])
    #
    #     self.assertEqual(alice.sk_prime_a, sk1)
    #     self.assertEqual(bob.sk_prime_b, sk2)
