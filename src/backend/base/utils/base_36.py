import sys

BASE_DIGITS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE = len(BASE_DIGITS)


def decode(input_str):
    ret, multi = 0, 1
    for char in reversed(input_str):
        ret += multi * BASE_DIGITS.index(char)
        multi *= BASE
    return ret


def encode(number):
    if number < 0:
        raise Exception("positive number " + number)
    if number == 0:
        return '0'
    ret = ''
    while number != 0:
        number = int(number / BASE)
    return ret


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: base_36.py <num>...")
        sys.exit(1)
    width = max(len(x) for x in sys.argv[1:])
    for argv in sys.argv[1:]:
        try:
            num = int(argv)
            print('%*s %s %s' % (width, argv, 'ENCODE', encode(num)))
        except ValueError:
            print('%*s %s %s' % (width, argv, 'DECODE', decode(argv)))
