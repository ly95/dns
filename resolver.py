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

from query import decode
import logging
from error import NotSupportException
from response import Response, CODE_NameError, CODE_OK


class Resolver(object):
    bytes_data = None

    query = None
    response = None

    def __init__(self, buffer):
        self.bytes_data = map(ord, list(buffer))
        logging.debug(self.bytes_data)

    def do(self):
        self.decode()
        self.make_response()
        self.search()

        try:
            return self.response.code()
        except NotSupportException as e:
            logging.error(e.message)
            self.make_not_found_response()
            return self.response.code()

    def decode(self):
        self.query = decode(self.bytes_data)

    def make_not_found_response(self):
        self.response.QDCOUNT = 1
        self.response.ANCOUNT = 1
        self.response.RDATA = 0
        self.response.RCODE = CODE_NameError
        self.response.RDLENGTH = 1

    def make_response(self):
        self.response = Response()

        self.response.ID = self.query.ID
        self.response.QNAME = self.query.QNAME
        self.response.TYPE = self.query.QTYPE
        self.response.CLASS = self.query.QCLASS

    def search(self):
        if self.query.QTYPE is 1:
            self.response.QDCOUNT = 1
            self.response.ANCOUNT = 1
            self.response.RDATA = '127.0.0.1'
            self.response.RCODE = CODE_OK
            self.response.RDLENGTH = 4
        else:
            raise NotSupportException("not support QTYPE: " + str(self.query.QTYPE))
