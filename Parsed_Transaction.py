import helpers

class Parsed_Transaction:

    def __init__ (self, rawtransaction_hex):
      # self.data is the hex str of all the fields left to parse
      self.data = rawtransaction_hex
      self.raw = rawtransaction_hex
      self.version = ''
      self.input_count = ''
      self.inputs = []
      self.output_count = ''
      self.outputs = []
      self.locktime = ''

      self.parse()

  # pops num_bytes from front of hex string
    def pop_bytes(self, num_bytes):
      num_bytes *= 2
      field = self.data[0:num_bytes]
      self.data = self.data[num_bytes:]
      return field


    # Compact field logic
    # if the number <= 252 ---> Put 1 byte
    # if the number is more than 252 than the first byte tells you how many more bytes to read off
    def compact_field_len(self):
      n = int(self.pop_bytes(1), 16)
      
      if n <= 252:
        return n

      else:
        n = 2 ** (n - 252)
        return n
      

    def parse(self):
      # Version: 4 bytes, little endian
      self.version = int(helpers.flip_endian(self.pop_bytes(4)), 16)
      # Input count: 1 byte
      self.input_count = int(self.pop_bytes(1), 16)
      # Parse out inputs
      self.inputs = self.parse_inputs(self.input_count)
      # Output count: 1 byte
      self.output_count = int(self.pop_bytes(1), 16)
      self.outputs = self.parse_outputs(self.output_count)
      # Locktime: 4 bytes, little endian
      self.locktime = self.pop_bytes(4)

    def parse_inputs(self, num):
      inputs = []

      for x in range(num):
        # txid: 32 bytes little endian
        txid = helpers.flip_endian(self.pop_bytes(32))
        # vout: 4 bytes little endian
        vout = int(helpers.flip_endian(self.pop_bytes(4)), 16)
        # scriptSigSize: 1 byte
        scriptSigSize = self.compact_field_len()
        # scriptSig: scriptSigSize, big endian
        scriptSig = self.pop_bytes(scriptSigSize)
        # sequence: 4 bytes
        sequence = self.pop_bytes(4)

        # Create input and append to inputs list
        input = {
          'txid': txid,
          'vout': vout,
          'scriptSigSize': scriptSigSize,
          'scriptSig': scriptSig,
          'sequence': sequence
        }
        inputs.append(input)

      return inputs

    def parse_outputs(self, num):
      outputs = []

      for x in range(num):
        # Amount: 8 bytes little endian
        amount = int(helpers.flip_endian(self.pop_bytes(8)), 16)
        # scriptPubKeySize: 1 byte
        scriptPubKeySize = self.compact_field_len()
        # scriptPubKey: scriptPubKeySize, big endian
        scriptPubKey = self.pop_bytes(scriptPubKeySize)

        # Create output and append to outputs list
        output = {
          'amount': amount,
          'scriptPubKeySize': scriptPubKeySize,
          'scriptPubKey': scriptPubKey
        }
        outputs.append(output)

      return outputs

    def print_info(self):
      return {
        'Version': self.version,
        'Input Count': self.input_count,
        'Inputs': self.inputs,
        'Output Count': self.output_count,
        'Outputs': self.outputs,
        'Locktime': self.locktime,
        'Remaining': self.data
      }