import unittest
from unittest import TestCase
from dealer import Dealer
from alice import Alice
from bob import Bob
from src import own_ecdsa
from util import mult_two_wires


class Test(TestCase):

    def test_mult_with_wires(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]
            alice = Alice(x_input=x)
            bob = Bob(y_input=y)
            dealer = Dealer(alice.order)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            alice_triple, bob_triple = dealer.create_u_v_w()

            zA, zB = mult_two_wires(alice, bob, alice.x_a, bob.x_b, alice.y_a, bob.y_b, alice_triple, bob_triple)

            self.assertEqual((zA + zB) % alice.order, (x * y) % alice.order)

    def test_mult_with_constant(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]

            alice = Alice(x_input=x)
            bob = Bob(y_input=y)

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

            alice = Alice(x_input=x)
            bob = Bob(y_input=y)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            zA = alice.add_with_constant(alice.x_a, 10)
            zB = bob.add_with_constant(bob.x_b)
            self.assertEqual((zA + zB) % alice.order, (alice.x_a + bob.x_b + 10) % alice.order)

            zA = alice.add_wires(alice.x_a, alice.y_a)
            zB = bob.add_wires(bob.x_b, bob.y_b)
            self.assertEqual((zA + zB) % alice.order, x + y)


    def test_convert(self):
        EC = own_ecdsa.create_generator()

        message = 40

        message2 = 59

        alice = Alice(x_input=message, EC=EC)

        bob = Bob(y_input=message2, EC=EC)

        bob.receive_input_share_from_other_participant(alice.x_b)

        secret_curve_point_bob = bob.convert(bob.x_b)

        secret_point_alice = alice.convert(alice.x_a)

        self.assertNotEqual(secret_point_alice, secret_curve_point_bob)

        message_point = alice.convert(message)

        self.assertEqual(message_point, secret_point_alice + secret_curve_point_bob)

    def test_open(self):
        EC = own_ecdsa.create_generator()

        message = 40

        message2 = 59

        alice = Alice(x_input=message, EC=EC)

        bob = Bob(y_input=message2, EC=EC)

        bob.receive_input_share_from_other_participant(alice.x_b)

        secret_curve_point_bob = bob.convert(bob.x_b)

        secret_point_alice = alice.convert(alice.x_a)

        curve_point = alice.open_curve_point(secret_curve_point_bob, secret_point_alice)

        self.assertEqual(message * EC.generator, curve_point)
