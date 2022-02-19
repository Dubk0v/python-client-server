import sys
import os
import unittest
# sys.path.append('../')
sys.path.append(os.path.join(os.getcwd(), '..'))



def test_presence(self):
    test = create_presence()
    test[TIME] = 1
    self.assertEqual(test, {ACTION: PRESENCE, TIME: 1, USER: {ACCOUNT_NAME: DEFAULT_ACCOUNT_NAME}})


if __name__ == '__main__':
    unittest.main()