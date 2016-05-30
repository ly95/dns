import struct
import logging

QR_REQUEST = 0
QR_RESPONSE = 1

# opcode
QUERY = 0
IQUERY = 1
STATUS = 2


class Message(object):
    ID = None
    QR = None
    OPCODE = None
    AA = None
    TC = None
    RD = None
    RA = None
    Z = None
    RCODE = None
    QDCOUNT = None
    ANCOUNT = None
    NSCOUNT = None
    ARCOUNT = None

    pos = 0

    def __init__(self):
        pass

    def decode(self, data):
        self.ID = self.get16bits(self.chunk(data))
        header = self.get16bits(self.chunk(data))

        logging.debug(("message header = %d" % header))

        self.QR = (header & int('1000000000000000', 2)) >> 15
        self.OPCODE = (header & int('111100000000000', 2)) >> 11
        self.AA = (header & int('10000000000', 2)) >> 10
        self.TC = (header & int('1000000000', 2)) >> 9
        self.RD = (header & int('100000000', 2)) >> 8
        self.RA = (header & int('10000000', 2)) >> 7
        self.Z = (header & int('11110000', 2)) >> 4
        self.RCODE = header & int('1111', 2)

        self.QDCOUNT = self.get16bits(self.chunk(data))
        self.ANCOUNT = self.get16bits(self.chunk(data))
        self.NSCOUNT = self.get16bits(self.chunk(data))
        self.ARCOUNT = self.get16bits(self.chunk(data))

    def chunk(self, data):
        return data[self.pos:]

    def get16bits(self, char):
        if len(char) < 2:
            raise ("char err")

        i = struct.unpack('B', char[0])[0] << 8
        i += struct.unpack('B', char[1])[0]

        self.pos += 2

        return i

    def test(self):
        print("-------")
        print("ID = ", self.ID)
        print("QR = ", self.QR)
        print("OPCODE = ", self.OPCODE)
        print("AA = ", self.AA)
        print("TC = ", self.TC)
        print("RD = ", self.RD)
        print("RA = ", self.RA)
        print("Z = ", self.Z)
        print("RCODE = ", self.RCODE)
        print("QDCOUNT = ", self.QDCOUNT)
        print("ANCOUNT = ", self.ANCOUNT)
        print("NSCOUNT = ", self.NSCOUNT)
        print("ARCOUNT = ", self.ARCOUNT)
        print("-------")
