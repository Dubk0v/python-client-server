"""5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать 
результаты из байтовового в строковый тип на кириллице.
"""

import chardet
import subprocess
import platform


def check_ping(site):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    args = ['ping', param, '2', site]
    result = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in result.stdout:
        result = chardet.detect(line)
        line = line.decode(result['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


if __name__ == '__main__':
    resources = ['yandex.ru', 'youtube.com']
    for resource in resources:
        check_ping(resource)

