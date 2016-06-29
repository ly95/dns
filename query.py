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
