from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
import ecdsa
from src.Threshold_ECDSA.user import User
import time

import matplotlib.pyplot as plt


# https://crypto.stackexchange.com/questions/59202/what-is-the-maximum-message-size-when-using-ecdsa-specifically-secp256k1
message = str(2**64-1).encode("utf8") #TODO: Change to something that makes more sense?

#https://stackoverflow.com/questions/52222002/what-is-the-difference-between-time-perf-counter-and-time-process-time
#This post says process_time if want to compare code efficiency

def time_threshold_ecdsa(number_of_signatures_to_generate):
    threshold_ECDSA = threshold_ecdsa()
    user1 = User("Alice", threshold_ECDSA)
    user1.set_pk(threshold_ECDSA.key_generation())
    # start = time.process_time()
    start = time.perf_counter() #Not 100% sure what to use yet.
    for i in range(0, number_of_signatures_to_generate):
        threshold_ECDSA.sign(message)

    # end = time.process_time()
    end = time.perf_counter()

    return print("Threshold ECDSA: It took " + str(end-start) + " to produce " + str(number_of_signatures_to_generate) + " signatures")


def time_library_ecdsa(number_of_signatures_to_generate):
    # SECP256k1 is the Bitcoin elliptic curve
    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    # start = time.process_time()
    start = time.perf_counter() #Not 100% sure what to use yet.
    for i in range(0, number_of_signatures_to_generate):
        sk.sign(message)

    # end = time.process_time()
    end = time.perf_counter()

    return print("Library ECDSA: It took " + str(end-start) + " to produce " + str(number_of_signatures_to_generate) + " signatures")



def comparison_of_signature_schemes():
    time_threshold_ecdsa = []
    time_library_ecdsa = []
    bitsizes = list(range(1,100))
    messages = [str(2**bitsize).encode("utf8") for bitsize in bitsizes]


    threshold_ECDSA = threshold_ecdsa()
    user1 = User("Alice", threshold_ECDSA)
    user1.set_pk(threshold_ECDSA.key_generation())

    sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)


    for i in range(0, len(messages)):
        start = time.perf_counter()
        threshold_ECDSA.sign(messages[i])
        end = time.perf_counter()
        time_threshold_ecdsa.append(end-start)

        start = time.perf_counter()
        sk.sign(messages[i])
        end = time.perf_counter()
        time_library_ecdsa.append(end-start)

    fig, ax = plt.subplots()
    fig.suptitle("Comparison between Threshold ECDSA and ECDSA")
    plt.plot(bitsizes, time_library_ecdsa, linewidth=1, label="Library ECDSA", color="b")
    plt.plot(bitsizes, time_threshold_ecdsa, linewidth=1, label="Threshold ECDSA", color="r")
    ax.set_xlabel('Bitsize of message')
    ax.set_ylabel('Time (s)')
    plt.legend()

    plt.show()
    plt.clf()




time_threshold_ecdsa(10000)
time_library_ecdsa(10000)
# comparison_of_signature_schemes()