import random
import mac

class Dealer:

    def __init__(self, order):
        self.order = order
        self.mac = mac.Mac(order)

    def make_random_share_with_macs(self, key_alice, key_bob):
        r = random.randint(0, self.order)
        r_bob_share = random.randint(0, r)
        r_alice_share = r - r_bob_share
        tag_alice = self.mac.Tag(key_bob, r_alice_share)
        tag_bob = self.mac.Tag(key_alice, r_bob_share)
        return (r_alice_share, tag_alice), (r_bob_share, tag_bob)


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
