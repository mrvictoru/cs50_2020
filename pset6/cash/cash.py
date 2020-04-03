from cs50 import get_float, get_int

def main():
    change = [25, 10 , 5, 1]
    owed = 0
    change_owed = int(get_positive_float()*100)
    for i in change:

        owed = owed+(change_owed // i)
        change_owed = change_owed % i

    print(owed)



def get_positive_float():
    while True:
        n = get_float("Change owed: ")
        if n > 0:
            break
    return n


main()