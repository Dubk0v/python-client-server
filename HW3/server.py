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
from decos import log
from select import select
from time import time
from argparse import ArgumentParser

SERVER_LOGGER = logging.getLogger('server')

@log
def process_client_msg(msg, msg_list, client, clients, names):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {msg}')
    if ACTION in msg and msg[ACTION] == PRESENCE and TIME in msg \
            and USER in msg:
        if msg[USER][ACCOUNT_NAME] not in names.keys():
            names[msg[USER][ACCOUNT_NAME]] = client
            send_msg(client, {RESPONSE: 200})
        else:
            send_msg(client, {
                RESPONSE: 400,
                ERROR: 'Имя пользователя уже занято.'
            })
            clients.remove(client)
            client.close()
        return
    elif ACTION in msg and msg[ACTION] == MSG and DESTINATION in msg \
            and TIME in msg and  SENDER in msg and MSG_TEXT in msg:
        msg_list.append(msg)
        return
    elif ACTION in msg and msg[ACTION] == EXIT and ACCOUNT_NAME in msg:
        clients.remove(names[msg[ACCOUNT_NAME]])
        names[msg[ACCOUNT_NAME]].close()
        del names[msg[ACCOUNT_NAME]]
        return
    else:
        send_msg(client, {
            RESPONSE: 400,
            ERROR: 'Запрос некорректен.'
        })
        return


@log
def process_msg(msg, names, listen_socks):
    if msg[DESTINATION] in names and names[msg[DESTINATION]] in listen_socks:
        send_msg(names[msg[DESTINATION]], msg)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {msg[DESTINATION]} '
                           f'от пользователя {msg[SENDER]}.')
    elif msg[DESTINATION] in names and names[msg[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {msg[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


@log
def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(argv[1:])
    listen_addr = namespace.a
    listen_port = namespace.p

    # проверка получения корректного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта {listen_port}. '
            f'Допустимы адреса с 1024 до 65535.')
        exit(1)

    return listen_addr, listen_port


def main():
    # try:
    #     if '-p' in argv:
    #         listen_port = int(argv[argv.index('-p') + 1])
    #         SERVER_LOGGER.info(f'Слушаем порт : {listen_port}')
    #     else:
    #         listen_port = DEFAULT_PORT
    #         SERVER_LOGGER.info(f'Слушаем порт по умолчанию : {listen_port}')
    #     if listen_port < 1024 or listen_port > 65535:
    #         raise ValueError
    # except IndexError:
    #     SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
    #     exit(1)
    # except ValueError:
    #     print(
    #         'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
    #     exit(1)
    #
    # try:
    #     if '-a' in argv:
    #         listen_addr = argv[argv.index('-a') + 1]
    #         SERVER_LOGGER.info(f'Слушаем адрес : {listen_addr}')
    #     else:
    #         listen_addr = ''
    #         SERVER_LOGGER.info(f'Слушаем все адреса')
    # except IndexError:
    #     SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать IP для сервера')
    #     exit(1)

    listen_addr, listen_port = arg_parser()
    SERVER_LOGGER.info(f'Слушаем порт : {listen_port}'
                       f'Слушаем адрес : {listen_addr}'
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_addr, listen_port))
    transport.settimeout(0.5)
    clients = []
    msgs = []
    names = dict()
    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_address = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соединение с ПК : {client_address}')
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_msg in recv_data_lst:
                try:
                    process_client_msg(get_msg(client_with_msg),
                                       msgs, client_with_msg)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_msg.getpeername()} '
                                f'отключился от сервера.')
                    clients.remove(client_with_msg)

        # if msgs and send_data_lst:
        #     message = {
        #         ACTION: MSG,
        #         SENDER: msgs[0][0],
        #         TIME: time(),
        #         MSG_TEXT: msgs[0][1]
        #     }
        #     del msgs[0]
        #     for waiting_client in send_data_lst:
        #         try:
        #             send_msg(waiting_client, message)
        #         except:
        #             SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()}'
        #                                f' отключился от сервера.')
        #             waiting_client.close()
        #             clients.remove(waiting_client)
        for i in msgs:
            try:
                process_msg(i, names, send_data_lst)
            except Exception:
                SERVER_LOGGER.info(f'Связь с клиентом с именем '
                                   f'{i[DESTINATION]} была потеряна')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        msgs.clear()


if __name__ == '__main__':
    main()
