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

from message import Message, HEADER_OFFSET

CODE_OK = 0
CODE_FormatError = 1
CODE_ServerFailure = 2
CODE_NameError = 3
CODE_NotImplemented = 4
CODE_Refused = 5


class Response(Message):
    QR = 1  # It's a response
    QNAME = None
    NAME = None
    TYPE = 0
    CLASS = 0
    TTL = 600
    RDLENGTH = 0
    RDATA = None

    def code(self):
        # Initiation
        self.QR = 1  # It's a response
        buffer = []

        # make header
        buffer = self.put16bits(buffer, self.ID)
        buffer = self.put16bits(buffer, self.make_flages())
        buffer = self.put16bits(buffer, self.QDCOUNT)
        buffer = self.put16bits(buffer, self.ANCOUNT)
        buffer = self.put16bits(buffer, self.NSCOUNT)
        buffer = self.put16bits(buffer, self.ARCOUNT)

        # make Question
        buffer = self.code_domain(buffer, self.QNAME)
        buffer = self.put16bits(buffer, self.TYPE)
        buffer = self.put16bits(buffer, self.CLASS)

        # make Answer
        buffer.append(192)  # Name is a pointer
        buffer.append(HEADER_OFFSET)  # Pointer is to the name at offset 0x00c

        buffer = self.put16bits(buffer, self.TYPE)
        buffer = self.put16bits(buffer, self.CLASS)
        buffer = self.put32bits(buffer, self.TTL)
        buffer = self.put16bits(buffer, self.RDLENGTH)

        # Value   Meaning/Use
        # x'0001 (1)  An A record for the domain name
        # x'0002 (2)  A NS record( for the domain name
        # x'0005 (5)  A CNAME record for the domain name
        # x'0006 (6)  A SOA record for the domain name
        # x'000B (11) A WKS record(s) for the domain name
        # x'000C (12) A PTR record(s) for the domain name
        # x'000F (15) A MX record for the domain name
        # x'0021 (33) A SRV record(s) for the domain name
        # x'001C (28) An AAAA record(s) for the domain name
        if self.TYPE is 1:
            buffer = self.code_ip(buffer, self.RDATA)

        # print(buffer)

        return str(bytearray(buffer))

    def code_domain(self, buffer, domain):
        for word in domain.split('.'):
            buffer.append(len(word))
            for c in list(word):
                buffer.append(ord(c))

        buffer.append(0)
        return buffer

    def code_ip(self, buffer, domain):
        for word in domain.split('.'):
            buffer.append(int(word))

        return buffer

    def put32bits(sefl, buffer, value):
        buffer.append(value >> 24)
        buffer.append(value >> 16)
        buffer.append(value >> 8)
        buffer.append(value & int('11111111', 2))
        return buffer

    def put16bits(self, buffer, value):
        buffer.append(value >> 8)
        buffer.append(value & int('11111111', 2))
        return buffer
