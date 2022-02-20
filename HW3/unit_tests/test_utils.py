import sys
import os
import unittest
import json
sys.path.append('../')  #'../']
# sys.path.append(os.path.join(os.getcwd(), '..'))  #'/Users/Dubkov/Desktop/Greekbrains/python/python-client-server/HW3/unit_tests/..']
# почему отрабатывает не как на видео?
# sys.path.insert(0, os.path.join(os.getcwd(), '..'))
# from pprint import pprint
# pprint(sys.path)

from common.utils import *
from common.variables import *

class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    def send(self, msg_to_send):
        json_test_msg = json.dumps(self.testdict)
        self.encoded_msg = json_test_msg.encode(ENCODING)
        self.received_msg = msg_to_send

    def recv(self, max_len):
        json_test_msg = json.dumps(self.testdict)
        return json_test_msg.encode(ENCODING)

class TestClass(unittest.TestCase):
    DICT_SEND = {
        ACTION: PRESENCE,
        TIME: 1,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    OK_DICT = {
        RESPONSE: 200
    }
    ERROR_DICT = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


    def test_send_msg_ok(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_msg(test_socket, self.DICT_SEND)
        self.assertEqual(test_socket.encoded_msg, test_socket.received_msg)

    def test_bytes_send_msg(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_msg(test_socket, self.DICT_SEND)
        self.assertIsInstance(test_socket.encoded_msg, bytes)

    def test_no_dict_send_msg(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_msg(test_socket, self.DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_msg, dict)

    def test_get_msg_ok(self):
        test_socket_ok = TestSocket(self.OK_DICT)
        self.assertEqual(get_msg(test_socket_ok), self.OK_DICT)

    def test_get_msg_err(self):
        test_socket_err = TestSocket(self.ERROR_DICT)
        self.assertEqual(get_msg(test_socket_err), self.ERROR_DICT)

    def test_dict_get_msg(self):
        test_socket_ok = TestSocket(self.OK_DICT)
        self.assertIsInstance(get_msg(test_socket_ok), dict)

    def test_no_str_get_msg(self):
        test_socket = TestSocket(self.DICT_SEND)
        send_msg(test_socket, self.DICT_SEND)
        self.assertNotIsInstance(test_socket.encoded_msg, str)