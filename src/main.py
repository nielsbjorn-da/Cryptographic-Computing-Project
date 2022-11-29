from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
from src.Threshold_ECDSA.user import User

if __name__ == '__main__':
    threshold_ECDSA = threshold_ecdsa()
    #TODO: Protocol should hold a dictionary or something on who has what keys.

    user1 = User("Alice", threshold_ECDSA)
    user1.set_pk(threshold_ECDSA.key_generation())

    user2 = User("Bob", threshold_ECDSA)

    message_to_verify, r_x, s, pk = user1.transfer(100, "Bob")
    user2.receive(message_to_verify, r_x, s, pk)


    # message = "42".encode("utf8")
    # r_x, s = threshold_ECDSA.sign(message)
    # result = threshold_ECDSA.verify(message, r_x, s, pk)
    # print(result)
