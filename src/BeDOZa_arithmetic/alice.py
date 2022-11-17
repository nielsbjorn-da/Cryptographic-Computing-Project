import random


class Alice:
    def __init__(self, order, x_input=0, randomness_from_dealer=None):
        self.secret_share_of_secret_key = None
        self.order = order
        self.randomness_from_dealer = randomness_from_dealer
        self.x_b = random.randint(0, self.order)
        self.x_a = (x_input - self.x_b)

    def set_secret_share_of_secret_key(self, secret_share_of_secret_key):
        self.secret_share_of_secret_key = secret_share_of_secret_key

    def get_secret_share_of_secret_key(self):
        return self.secret_share_of_secret_key

    def receive_input_share_from_other_participant(self, input_share_from_other_participant):
        self.y_a = input_share_from_other_participant

    def get_input_share_from_other_participant(self):
        return self.y_a

    def send_input_share_to_bob(self):
        return self.x_b

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

    def open_d_shares_to_bob(self):
        return self.d_shares

    def receive_e_shares_from_other_participant(self, e_shares_from_other_participant):
        self.e_shares_from_other_participant = e_shares_from_other_participant

    def open_e_shares_to_bob(self):
        return self.e_shares

    def output(self, bob):
        return self.output_shares ^ bob.get_output_share()

    def add_with_constant(self, x_a, c):
        return (x_a + c) % self.order

    def add_wires(self, x_a, y_a):
        return (x_a + y_a) % self.order

    def mult_with_constant(self, x_a, c):
        return x_a * c % self.order

    def open(self, x_a, x_b):
        return (x_a + x_b) % self.order
