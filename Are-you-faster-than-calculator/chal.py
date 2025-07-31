#!/usr/local/bin/python

import time
from random import randint, choice

operators = ['+', '-', '*', '/', '^', '%', '|']

def main():
    print("Are you fast in math? Let's see!")
    print()
    for i in range(100):
        a = randint(1, 100)
        b = randint(1, 100)
        op = choice(operators)
        print(f'{a} {op} {b} = ?')
        start = time.time()
        ans = input()
        end = time.time()
        if end - start > 3:
            print('Too slow!')
            return
        if op == '+':
            if int(ans) != a + b:
                print('Wrong!')
                return
        elif op == '-':
            if int(ans) != a - b:
                print('Wrong!')
                return
        elif op == '*':
            if int(ans) != a * b:
                print('Wrong!')
                return
        elif op == '/':
            if int(ans) != a // b:
                print('Wrong!')
                return
        elif op == '^':
            if int(ans) != a ** b:
                print('Wrong!')
                return
        elif op == '%':
            if int(ans) != a % b:
                print('Wrong!')
                return
        elif op == '|':
            if int(ans) != a | b:
                print('Wrong!')
                return
            
    print('You are fast in math! Here is your flag: CITU{0k_y0u_4r3_f4st_m4th_w1z4rd!}')

if __name__ == '__main__':
    main()