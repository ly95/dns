from message import Message, HEADER_OFFSET
import struct


def decode(data):
    return Query().decode(data)


class Query(Message):
    QNAME = ""
    QTYPE = None
    QCLASS = None

    def __init__(self):
        super(Query, self).__init__()

    def decode(self, data):
        super(Query, self).decode(data)

        self.QNAME = self.decode_qrname(data)
        self.QTYPE = self.get16bits(self.chunk(data))
        self.QCLASS = self.get16bits(self.chunk(data))

        return self

    def decode_qrname(self, data):
        self.pos = HEADER_OFFSET
        label = ''

        while True:
            label_length = data[self.pos]
            if label_length is 0:
                break
            self.pos += 1
            if len(label) > 0:
                label += '.'

            for i in range(0, label_length):
                label += chr(data[self.pos + i:][0])

            self.pos += label_length

        self.pos += 1

        return label
