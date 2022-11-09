import ecdsa.curves
from BeDOZa_arithmetic.alice import Alice
from BeDOZa_arithmetic.bob import Bob

import own_ecdsa

if __name__ == '__main__':
    EC = own_ecdsa.create_generator()

    message = 513523412513515235
    message2 = 59

    alice = Alice(message)

    bob = Bob(message2)

    bob.receive_input_share_from_other_participant(alice.x_b)

    secret_curve_point_bob = bob.convert(bob.x_b)

    secret_point_alice = alice.convert(alice.x_a)

    curve_point = alice.open_curve_point(secret_curve_point_bob, secret_point_alice)

    assert message * EC.generator == curve_point
