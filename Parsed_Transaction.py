
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

    def parse(self):
      # Version: 4 bytes, little endian
      self.version = self.pop_bytes(4)
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
        txid = self.pop_bytes(32)
        # vout: 4 bytes little endian
        vout = self.pop_bytes(4)
        # scriptSigSize: 1 byte
        scriptSigSize = int(self.pop_bytes(1), 16)
        # scriptSig: scriptSigSize, big endian
        scriptSig = self.pop_bytes(scriptSigSize)
        # sequence: 4 bytes little endian
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
        amount = self.pop_bytes(8)
        # scriptPubKeySize: 1 byte
        scriptPubKeySize = int(self.pop_bytes(1), 16)
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