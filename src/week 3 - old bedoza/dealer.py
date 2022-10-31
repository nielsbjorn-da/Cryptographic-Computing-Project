import random


class Dealer:

    def __init__(self):
        self.randomness_for_a_for_5_layers, self.randomness_for_b_for_5_layers = self.create_u_v_w_for_5_layers()


    def create_u_v_w(self):
        rand_triple_for_a = []
        rand_triple_for_b = []

        u = random.randint(0, 1)
        u_for_a = random.randint(0, 1)
        u_for_b = u ^ u_for_a

        v = random.randint(0, 1)
        v_for_a = random.randint(0, 1)
        v_for_b = v ^ v_for_a

        w = u & v
        w_for_a = random.randint(0, 1)
        w_for_b = w ^ w_for_a

        rand_triple_for_a.append(u_for_a)
        rand_triple_for_a.append(v_for_a)
        rand_triple_for_a.append(w_for_a)

        rand_triple_for_b.append(u_for_b)
        rand_triple_for_b.append(v_for_b)
        rand_triple_for_b.append(w_for_b)

        return rand_triple_for_a, rand_triple_for_b


    def create_u_v_w_for_5_layers(self):
        rand_a = []
        rand_b = []
        for i in range(5):
            rand_triple_for_a_level_i, rand_triple_for_b_level_i = self.create_u_v_w()
            rand_a.append(rand_triple_for_a_level_i)
            rand_b.append(rand_triple_for_b_level_i)
        return rand_a, rand_b


    def rand_a(self):
        return self.randomness_for_a_for_5_layers


    def rand_b(self):
        return self.randomness_for_b_for_5_layers