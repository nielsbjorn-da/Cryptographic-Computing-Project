from src.Threshold_ECDSA.threshold_ecdsa import threshold_ecdsa
import json
class User:
    def __init__(self, id, protocol: threshold_ecdsa):
        self.protocol = protocol
        # self.id = str(random.randint(1, 100000000)) # TODO: Unique ID - how?
        self.id = id # TODO: Fake it: They choose their own IDs
        self.wallet = 1000
        self.pk = None

    def transfer(self, amount, to_id):
        print(self.wallet)
        self.wallet -= amount
        amount_as_string = str(amount)

        #NOTE: We are not using the IDs right now.
        to_id_as_string = str(to_id)
        from_id_as_string = str(self.id)
        message = '{' + '"amount": ' + amount_as_string + ', "to_id": ' + '"' + to_id_as_string + '"' + ', "from_id": ' + '"' + from_id_as_string + '"' + '}'
        message = message.encode("utf8")
        r_x, s = self.protocol.sign(message)
        print(self.wallet)
        print("----------")
        return message, r_x, s, self.pk

    def receive(self, message, r_x, s, pk):
        print(self.wallet)
        result = self.protocol.verify(message, r_x, s, pk)
        message_as_json_object = json.loads(message)
        amount = message_as_json_object["amount"]

        #NOTE: We are not using the IDs.
        to_id_as_string = message_as_json_object["to_id"]
        from_id_as_string = message_as_json_object["from_id"]
        if result:
            self.wallet = self.wallet + amount
        print(self.wallet)


    def set_pk(self, pk):
        self.pk = pk
