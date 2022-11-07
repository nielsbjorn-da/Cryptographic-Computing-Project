import unittest
from unittest import TestCase
from dealer import Dealer
from alice import Alice
from bob import Bob
from util import mult_two_wires


class Test(TestCase):

    def test_mult_with_wires(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]
            order_p = 50
            print(f"\nGroup: Z_{order_p}")
            alice = Alice(x, order=order_p)
            bob = Bob(y, order=order_p)
            dealer = Dealer(order=order_p)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            alice_triple, bob_triple = dealer.create_u_v_w()

            zA, zB = mult_two_wires(alice, bob, alice.x_a, bob.x_b, alice.y_a, bob.y_b, alice_triple, bob_triple)

            self.assertEqual((zA + zB) % order_p,  (x * y) % order_p)

    def test_mult_with_constant(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]

            order_p = 50

            alice = Alice(x, order=order_p)
            bob = Bob(y, order=order_p)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            c = 13
            zA = alice.mult_with_constant(alice.x_a, c)
            zB = bob.mult_with_constant(bob.x_b, c)

            self.assertEqual((zA + zB) % order_p, (x * c) % order_p)


    def test_add(self):
        # Initialization
        inputs = [(3, 5), (10, 20), (30, 2)]

        for i in range(len(inputs)):
            x, y = inputs[i]

            order_p = 50
            alice = Alice(x, order=order_p)
            bob = Bob(y, order=order_p)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            zA = alice.add_with_constant(alice.x_a, 10)
            zB = bob.add_with_constant(bob.x_b)
            self.assertEqual((zA + zB) % order_p, (alice.x_a + bob.x_b + 10) % order_p)

            zA = alice.add_wires(alice.x_a, alice.y_a)
            zB = bob.add_wires(bob.x_b, bob.y_b)
            self.assertEqual((zA + zB) % order_p, x + y)