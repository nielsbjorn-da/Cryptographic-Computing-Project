from unittest import TestCase
from dealer import Dealer
from util import mult_two_wires
from src.BeDOZA_arithmetic_mac.alice import Alice
from src.BeDOZA_arithmetic_mac.bob import Bob
import ecdsa
from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
from mac import Mac

class Test(TestCase):
    def setUp(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator

    def test_input_wires_mac(self):
        pass

    def test_open_with_mac(self):

        inputs = [(3, 5), (10, 20), (30, 2)]

        mac = Mac(self.order)
        alice_mac_keys = mac.Gen(len(inputs) * 2)
        bob_mac_keys = mac.Gen(len(inputs) * 2)

        for i in range(len(inputs)):
            x, y = inputs[i]
            alice = Alice(order=self.order, x_input=x)
            bob = Bob(order=self.order, y_input=y)

            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            #tags  on inputs
            alice_key1 = alice_mac_keys[i * 2]
            alice_key2 = alice_mac_keys[i * 2 + 1]
            bob_key1 = bob_mac_keys[i * 2]
            bob_key2 = bob_mac_keys[i * 2 + 1]
            print("\nkeys:", alice_key1, alice_key2)

            alice_tag_x = mac.Tag(bob_key1, alice.x_a)
            alice_tag_y = mac.Tag(bob_key2, alice.y_a)
            bob_tag_x = mac.Tag(alice_key1, bob.x_b)
            bob_tag_y = mac.Tag(alice_key2, bob.y_b)

            #test opening input
            alice_open_y = alice.open(alice.y_a, bob.y_b, alice_key2, bob_tag_y)
            self.assertEqual(alice_open_y, y)

            #add input and open

            zA, zA_tag, zA_key = alice.add_wires(alice.x_a, alice.y_a, (alice_tag_x, alice_tag_y), (alice_key1, alice_key2))
            zB, zB_tag, zB_key = bob.add_wires(bob.x_b, bob.y_b, (bob_tag_x, bob_tag_y), (bob_key1, bob_key2))

            alice_open_z = alice.open(zA, zB, zA_key, zB_tag)
            bob_open_z = bob.open(zB, zA, zB_key, zA_tag)
            self.assertEqual(alice_open_z, (zA+zB) % self.order)
            self.assertEqual(bob_open_z, (zA + zB) % self.order)

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

        mac = Mac(self.order)
        alice_mac_keys = mac.Gen(len(inputs)*2)
        bob_mac_keys = mac.Gen(len(inputs)*2)

        for i in range(len(inputs)):
            x, y = inputs[i]
            alice = Alice(order=self.order, x_input=x)
            bob = Bob(order=self.order, y_input=y)


            alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
            bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

            ''' not implemented
            zA = alice.add_with_constant(alice.x_a, 10)
            zB = bob.add_with_constant(bob.x_b)
            self.assertEqual((zA + zB) % alice.order, (alice.x_a + bob.x_b + 10) % alice.order)'''

            alice_key1 = alice_mac_keys[i*2]
            alice_key2 = alice_mac_keys[i*2+1]
            bob_key1 = bob_mac_keys[i * 2]
            bob_key2 = bob_mac_keys[i * 2 + 1]
            print("\nkeys:", alice_key1, alice_key2)

            #tag under other's key
            alice_tag_x = mac.Tag(bob_key1, alice.x_a)
            alice_tag_y = mac.Tag(bob_key2, alice.y_a)
            bob_tag_x = mac.Tag(alice_key1, bob.x_b)
            bob_tag_y = mac.Tag(alice_key2, bob.y_b)

            self.assertTrue(mac.Ver(bob_key1, alice_tag_x, alice.x_a))
            self.assertTrue(mac.Ver(alice_key1, bob_tag_x, bob.x_b))

            zA, zA_tag, zA_key = alice.add_wires(alice.x_a, alice.y_a, (alice_tag_x, alice_tag_y), (alice_key1, alice_key2))
            zB, zB_tag, zB_key = bob.add_wires(bob.x_b, bob.y_b, (bob_tag_x, bob_tag_y), (bob_key1, bob_key2))

            self.assertEqual((zA + zB) % alice.order, x + y)
            self.assertTrue(mac.Ver(zA_key, zB_tag, zB))
            self.assertTrue(mac.Ver(zB_key, zA_tag, zA))


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
