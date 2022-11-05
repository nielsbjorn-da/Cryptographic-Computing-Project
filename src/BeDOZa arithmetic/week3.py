from dealer import Dealer
from alice import Alice
from bob import Bob
from util import mult_two_wires

def test_mult_with_wires(x,y):
    # Initialization
    order_p = 50
    print(f"\nGroup: Z_{order_p}")
    alice = Alice(x, order=order_p)
    bob = Bob(y, order=order_p)
    dealer = Dealer(order=order_p)

    alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
    bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

    print("input:", x, y)

    print("xA, xB", alice.x_a, bob.x_b)
    print("yA, yB", alice.y_a, bob.y_b)

    print("order", dealer.order)
    alice_triple, bob_triple = dealer.create_u_v_w()
    print(alice_triple)
    print(bob_triple)
    print(alice.open(alice_triple[0], bob_triple[0]))
    print(alice.open(alice_triple[1], bob_triple[1]))
    print(alice.open(alice_triple[2], bob_triple[2]))
    print(alice.open(alice_triple[0], bob_triple[0]) * alice.open(alice_triple[1], bob_triple[1]) % order_p)

    zA, zB = mult_two_wires(alice, bob, alice.x_a, bob.x_b, alice.y_a, bob.y_b, alice_triple, bob_triple)
    print("mult with wires:", x, y, (zA + zB) % order_p)
    assert (zA + zB) % order_p == (x * y) % order_p

def test_mult_with_constant(x,y):
    # Initialization
    order_p = 50
    print(f"\nGroup: Z_{order_p}")
    alice = Alice(x, order=order_p)
    bob = Bob(y, order=order_p)

    alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
    bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())

    print("input:", x, y)

    print("xA, xB", alice.x_a, bob.x_b)
    print("yA, yB", alice.y_a, bob.y_b)

    c = 13
    zA = alice.mult_with_constant(alice.x_a, c)
    zB = bob.mult_with_constant(bob.x_b, c)
    print("mult with constant:", x, c, (zA+zB) % order_p)
    assert (zA + zB) % order_p == (x * c) % order_p

def test_add(x, y):
    # Initialization
    order_p = 50
    alice = Alice(x, order=order_p)
    bob = Bob(y, order=order_p)

    alice.receive_input_share_from_other_participant(bob.send_input_share_to_alice())
    bob.receive_input_share_from_other_participant(alice.send_input_share_to_bob())


    print("\ninput:", x, y)
    print("xA, xB", alice.x_a, bob.x_b)
    print("yA, yB", alice.y_a, bob.y_b)

    zA = alice.add_with_constant(alice.x_a, 10)
    zB = bob.add_with_constant(bob.x_b)
    print("add with constant 10", alice.x_a + bob.x_b, zA, zB, zA + zB)
    assert (zA+zB) % order_p == (alice.x_a + bob.x_b + 10) % order_p

    zA = alice.add_wires(alice.x_a, alice.y_a)
    zB = bob.add_wires(bob.x_b, bob.y_b)
    print("add input wires", zA, zB, (zA+zB) % order_p, (x+y) % order_p)
    assert (zA + zB) % order_p == x+y

test_add(3,5)
test_add(10, 20)
test_add(30,2)

test_mult_with_constant(3,5)
test_mult_with_constant(10,20)
test_mult_with_constant(30,2)

test_mult_with_wires(3,5)
test_mult_with_wires(10,20)
test_mult_with_wires(30,2)