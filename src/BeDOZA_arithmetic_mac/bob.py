import random
import mac

class Bob:

    def __init__(self, order, y_input=0, randomness_from_dealer=None):
        self.secret_share_of_secret_key = None
        self.order = order
        self.randomness_from_dealer = randomness_from_dealer
        self.y_b = random.randint(0, self.order)
        self.y_a = (y_input - self.y_b)
        self.mac = mac.Mac(order)

    def set_secret_share_of_secret_key(self, secret_share_of_secret_key):
        self.secret_share_of_secret_key = secret_share_of_secret_key

    def get_secret_share_of_secret_key(self):
        return self.secret_share_of_secret_key

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

    def add_wires(self, x_b, y_b, tags, keys):
        new_tag = sum(tags) % self.order
        new_key = (keys[0][0], (keys[0][1] + keys[1][1]) % self.order)
        return (x_b + y_b) % self.order, new_tag, new_key

    def mult_with_constant(self, x_b, c):
        return x_b * c % self.order

    def open(self, own_share, share_from_other, own_key, tag_from_other):
        if self.mac.Ver(own_key, tag_from_other, share_from_other):
            return (own_share + share_from_other) % self.order
        else:
            raise Exception("Mac verification failed in open")
