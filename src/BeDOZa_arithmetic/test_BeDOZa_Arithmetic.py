from unittest import TestCase
from dealer import Dealer
from util import mult_two_wires
from src.BeDOZa_arithmetic.alice import Alice
from src.BeDOZa_arithmetic.bob import Bob
import ecdsa
from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa

class Test(TestCase):
    def setUp(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator

    def test_mult_with_wires(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]
            alice = Alice(order=self.order, x_input=x)
            bob = Bob(order=self.order, y_input=y)
            dealer = Dealer(self.order)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            alice_triple, bob_triple = dealer.rand_mul()

            zA, zB = mult_two_wires(alice, bob, alice.x_a, bob.x_b, alice.y_a, bob.y_b, alice_triple, bob_triple)

            self.assertEqual((zA + zB) % alice.order, (x * y) % alice.order)

    def test_mult_with_constant(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]

            alice = Alice(order=self.order, x_input=x)
            bob = Bob(order=self.order, y_input=y)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            c = 13
            zA = alice.mult_with_constant(alice.x_a, c)
            zB = bob.mult_with_constant(bob.x_b, c)

            self.assertEqual((zA + zB) % alice.order, (x * c) % bob.order)

    def test_add(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]


        for i in range(len(inputs)):
            x, y = inputs[i]

            alice = Alice(order=self.order, x_input=x)
            bob = Bob(order=self.order, y_input=y)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            zA = alice.add_with_constant(alice.x_a, 10)
            zB = bob.add_with_constant(bob.x_b)
            self.assertEqual((zA + zB) % alice.order, (alice.x_a + bob.x_b + 10) % alice.order)

            zA = alice.add_wires(alice.x_a, alice.y_a)
            zB = bob.add_wires(bob.x_b, bob.y_b)
            self.assertEqual((zA + zB) % alice.order, x + y)


    def test_convert(self):

        message = 40

        message2 = 59

        alice = Alice(order=self.order, x_input=message)

        bob = Bob(order=self.order, y_input=message2)

        bob.receive_input_share_from_other_participant(alice.x_b)

        threshold_ECDSA = threshold_ecdsa()

        secret_curve_point_bob = threshold_ECDSA.convert(bob.x_b)

        secret_point_alice = threshold_ECDSA.convert(alice.x_a)

        self.assertNotEqual(secret_point_alice, secret_curve_point_bob)

        message_point = threshold_ECDSA.convert(message)

        self.assertEqual(message_point, secret_point_alice + secret_curve_point_bob)

    def test_open(self):

        message = 40

        message2 = 59

        alice = Alice(order=self.order, x_input=message)

        bob = Bob(order=self.order, y_input=message2)

        bob.receive_input_share_from_other_participant(alice.x_b)

        threshold_ECDSA = threshold_ecdsa()

        secret_curve_point_bob = threshold_ECDSA.convert(bob.x_b)

        secret_point_alice = threshold_ECDSA.convert(alice.x_a)

        curve_point = threshold_ECDSA.open_curve_point(secret_curve_point_bob, secret_point_alice)

        self.assertEqual(message * self.generator, curve_point)
