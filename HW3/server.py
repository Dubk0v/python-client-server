"""
Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт
для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает
все доступные адреса).
"""

from common.variables import *
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_msg, get_msg
from json import JSONDecodeError
import logging
import log.server_log_config

SERVER_LOGGER = logging.getLogger('server')


def process_client_msg(msg):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {msg}')
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg \
            and USER in msg and msg[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in argv:
            listen_port = int(argv[argv.index('-p') + 1])
            SERVER_LOGGER.info(f'Слушаем порт : {listen_port}')
        else:
            listen_port = DEFAULT_PORT
            SERVER_LOGGER.info(f'Слушаем порт по умолчанию : {listen_port}')
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
        exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    try:
        if '-a' in argv:
            listen_address = argv[argv.index('-a') + 1]
            SERVER_LOGGER.info(f'Слушаем адрес : {listen_address}')
        else:
            listen_address = ''
            SERVER_LOGGER.info(f'Слушаем все адреса')
    except IndexError:
        SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать IP для сервера')
        exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соединение с ПК : {client_address}')
        try:
            msg_from_client = get_msg(client)
            SERVER_LOGGER.debug(f'Получено сообщение от клиента : {msg_from_client}')
            response = process_client_msg(msg_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту : {response}')
            send_msg(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается')
            client.close()
        except JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать Json строку, полученную от'
                                f'клиента {client_address}. Соединение закрывается')
            client.close()


if __name__ == '__main__':
    main()
