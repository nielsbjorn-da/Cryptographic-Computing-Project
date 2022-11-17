import random


class Dealer:

    def __init__(self, order):
        self.order = order

    def rand_mul(self):
        random_triple_for_server1 = []
        random_triple_for_server2 = []

        a = random.randint(0, self.order)
        secret_share_of_a_for_server1 = random.randint(0, self.order)
        secret_share_of_a_for_server2 = (a - secret_share_of_a_for_server1) % self.order

        b = random.randint(0, self.order)
        secret_share_of_b_for_server1 = random.randint(0, self.order)
        secret_share_of_b_for_server2 = (b - secret_share_of_b_for_server1) % self.order

        c = a * b % self.order
        secret_share_of_c_for_server1 = random.randint(0, self.order)
        secret_share_of_c_for_server2 = (c - secret_share_of_c_for_server1) % self.order

        random_triple_for_server1.append(secret_share_of_a_for_server1)
        random_triple_for_server1.append(secret_share_of_b_for_server1)
        random_triple_for_server1.append(secret_share_of_c_for_server1)

        random_triple_for_server2.append(secret_share_of_a_for_server2)
        random_triple_for_server2.append(secret_share_of_b_for_server2)
        random_triple_for_server2.append(secret_share_of_c_for_server2)

        return random_triple_for_server1, random_triple_for_server2
