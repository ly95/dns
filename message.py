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

    def __init__(self, data):
        self.ID = self.get16bits(self.chunk(data))
        header = self.get16bits(self.chunk(data))

        logging.debug(("message header = %d" % header))

        self.QR = header & int('1000000000000000', 2)
        self.OPCODE = header & int('111100000000000', 2)
        self.AA = header & int('10000000000', 2)
        self.TC = header & int('1000000000', 2)
        self.RD = header & int('100000000', 2)
        self.RA = header & int('10000000', 2)
        self.Z = header & int('11110000', 2)
        self.RCODE = header & int('1111', 2)

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
        print("ID = %d", self.ID)
        print("QR = %d", self.QR)
        print("OPCODE = %d", self.OPCODE)
        print("AA = %d", self.AA)
        print("TC = %d", self.TC)
        print("RD = %d", self.RD)
        print("RA = %d", self.RA)
        print("Z = %d", self.Z)
        print("RCODE = %d", self.RCODE)
        print("-------")
