import random

import ecdsa

from src.own_ecdsa import EllipticCurve


class Bob:

    def __init__(self, y_input=0, EC=EllipticCurve(generator=ecdsa.curves.SECP256k1.generator),  randomness_from_dealer=None):
        self.EC = EC
        self.randomness_from_dealer = randomness_from_dealer
        self.order = self.EC.p
        self.y_b = random.randint(0, self.order)
        self.y_a = (y_input - self.y_b)
        self.k_inverse = None
        self.sk_b = None


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

    def add_wires(self, x_b: int, y_b: int):
        return (x_b + y_b) % self.order

    def mult_with_constant(self, x_b, c):
        return x_b * c % self.order

    def open(self, x_b, x_a):
        return (x_b + x_a) % self.order

    def convert(self, secret_share):
        secret_curve_point = self.EC.generator * secret_share
        return secret_curve_point

    def open_curve_point(self, secret_share_point_a, secret_share_point_b):
        curve_point = (secret_share_point_a + secret_share_point_b)
        return curve_point
