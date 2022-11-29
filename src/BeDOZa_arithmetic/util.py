from src.BeDOZa_arithmetic.alice import Alice
from src.BeDOZa_arithmetic.bob import Bob
from Crypto.Hash import SHA256


def mult_two_wires(server1: Alice, server2: Bob, x_a, x_b, y_a, y_b, rand_triple_a, rand_triple_b):
    d_a = server1.add_wires(x_a, rand_triple_a[0])
    e_a = server1.add_wires(y_a, rand_triple_a[1])

    d_b = server2.add_wires(x_b, rand_triple_b[0])
    e_b = server2.add_wires(y_b, rand_triple_b[1])

    d_opened_a = server1.open(d_a, d_b)
    e_opened_a = server1.open(e_a, e_b)

    d_opened_b = server2.open(d_b, d_a)
    e_opened_b = server2.open(e_b, e_a)

    w_a = rand_triple_a[2]
    mult_1_a = server1.mult_with_constant(x_a, e_opened_a)
    mult_2_a = server1.mult_with_constant(y_a, d_opened_a)
    z_a = (w_a + mult_1_a + mult_2_a - (e_opened_a * d_opened_a))  # % self.alice.order

    w_b = rand_triple_b[2]
    mult_1_b = server2.mult_with_constant(x_b, e_opened_b)
    mult_2_b = server2.mult_with_constant(y_b, d_opened_b)
    z_b = (w_b + mult_1_b + mult_2_b)  # % self.bob.order #no e*d?
    return z_a, z_b


def hash_SHA256(message, order):
    h = SHA256.new()
    h.update(message)
    e = h.hexdigest()
    e = bin(int(e, 16))[2:]
    # L_n = order.bit_length()
    # z = e[:L_n]
    # z = int(z)
    return int(e)
