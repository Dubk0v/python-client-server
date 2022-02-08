"""4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» 
из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""


def convert_str_to_bytes(words):
    if len(words) > 0:
        for word in words:
            word = str.encode(word, encoding='utf-8')
            print(word)
            word = bytes.decode(word, encoding='utf-8')
            print(word)


if __name__ == '__main__':
    WORDS_LIST = ["разработка", "администрирование", "protocol", "standard"]
    convert_str_to_bytes(WORDS_LIST)
