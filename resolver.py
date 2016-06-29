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
        except NotSupportException, e:
            logging.error(e.message)
            self.make_not_found_response()
            return self.response.code()

    def decode(self):
        self.query = decode(self.bytes_data)

    def make_not_found_response(self):
        pass

    def make_response(self):
        self.response = Response()

        self.response.ID = self.query.ID
        self.response.QNAME = self.query.QNAME
        self.response.TYPE = self.query.QTYPE
        self.response.CLASS = self.query.QCLASS

    def search(self):
        self.response.QDCOUNT = 1
        self.response.ANCOUNT = 1
        self.response.RDATA = '127.0.0.1'

        if len(self.query.QNAME) is 0:
            self.response.RCODE = CODE_NameError
            self.response.RDLENGTH = 1
        else:
            self.response.RCODE = CODE_OK
            self.response.RDLENGTH = 4
