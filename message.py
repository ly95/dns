"""
   Copyright 2016 Yang Lin <linyang95@aol.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from error import DecodeException

HEADER_OFFSET = 12

QR_REQUEST = 0
QR_RESPONSE = 1

# opcode
QUERY = 0
IQUERY = 1
STATUS = 2


class Message(object):
    ID = None
    QR = None
    OPCODE = 0
    AA = 0
    TC = 0
    RD = 0
    RA = 0
    Z = 0
    RCODE = None
    QDCOUNT = 0
    ANCOUNT = 0
    NSCOUNT = 0
    ARCOUNT = 0

    pos = 0

    def __init__(self):
        pass

    def decode(self, data):
        self.ID = self.get16bits(self.chunk(data))
        header = self.get16bits(self.chunk(data))

        self.QR = header >> 15
        self.OPCODE = header >> 11
        self.AA = header >> 10
        self.TC = header >> 9
        self.RD = header >> 8
        self.RA = header >> 7
        self.Z = header >> 4
        self.RCODE = header & int('1111', 2)

        self.QDCOUNT = self.get16bits(self.chunk(data))
        self.ANCOUNT = self.get16bits(self.chunk(data))
        self.NSCOUNT = self.get16bits(self.chunk(data))
        self.ARCOUNT = self.get16bits(self.chunk(data))

    def chunk(self, data):
        return data[self.pos:]

    def get16bits(self, char):
        if len(char) < 2:
            raise DecodeException("char err")

        i = char[0] << 8
        i += char[1]

        self.pos += 2

        return i

    def make_flages(self):
        # 8 bits
        flags = self.QR << 15
        flags += self.OPCODE << 14
        flags += self.AA << 10
        flags += self.TC << 9
        flags += self.RD << 8

        # 8 bits
        flags += self.RA << 7
        flags += self.Z << 4
        flags += self.RCODE

        return flags
