import threshold_ecdsa

class User:
    def __init__(self, name):
        self.wallet = 1000
        self.name = name
        self.sk = 123
        self.pk = 321
        self.threshold_ecdsa = threshold_ecdsa()

    def transfer(self):
        pass

    def sign(self, message):
        threshold_ecdsa.sign_message(message)
        pass