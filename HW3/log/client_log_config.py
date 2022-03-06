import logging
import os


log = logging.getLogger('client')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')
file_hand = logging.FileHandler(PATH, encoding='utf-8')


formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
file_hand.setFormatter(formatter)
log.addHandler(file_hand)
log.setLevel(logging.DEBUG)

