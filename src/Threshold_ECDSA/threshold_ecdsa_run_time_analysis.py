import ecdsa
import random
from src.BeDOZa_arithmetic.util import hash_SHA256
from src.BeDOZa_arithmetic.alice import Alice
from src.BeDOZa_arithmetic.bob import Bob
from src.BeDOZa_arithmetic.dealer import Dealer
from src.BeDOZa_arithmetic.util import mult_two_wires
from src.Threshold_ECDSA.user import User
import time
import numpy as np
import src.old_code.ECDSA as own_ECDSA


def create_random_messages(number_of_messages_to_generate):
    random_messages = []
    random.seed(42)
    for i in range(0, number_of_messages_to_generate):
        random_message = random.randint(0, ecdsa.SECP256k1.order)
        random_message = str(random_message).encode("utf8")
        random_messages.append(random_message)
    return random_messages

class timing_of_threshold_ecdsa():
    def __init__(self):
        self.order = ecdsa.curves.SECP256k1.order
        self.generator = ecdsa.curves.SECP256k1.generator
        self.alice = Alice(order=self.order)
        self.bob = Bob(order=self.order)
        self.dealer = Dealer(order=self.order)
        self.time_for_key_gen = []
        self.time_for_user_independent_preprocessing = []
        self.time_for_user_dependent_preprocessing = []
        self.time_for_message_signing = []
        self.random_triple_for_server1, self.random_triple_for_server2 = self.dealer.rand_mul()



    def key_generation(self):
        start = time.perf_counter()
        secret_key = random.randint(0, self.order)
        secret_share_of_secret_key_for_server1 = random.randint(0, self.order)
        secret_share_of_secret_key_for_server2 = (secret_key - secret_share_of_secret_key_for_server1) % self.order
        self.alice.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server1)
        self.bob.set_secret_share_of_secret_key(secret_share_of_secret_key_for_server2)
        public_key = self.open_curve_point(self.convert(secret_share_of_secret_key_for_server1),
                                           self.convert(secret_share_of_secret_key_for_server2))
        end = time.perf_counter()
        self.time_for_key_gen.append(end-start)
        return public_key

    def open(self, secret_share_for_server1, secret_share_for_server2):
        opened_value = (secret_share_for_server1 + secret_share_for_server2) % self.order
        return opened_value

    def open_curve_point(self, secret_share_of_curve_point_server1, secret_share_of_curve_point_server2):
        opened_curve_point = secret_share_of_curve_point_server1 + secret_share_of_curve_point_server2
        return opened_curve_point

    def convert(self, secret_share):
        secret_curve_point = secret_share * self.generator
        return secret_curve_point

    def user_independent_preprocessing(self):
        start = time.perf_counter()
        # Step 1
        random_triple_for_server1, random_triple_for_server2 = self.dealer.rand_mul()
        secret_share_of_a_for_server1 = random_triple_for_server1[0]
        secret_share_of_a_for_server2 = random_triple_for_server2[0]
        secret_share_of_b_for_server1 = random_triple_for_server1[1]
        secret_share_of_b_for_server2 = random_triple_for_server2[1]
        secret_share_of_c_for_server1 = random_triple_for_server1[2]
        secret_share_of_c_for_server2 = random_triple_for_server2[2]

        # Step 2
        c = self.open(secret_share_of_c_for_server1, secret_share_of_c_for_server2)

        # Step 3
        secret_share_of_k_inverse_for_server1 = secret_share_of_a_for_server1
        secret_share_of_k_inverse_for_server2 = secret_share_of_a_for_server2

        # Step 4
        c_inverse = pow(c, -1, self.order)
        secret_shared_curve_point_of_k_inverse_for_server1 = self.convert(secret_share_of_b_for_server1) * c_inverse
        secret_shared_curve_point_of_k_inverse_for_server2 = self.convert(secret_share_of_b_for_server2) * c_inverse

        # Step 5
        end = time.perf_counter()
        self.time_for_user_independent_preprocessing.append(end-start)
        return secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2

    def user_dependent_preprocessing(self):
        # Step 1
        secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2 = self.user_independent_preprocessing()
        start = time.perf_counter()
        secret_share_of_secret_key_for_server1 = self.alice.get_secret_share_of_secret_key()
        secret_share_of_secret_key_for_server2 = self.bob.get_secret_share_of_secret_key()

        # Step 2
        random_triple_for_server1, random_triple_for_server2 = self.dealer.rand_mul()
        secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = mult_two_wires(
            self.alice, self.bob,
            secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2,
            secret_share_of_secret_key_for_server1, secret_share_of_secret_key_for_server2, random_triple_for_server1,
            random_triple_for_server2)

        # Step 3
        end = time.perf_counter()
        self.time_for_user_dependent_preprocessing.append(end-start)
        return secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime

    def sign(self, message):
        secret_shared_curve_point_of_k_inverse_for_server1, secret_shared_curve_point_of_k_inverse_for_server2, secret_share_of_k_inverse_for_server1, secret_share_of_k_inverse_for_server2, secret_share_of_secret_key_for_server1_prime, secret_share_of_secret_key_for_server2_prime = self.user_dependent_preprocessing()
        start = time.perf_counter()
        # Step 1
        R = self.open_curve_point(secret_shared_curve_point_of_k_inverse_for_server1,
                                  secret_shared_curve_point_of_k_inverse_for_server2)

        # Step 2
        r_x = R.x()

        # Step 3
        secret_share_of_signature_for_server1 = (hash_SHA256(message,
                                                             self.order) * secret_share_of_k_inverse_for_server1) + (
                                                            r_x * secret_share_of_secret_key_for_server1_prime)
        secret_share_of_signature_for_server2 = (hash_SHA256(message,
                                                             self.order) * secret_share_of_k_inverse_for_server2) + (
                                                            r_x * secret_share_of_secret_key_for_server2_prime)

        # Step 4
        s = self.open(secret_share_of_signature_for_server1, secret_share_of_signature_for_server2)
        end = time.perf_counter()
        self.time_for_message_signing.append(end-start)
        return r_x, s

    def verify(self, message, r_x, s, pk):
        message_hash = hash_SHA256(message, self.order)
        s_inverse = pow(s, -1, self.order)
        y = message_hash * self.generator + r_x * pk
        curve_point = s_inverse * y
        return r_x == curve_point.x()


if __name__ == '__main__':
    number_of_messages = 100
    random_messages = create_random_messages(number_of_messages)
    threshold_ECDSA = timing_of_threshold_ecdsa()

    for i in range(0, len(random_messages)):
        threshold_ECDSA.key_generation()
        threshold_ECDSA.sign(random_messages[i])

    time_for_key_gen = np.array(threshold_ECDSA.time_for_key_gen)
    time_for_user_independent_preprocessing = np.array(threshold_ECDSA.time_for_user_independent_preprocessing)
    time_for_user_dependent_preprocessing = np.array(threshold_ECDSA.time_for_user_dependent_preprocessing)
    time_for_message_signing = np.array(threshold_ECDSA.time_for_message_signing)
    total_time = np.array((time_for_key_gen + time_for_user_independent_preprocessing + time_for_user_dependent_preprocessing + time_for_message_signing))

    time_for_key_gen *= 1000
    time_for_user_independent_preprocessing *= 1000
    time_for_user_dependent_preprocessing *= 1000
    time_for_message_signing *= 1000
    total_time *= 1000

    avg_time_for_key_gen = np.round(np.average(time_for_key_gen), 2)
    avg_time_for_user_independent_preprocessing = np.round(np.average(time_for_user_independent_preprocessing), 2)
    avg_time_for_user_dependent_preprocessing = np.round(np.average(time_for_user_dependent_preprocessing), 2)
    avg_time_for_message_signing = np.round(np.average(time_for_message_signing), 2)
    avg_total_time = np.round(np.average(total_time), 2)

    print("Average time for key generation: " + str(avg_time_for_key_gen))
    print("Average time for user independent preprocessing: " + str(avg_time_for_user_independent_preprocessing))
    print("Average time for user dependent preprocessing: " + str(avg_time_for_user_dependent_preprocessing))
    print("Average time for message signing: " + str(avg_time_for_message_signing))
    print("Average time in total: " + str(avg_total_time))


    #Comparison of message signing vs. ECDSA
    print()
    print("Comparison of message signing in Threshold ECDSA vs. ECDSA")
    # sk, pk = own_ECDSA.key_generation()

    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    start = time.perf_counter()
    for i in range(0, len(random_messages)):
        sk.sign(random_messages[i]) #library ECDSA
        # own_ECDSA.sign(random_messages[i], sk) #own ECDSA

    end = time.perf_counter()

    average_time_for_ECDSA_signing = (end-start)*1000/number_of_messages

    print("Average time for message signing Threshold ECDSA: " + str(avg_time_for_message_signing))
    print("Average time for message signing ECDSA: " + str(average_time_for_ECDSA_signing))



