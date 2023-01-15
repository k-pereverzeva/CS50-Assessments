import re
from cs50 import get_int

while True:
    credit = get_int("Number: ")
    if credit > 0:
        break

numbers = [int(a) for a in str(credit)]
reversed_num = list(reversed(numbers))
print(reversed_num)
length = len(numbers)
summ = 0

for i in range(1, length, 2):
    mult = reversed_num[i] * 2
    if mult >= 10:
        summ = summ + (mult % 10) + 1
    else:
        summ = summ + mult

for i in range(0, length, 2):
    summ = summ + reversed_num[i]

print(summ)

if summ % 10 == 0:
    if length == 15 and numbers[0] == 3 and (numbers[1] == 4 or numbers[1] == 7):
        print("AMEX")
    elif length == 16 and numbers[0] == 5 and numbers[1] >= 1 and numbers[1] <= 5:
        print("MASTERCARD")
    elif numbers[0] == 4 and (length == 13 or length == 16):
        print("VISA")
    else:
        print("INVALID")
else:
    print("INVALID")