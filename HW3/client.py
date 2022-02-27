"""
Функции клиента: сформировать presence-сообщение; отправить сообщение серверу;
получить ответ сервера; разобрать сообщение сервера;параметры командной
строки скрипта client.py <addr> [<port>]: addr — ip-адрес сервера;
port — tcp-порт на сервере, по умолчанию 7777.
"""

from common.variables import *
from time import time
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_msg, get_msg
from json import JSONDecodeError
import logging
import log.client_log_config

CLIENT_LOGGER = logging.getLogger('client')


def create_presence(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE}'
                        f' сообщение для пользователя {account_name}')
    return out


def process_ans(msg):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера : {msg}')
    if RESPONSE in msg:
        if msg[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {msg[ERROR]}'
    raise ValueError


def main():
    try:
        server_address = argv[1]
        server_port = int(argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    CLIENT_LOGGER.info(f'Запущен клиент с параметрами: '
                       f'адрес сервера : {server_address}, порт : {server_port}')
    transport = socket(AF_INET, SOCK_STREAM)
    transport.connect((server_address, server_port))
    msg_to_server = create_presence()
    send_msg(transport, msg_to_server)
    try:
        answer = process_ans(get_msg(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера: {answer}')
    except JSONDecodeError:
        CLIENT_LOGGER.error(f'Не удалось декодировать Json строку')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}')


if __name__ == '__main__':
    main()
