from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
from src.Threshold_ECDSA.user import User

if __name__ == '__main__':


    threshold_ECDSA_user1 = threshold_ecdsa()
    user1 = User("Alice", threshold_ECDSA_user1)
    user1.set_pk(threshold_ECDSA_user1.key_generation())

    threshold_ECDSA_user2 = threshold_ecdsa()
    user2 = User("Bob", threshold_ECDSA_user2)
    user2.set_pk(threshold_ECDSA_user2.key_generation())

    print()
    print("Beginning transfer")
    message_to_verify, r_x, s, pk = user1.transfer(100, "Bob")
    user2.receive(message_to_verify, r_x, s, pk)

    print()
    print("Beginning transfer")
    message_to_verify_2, r_x_2, s_2, pk_2 = user2.transfer(500, "Alice")
    user1.receive(message_to_verify_2, r_x_2, s_2, pk_2)


    # message = "42".encode("utf8")
    # r_x, s = threshold_ECDSA.sign(message)
    # result = threshold_ECDSA.verify(message, r_x, s, pk)
    # print(result)
