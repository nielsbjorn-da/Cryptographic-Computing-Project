import random


class Dealer:

    def __init__(self, order):
        #self.randomness_for_a_for_5_layers, self.randomness_for_b_for_5_layers = self.create_u_v_w_for_5_layers()
        self.order = order


    def create_u_v_w(self):
        rand_triple_for_a = []
        rand_triple_for_b = []

        u = random.randint(0, self.order)
        u_for_a = random.randint(0, self.order)
        u_for_b = (u - u_for_a) % self.order

        v = random.randint(0, self.order)
        v_for_a = random.randint(0, self.order)
        v_for_b = (v - v_for_a) % self.order

        w = u * v % self.order
        w_for_a = random.randint(0, self.order)
        w_for_b = (w - w_for_a) % self.order

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