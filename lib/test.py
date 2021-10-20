# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def encry_msg(msg):
    txt = 'abcdefghijklmnopqrstuwvxyz'
    num = len(txt)
    print(num)


if __name__ == '__main__':
    rule = input()

    if rule:
        ln, num = rule.split()
    else:
        exit(0)

    msg = input()

    encry_msg(msg)