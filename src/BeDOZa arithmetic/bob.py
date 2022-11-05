import random

class Bob:

    def __init__(self, y_input, order, randomness_from_dealer=None):
        self.randomness_from_dealer = randomness_from_dealer
        self.order = order
        self.y_a = random.randint(0, self.order)
        self.y_b = (y_input - self.y_a) % self.order

    def receive_input_share_from_other_participant(self, input_share_from_other_participant):
        self.x_b = input_share_from_other_participant

    def get_input_share_from_other_participant(self):
        return self.x_b

    def send_input_share_to_alice(self):
        return self.y_a

    def set_e_shares(self, e_shares):
        self.e_shares = e_shares

    def set_d_shares(self, d_shares):
        self.d_shares = d_shares

    def get_e_shares(self):
        return self.e_shares

    def get_d_shares(self):
        return self.d_shares

    def set_output_shares(self, output_shares):
        self.output_shares = output_shares

    def receive_d_shares_from_other_participant(self, d_shares_from_other_participant):
        self.d_shares_from_other_participant = d_shares_from_other_participant

    def open_d_shares_to_alice(self):
        return self.d_shares

    def receive_e_shares_from_other_participant(self, e_shares_from_other_participant):
        self.e_shares_from_other_participant = e_shares_from_other_participant

    def open_e_shares_to_alice(self):
        return self.e_shares

    def get_output_share(self):
        return self.output_shares

    def add_with_constant(self, x_b):
        return x_b

    def add_wires(self, x_b, y_b):
        return (x_b + y_b) % self.order

    def mult_with_constant(self, x_b, c):
        return x_b * c % self.order

    def open(self, x_b, x_a):
        return (x_b + x_a) % self.order
