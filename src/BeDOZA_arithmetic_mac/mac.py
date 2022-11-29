import random

class Mac:

    def __init__(self, order):
        self.order = order

    def Gen(self, number_of_macs):
        constant_key_part = random.randint(0, self.order)
        keys = []
        for i in range(number_of_macs):
            random_key_part = random.randint(0, self.order)
            keys.append((constant_key_part, random_key_part))
        return keys

    def Tag(self, key, message):
        return (key[0] * message + key[1] ) % self.order

    def Ver(self, key, tag, message):
        return tag == self.Tag(key, message)


if __name__ == '__main__':
    mac = Mac(27364274)
    keys = mac.Gen(3)
    messages = [12314,5653463, 23523]
    for i in range(len(messages)):
        tag = mac.Tag(keys[i], messages[i])
        print("Message: {}, Key: {}, Mac: {}".format(messages[i], keys[i], tag))
        assert mac.Ver(keys[i], tag, messages[i]) # positive test
        if i > 0:
            assert not mac.Ver(keys[i], mac.Tag(keys[i-1], messages[i]), messages[i]) # negative test
