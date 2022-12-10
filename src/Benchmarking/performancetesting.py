from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
import src.old_code.ECDSA as own_ECDSA
import ecdsa
from src.Threshold_ECDSA.user import User
import time

import random
def create_random_messages(number_of_messages_to_generate):
    random_messages = []
    random.seed(42)
    for i in range(0, number_of_messages_to_generate):
        random_message = random.randint(0, ecdsa.SECP256k1.order)
        random_message = str(random_message).encode("utf8")
        random_messages.append(random_message)
    return random_messages

# https://stackoverflow.com/questions/52222002/what-is-the-difference-between-time-perf-counter-and-time-process-time
# Some dude says that perf_counter is preferable.
def time_signature_generation_threshold_ecdsa(messages):
    threshold_ECDSA = threshold_ecdsa()
    user1 = User("Alice", threshold_ECDSA)
    user1.set_pk(threshold_ECDSA.key_generation())
    start = time.perf_counter()
    for i in range(0, len(messages)):
        threshold_ECDSA.sign(messages[i])

    end = time.perf_counter()

    return print("Threshold ECDSA: It took " + str(end - start) + " to produce " + str(
        len(messages)) + " signatures")


def time_signature_generation_library_ecdsa(messages):
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    start = time.perf_counter()
    for i in range(0, len(messages)):
        sk.sign(messages[i])

    end = time.perf_counter()

    return print("Library ECDSA: It took " + str(end - start) + " to produce " + str(
        len(messages)) + " signatures")

def time_signature_generation_own_ecdsa(messages):
    sk, pk = own_ECDSA.key_generation()
    start = time.perf_counter()
    for i in range(0, len(messages)):
        own_ECDSA.sign(messages[i], sk)

    end = time.perf_counter()

    return print("Own ECDSA: It took " + str(end - start) + " to produce " + str(
        len(messages)) + " signatures")

random_messages = create_random_messages(10000)
time_signature_generation_threshold_ecdsa(random_messages)
time_signature_generation_library_ecdsa(random_messages)
time_signature_generation_own_ecdsa(random_messages)
