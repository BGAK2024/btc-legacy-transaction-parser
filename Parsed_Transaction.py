
class Parsed_Transaction:

    def __init__ (self, rawtransaction_hex):
        self.data = rawtransaction_hex

        self.parse()

    def parse(self):

        