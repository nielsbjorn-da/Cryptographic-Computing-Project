import ecdsa

def number_of_bytes_in_number(a):
    i = 0

    while(a > 0):
        a = a >> 8;
        i += 1;

    print (i)

number_of_bytes_in_number(ecdsa.curves.SECP256k1.order)