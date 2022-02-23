import sys
import os
import unittest
# sys.path.append('../')  #'../']
sys.path.append(os.path.join(os.getcwd(), '..'))  #'/Users/Dubkov/Desktop/Greekbrains/python/python-client-server/HW3/unit_tests/..']
# почему отрабатывает не как на видео?
# sys.path.insert(0, os.path.join(os.getcwd(), '..'))
# from pprint import pprint
# pprint(sys.path)
from client import create_presence, process_ans
from common.variables import *

class TestClass(unittest.TestCase):
    OK_DICT = {
        RESPONSE: 200
    }
    ERROR_DICT = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_presence(self):
        test = create_presence()
        test[TIME] = 1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_no_presence(self):
        test = create_presence()
        test[TIME] = 1
        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 1})

    def test_200_ans(self):
        self.assertEqual(process_ans(self.OK_DICT), '200 : OK')

    def test_400_ans(self):
        self.assertEqual(process_ans(self.ERROR_DICT), '400 : Bad Request')

    def test_dict_presence(self):
        self.assertIsInstance(create_presence(), dict)

    def test_no_str_presence(self):
        self.assertNotIsInstance(create_presence(), str)
    def test_error_ans(self):
        self.assertRaises(ValueError, process_ans, 'Wrong dict')

    def test_str_ans(self):
        self.assertIsInstance(process_ans({RESPONSE: 200}), str)

    def test_no_dict_ans(self):
        self.assertNotIsInstance(process_ans({RESPONSE: 200}), dict)

    if __name__ == '__main__':
        unittest.main()