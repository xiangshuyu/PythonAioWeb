import random

ALL_CHAR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def gen_random_str(str_len=10):
    result = ""
    for i in range(0, str_len):
        rand_int = random.randint(0, 62)
        char = ALL_CHAR[rand_int: rand_int + 1]
        result += char
    return result


if __name__ == '__main__':
    gen_random_str(32)

# 345
