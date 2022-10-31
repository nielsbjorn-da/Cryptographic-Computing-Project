import random


def xor_with_constant(input_bit, constant: int):
    return input_bit ^ constant


def create_bit_array_from_bit_string(bitstring: str):
    bit_array = []
    for i in range(len(bitstring)):
        bit_array.append(int(bitstring[i]))

    return bit_array


def btformula_from_class(x_as_bit_string, y_as_bit_string):
    x_as_bit_array = create_bit_array_from_bit_string(x_as_bit_string)
    y_as_bit_array = create_bit_array_from_bit_string(y_as_bit_string)
    return ((1 ^ (x_as_bit_array[0] & (1 ^ y_as_bit_array[0]))) & (1 ^ (x_as_bit_array[1] & (1 ^ y_as_bit_array[1])))) & (1 ^ (x_as_bit_array[2] & (1 ^ y_as_bit_array[2])))


def create_random_bit_array(length: int):
    random_bit_array = []
    for i in range(length):
        random_bit_array.append(random.randint(0,1))
    return random_bit_array


def xor_two_bit_arrays(bit_array1, bit_array2):
    result = []
    if len(bit_array1) != len(bit_array2):
        raise Exception("The two bit arrays are not of equal size")
    else:
        for i in range(len(bit_array1)):
            result.append(bit_array1[i] ^ bit_array2[i])
        return result