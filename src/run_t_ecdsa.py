from t_ecdsa import threshold_ecdsa

if __name__ == '__main__':
    threshold_ECDSA = threshold_ecdsa()
    pk = threshold_ECDSA.key_generation()
    message = "42".encode("utf8")
    r_x, s = threshold_ECDSA.sign(message)
    result = threshold_ECDSA.verify(message, r_x, s, pk)
    print(result)

