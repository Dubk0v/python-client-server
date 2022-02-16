"""
Функции сервера: принимает сообщение клиента; формирует ответ клиенту;
отправляет ответ клиенту; имеет параметры командной строки: -p <port> — TCP-порт
для работы (по умолчанию использует 7777); -a <addr> — IP-адрес для прослушивания (по умолчанию слушает
все доступные адреса).
"""

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, RESPONDEFAULT_IP_ADDRESSSE, DEFAULT_PORT
from sys import argv, exit
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_msg, get_msg
from json import JSONDecodeError

def process_client_msg(msg):
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg \
            and USER in msg and msg[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONDEFAULT_IP_ADDRESSSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in argv:
            listen_port = int(argv[argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        exit(1)

    try:
        if '-a' in argv:
            listen_address = argv[argv.index('-a') + 1]
        else:
            listen_address = ''
    except IndexError:
        print('После параметра \'a\'- необходимо указать IP для сервера')
        exit(1)

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            msg_from_client = get_msg(client)
            print(msg_from_client)
            response = process_client_msg(msg_from_client)
            send_msg(client, response)
            client.close()
        except (ValueError, JSONDecodeError):
            print('Принято некорректное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
