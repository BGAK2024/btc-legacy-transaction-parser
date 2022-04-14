
class Parsed_Transaction:

    def __init__ (self, rawtransaction_hex):
      # self.data is the hex str of all the fields left to parse
      self.data = rawtransaction_hex
      self.raw = rawtransaction_hex

      self.parse()

  # pops num_bytes from front of hex string
    def pop_bytes(self, num_bytes):
      num_bytes *= 2
      field = self.data[0:num_bytes]
      self.data = self.data[num_bytes:]
      return field

    def parse(self):
      # Version: 4 bytes, little endian
      self.version = self.pop_bytes(4)
      # Input count: 1 byte
      # inputs = self.parse_inputs()
      # # Output count: 1 byte
      # outputs = self.parse_inputs()

    # def parse_inputs():

        