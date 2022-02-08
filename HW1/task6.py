"""6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Далее забыть о том, что мы сами только что создали
этот файл и исходить из того, что перед нами файл в неизвестной кодировке.
Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""

from chardet import detect


def create_file(file_name, words):
    f = open(file_name, 'w', encoding='utf-8')
    for word in words:
        f.write(word + '\n')
    f.close()


def detect_file_encoding(file):
    with open(file, 'rb') as f:
        content = f.read()
    encoding = detect(content)['encoding']
    print(encoding)
    return encoding


def open_file(file):
    encoding = detect_file_encoding(file)
    with open(file, encoding=encoding) as f_n:
        for el_str in f_n:
            print(el_str, end='')
        print()


if __name__ == '__main__':
    WORDS_LIST = ["сетевое программирование", "сокет", "декоратор"]
    FILE_NAME = 'test_file.txt'
    create_file(FILE_NAME, WORDS_LIST)
    open_file(FILE_NAME)
