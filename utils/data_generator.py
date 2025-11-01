import random
import string

def generate_post_code(length=10):
    """
    Генерирует случайный номер из 10 цифр
    :type length: int
    :rtype: str
    """
    if length <= 0:
        raise ValueError('Длина должна быть положительным числом и не равняться нулю')

    return ''.join(random.choices(string.digits, k=length))

def post_code_to_first_name(post_code_str):
    """
    Преобразует строковый Post Code в имя, где каждая пара цифр - индекс буквы (0-25)
    0 -> 'a', 1 -> 'b', ..., 25 -> 'z', 26 -> 'a', 27 -> 'b', и т. д.
    :type post_code_str: str
    :rtype: str
    """
    if len(post_code_str) != 10 or not post_code_str.isdigit():
        raise ValueError('Post Code должен быть 10-значной строкой из цифр')

    name = ''

    for i in range(0, 10, 2):                   # берём пары
        pair_str = post_code_str[i:i + 2]
        num = int(pair_str)                     # преобразуем пару в число
        letter_index = num % 26                 # остаток от деления на 26 дает индекс буквы (0-25)
        letter = chr(ord('a') + letter_index)   # получаем букву по индексу
        name += letter

    return name
