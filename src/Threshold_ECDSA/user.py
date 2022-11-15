from threshold_ecdsa import ThresholdEcdsa

class User:
    def __init__(self, name):
        self.wallet = 1000
        self.name = name
        self.sk = 123
        self.pk = 321
        self.threshold_ecdsa = ThresholdEcdsa()

    def transfer(self):
        pass

    def sign(self, message):
        self.threshold_ecdsa.sign_message(message)
        pass

