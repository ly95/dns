from message import Message
import struct


class Query(Message):
    QNAME = ""
    QTYPE = None
    QCLASS = None

    def __init__(self):
        super(Query, self).__init__()

    def decode(self, data):
        if '163' not in data:
            return

        super(Query, self).decode(data)

        self.QNAME = self.decode_qrname(data)
        self.QTYPE = self.get16bits(self.chunk(data))
        self.QCLASS = self.get16bits(self.chunk(data))

    def decode_qrname(self, data):
        self.pos = 12
        label = ''

        while True:
            label_length = int(struct.unpack('B', data[self.pos])[0])
            if label_length is 0:
                break
            self.pos += 1
            if len(label) > 0:
                label += '.'
            label += data[self.pos:self.pos + label_length]
            self.pos += label_length

        self.pos += 1

        return label

    def test(self):
        super(Query, self).test()

        print("QNAME = ", self.QNAME)
        print("QTYPE = ", self.QTYPE)
        print("QCLASS = ", self.QCLASS)
        print("-------")
