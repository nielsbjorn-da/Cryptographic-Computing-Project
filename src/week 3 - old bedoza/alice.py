from util import create_random_bit_array, xor_two_bit_arrays, xor_with_constant


class Alice:
    def __init__(self, x_as_bit_array, randomness_from_dealer):
        self.x_as_bit_array = x_as_bit_array
        self.randomness_from_dealer = randomness_from_dealer
        self.x_b = create_random_bit_array(len(x_as_bit_array))
        self.x_a = xor_two_bit_arrays(self.x_as_bit_array, self.x_b)

    def receive_input_share_from_other_participant(self, input_share_from_other_participant):
        self.input_share_from_other_participant = input_share_from_other_participant

    def get_input_share_from_other_participant(self):
        return self.input_share_from_other_participant

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

    def compute_layer1(self):
        output_share_layer_1_alice_a = xor_with_constant(self.get_input_share_from_other_participant()[0], 1)
        output_share_layer_1_alice_b = xor_with_constant(self.get_input_share_from_other_participant()[1], 1)
        output_share_layer_1_alice_r = xor_with_constant(self.get_input_share_from_other_participant()[2], 1)
        self.input_share_from_other_participant = [output_share_layer_1_alice_a, output_share_layer_1_alice_b, output_share_layer_1_alice_r]

    def compute_layer2_before_open(self):
        self.w_shares = []
        e_shares = []
        d_shares = []
        for i in range(3):
            self.u = self.randomness_from_dealer[i][0]
            self.v = self.randomness_from_dealer[i][1]
            self.w = self.randomness_from_dealer[i][2]
            self.w_shares.append(self.w)
            d_shares.append(self.x_a[i] ^ self.u)
            e_shares.append(self.input_share_from_other_participant[i] ^ self.v)

        self.set_e_shares(e_shares)
        self.set_d_shares(d_shares)

    def compute_rest_of_layer2(self):
        temp_output_shares = []
        for i in range(3):
            d = self.d_shares[i] ^ self.d_shares_from_other_participant[i]
            e = self.e_shares[i] ^ self.e_shares_from_other_participant[i]
            temp_output_shares.append(self.w_shares[i] ^ e & self.x_a[i] ^ d & self.input_share_from_other_participant[i] ^ e & d)

        self.set_output_shares(temp_output_shares)

    def compute_layer3(self):
        self.set_output_shares([xor_with_constant(self.output_shares[0], 1), xor_with_constant(self.output_shares[1], 1), xor_with_constant(self.output_shares[2], 1)])

    def compute_layer4_before_open(self):
        self.u = self.randomness_from_dealer[3][0]
        self.v = self.randomness_from_dealer[3][1]
        self.w = self.randomness_from_dealer[3][2]
        d = self.output_shares[1] ^ self.u
        e = self.output_shares[2] ^ self.v
        self.set_e_shares(e)
        self.set_d_shares(d)

    def compute_rest_of_layer4(self):
        d = self.d_shares ^ self.d_shares_from_other_participant
        e = self.e_shares ^ self.e_shares_from_other_participant
        output_share = self.w ^ e & self.output_shares[1] ^ d & self.output_shares[2] ^ e & d
        self.output_shares[1] = output_share

    def compute_layer5_before_open(self):
        self.u = self.randomness_from_dealer[4][0]
        self.v = self.randomness_from_dealer[4][1]
        self.w = self.randomness_from_dealer[4][2]
        d = self.output_shares[0] ^ self.u
        e = self.output_shares[1] ^ self.v
        self.set_e_shares(e)
        self.set_d_shares(d)

    def compute_rest_of_layer5(self):
        d = self.d_shares ^ self.d_shares_from_other_participant
        e = self.e_shares ^ self.e_shares_from_other_participant
        output_share = self.w ^ e & self.output_shares[0] ^ d & self.output_shares[1] ^ e & d
        self.set_output_shares(output_share)

    def output(self, bob):
        return self.output_shares ^ bob.get_output_share()
