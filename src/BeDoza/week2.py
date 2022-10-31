import random
import numpy as np


truth_table = np.asarray([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1]])


blood_type_map_from_string_to_integer = {
    "000": 0,
    "001": 1,
    "010": 2,
    "011": 3,
    "100": 4,
    "101": 5,
    "110": 6,
    "111": 7,
}


class Dealer:

    def __init__(self):
        self.n = 3  # Since we are dealing with 3-bit numbers
        self.r_as_integer = random.randint(0, 2 ** self.n-1)
        self.s_as_integer = random.randint(0, 2 ** self.n-1)
        self.matrix_b = np.random.randint(2, size=(2 ** self.n, 2 ** self.n))
        self.matrix_a = np.zeros((2 ** self.n, 2 ** self.n)).astype(int)

        for i in range(2**self.n):
            for j in range(2**self.n):
                self.matrix_a[i, j] = self.matrix_b[i, j] ^ truth_table[(i - self.r_as_integer) % (2 ** self.n), (j - self.s_as_integer) % (2 ** self.n)]

    def rand_a(self):
        return self.r_as_integer, self.matrix_a

    def rand_b(self):
        return self.s_as_integer, self.matrix_b


class Alice:

    def __init__(self, x_as_bit_string: str, tuple_from_dealer):
        (r_as_integer, matrix_a) = tuple_from_dealer
        self.r_as_integer = r_as_integer
        self.matrix_a = matrix_a
        self.v = 0
        self.z_b = 0
        self.n = len(x_as_bit_string)
        self.x_as_integer = blood_type_map_from_string_to_integer[x_as_bit_string]
        self.u = (self.x_as_integer + self.r_as_integer) % (2 ** self.n)

    def send(self):
        return self.u

    def receive(self, tuple_from_bob):
        (v, z_b) = tuple_from_bob
        self.v = v
        self.z_b = z_b

    def output(self):
        z = self.matrix_a[self.u, self.v] ^ self.z_b
        return z


class Bob:

    def __init__(self, y_as_bit_string: str, tuple_from_dealer):
        (s_as_integer, matrix_b) = tuple_from_dealer
        self.s_as_integer = s_as_integer
        self.matrix_b = matrix_b
        self.u = 0
        self.z_b = 0
        self.n = len(y_as_bit_string)
        self.y_as_integer = blood_type_map_from_string_to_integer[y_as_bit_string]
        self.v = (self.y_as_integer + self.s_as_integer) % (2 ** self.n)

    def send(self):
        self.z_b = self.matrix_b[self.u, self.v]
        return self.v, self.z_b

    def receive(self, u):
        self.u = u


def test_protocol(x: str, y: str):
    dealer = Dealer()
    alice = Alice(x, dealer.rand_a())
    bob = Bob(y, dealer.rand_b())
    bob.receive(alice.send())
    alice.receive(bob.send())
    z = alice.output()
    return z


###################################################### TESTING ######################################################

#  These are just manual test, where I test each entry in the compatibility table on the Wikipedia article on blood types.
def test_protocol_on_every_possible_input():
    # All possibilities for recipient blood type "000".
    result = test_protocol("000", "000")
    assert result == 1

    result = test_protocol("000", "001")
    assert result == 0

    result = test_protocol("000", "010")
    assert result == 0

    result = test_protocol("000", "011")
    assert result == 0

    result = test_protocol("000", "100")
    assert result == 0

    result = test_protocol("000", "101")
    assert result == 0

    result = test_protocol("000", "110")
    assert result == 0

    result = test_protocol("000", "111")
    assert result == 0

    # All possibilities for recipient blood type "001".
    result = test_protocol("001", "000")
    assert result == 1

    result = test_protocol("001", "001")
    assert result == 1

    result = test_protocol("001", "010")
    assert result == 0

    result = test_protocol("001", "011")
    assert result == 0

    result = test_protocol("001", "100")
    assert result == 0

    result = test_protocol("001", "101")
    assert result == 0

    result = test_protocol("001", "110")
    assert result == 0

    result = test_protocol("001", "111")
    assert result == 0

    # All possibilities for recipient blood type "010".
    result = test_protocol("010", "000")
    assert result == 1

    result = test_protocol("010", "001")
    assert result == 0

    result = test_protocol("010", "010")
    assert result == 1

    result = test_protocol("010", "011")
    assert result == 0

    result = test_protocol("010", "100")
    assert result == 0

    result = test_protocol("010", "101")
    assert result == 0

    result = test_protocol("010", "110")
    assert result == 0

    result = test_protocol("010", "111")
    assert result == 0

    # All possibilities for recipient blood type "011".
    result = test_protocol("011", "000")
    assert result == 1

    result = test_protocol("011", "001")
    assert result == 1

    result = test_protocol("011", "010")
    assert result == 1

    result = test_protocol("011", "011")
    assert result == 1

    result = test_protocol("011", "100")
    assert result == 0

    result = test_protocol("011", "101")
    assert result == 0

    result = test_protocol("011", "110")
    assert result == 0

    result = test_protocol("011", "111")
    assert result == 0

    # All possibilities for recipient blood type "100".
    result = test_protocol("100", "000")
    assert result == 1

    result = test_protocol("100", "001")
    assert result == 0

    result = test_protocol("100", "010")
    assert result == 0

    result = test_protocol("100", "011")
    assert result == 0

    result = test_protocol("100", "100")
    assert result == 1

    result = test_protocol("100", "101")
    assert result == 0

    result = test_protocol("100", "110")
    assert result == 0

    result = test_protocol("100", "111")
    assert result == 0

    # All possibilities for recipient blood type "101".
    result = test_protocol("101", "000")
    assert result == 1

    result = test_protocol("101", "001")
    assert result == 1

    result = test_protocol("101", "010")
    assert result == 0

    result = test_protocol("101", "011")
    assert result == 0

    result = test_protocol("101", "100")
    assert result == 1

    result = test_protocol("101", "101")
    assert result == 1

    result = test_protocol("101", "110")
    assert result == 0

    result = test_protocol("101", "111")
    assert result == 0

    # All possibilities for recipient blood type "110".
    result = test_protocol("110", "000")
    assert result == 1

    result = test_protocol("110", "001")
    assert result == 0

    result = test_protocol("110", "010")
    assert result == 1

    result = test_protocol("110", "011")
    assert result == 0

    result = test_protocol("110", "100")
    assert result == 1

    result = test_protocol("110", "101")
    assert result == 0

    result = test_protocol("110", "110")
    assert result == 1

    result = test_protocol("110", "111")
    assert result == 0

    # All possibilities for recipient blood type "111".
    result = test_protocol("111", "000")
    assert result == 1

    result = test_protocol("111", "001")
    assert result == 1

    result = test_protocol("111", "010")
    assert result == 1

    result = test_protocol("111", "011")
    assert result == 1

    result = test_protocol("111", "100")
    assert result == 1

    result = test_protocol("111", "101")
    assert result == 1

    result = test_protocol("111", "110")
    assert result == 1

    result = test_protocol("111", "111")
    assert result == 1

    print("All 64 tests of the OTTT protocol passed successfully.")


test_protocol_on_every_possible_input()



