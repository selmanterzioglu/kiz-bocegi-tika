import sys

class a:
    b = 5

for i in vars(a):
    print(sys.getsizeof(i))