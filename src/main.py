import ecdsa.curves

import own_ecdsa
from BeDOZa_arithmetic.alice import Alice

if __name__ == '__main__':
    EC = own_ecdsa.create_generator()

    message = 49

    alice = Alice(message, EC=EC)


    secret_point = alice.convert(alice.x_a)
    secret_point_2 = alice.convert(alice.x_b)

    print("Secret point 1:", secret_point.x(), "Secret point 2:", secret_point_2.x())
    print((secret_point.x() + secret_point_2.x()))
    print(alice.convert(message).x())
    print("x_a:", alice.x_a, "x_b:", alice.x_b)

    assert alice.convert(message).x() % alice.EC.p == (secret_point.x() + secret_point_2.x()) % alice.EC.p
