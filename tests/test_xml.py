import unittest
import xmlrpc.client
import urllib.request, urllib.error, urllib.parse
from tornadorpc.xml import XMLRPCHandler

from tests.helpers import TestHandler, RPCTests


class XMLTestHandler(XMLRPCHandler, TestHandler):

    def return_fault(self, code, msg):
        return xmlrpc.client.Fault(code, msg)


class XMLRPCTests(RPCTests, unittest.TestCase):

    handler = XMLTestHandler

    def get_client(self):
        client = xmlrpc.client.ServerProxy(self.get_url())
        return client

    def test_private(self):
        client = self.get_client()
        try:
            client.private()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpc.client.Fault as f:
            self.assertEqual(-32601, f.faultCode)

    def test_private_by_underscore(self):
        client = self.get_client()
        try:
            client._private()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpc.client.Fault as f:
            self.assertEqual(-32601, f.faultCode)

    def test_invalid_params(self):
        client = self.get_client()
        try:
            client.return_fault('a', 'b', 'c')
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpc.client.Fault as f:
            self.assertEqual(-32602, f.faultCode)

    def test_internal_error(self):
        client = self.get_client()
        try:
            client.internal_error()
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpc.client.Fault as f:
            self.assertEqual(-32603, f.faultCode)

    def test_parse_error(self):
        try:
            urllib.request.urlopen(self.get_url(), b'<garbage/>')
        except xmlrpc.client.Fault as f:
            self.assertEqual(-32700, f.faultCode)

    def test_handler_return_fault(self):
        client = self.get_client()
        fault_code = 100
        fault_string = 'Yar matey!'
        try:
            client.return_fault(fault_code, fault_string)
            self.fail('xmlrpclib.Fault should have been raised')
        except xmlrpc.client.Fault as f:
            self.assertEqual(fault_code, f.faultCode)
            self.assertEqual(fault_string, f.faultString)
