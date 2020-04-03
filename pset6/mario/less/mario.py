from cs50 import get_int

def main():
    n = get_positive_int()
    for i in range(n):
        if i > 0:
            for j in range(n - i):
                    print(" ", end="")
            for k in range(i):
                print("#", end="")
            print()

def get_positive_int():
    while True:
        n = get_int("Positive Integer: ")
        if n > 0 and n < 9:
            break
    return n+1

main()