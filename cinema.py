# this program get seats input from user and display a seating chart for a theater

# print title of movies, time, and price
def show_title():
    print("POPCORN CINEMA - Movie Ticketing System".center(50))
    print('Movie Name: WARRIOR OF FUTURE - 2D\nDate: 14 Sep 2022 (WED)\nTime: 19:30\nPrice:   Standard - MOP 110.0\n\t POPCORN VIP - MOP 100.0\n\t JUMBO POPCORN VIP - MOP 90.0')
    
# print seating chart, occupied seats are marked with 'X'
def show_seats(occupied_seats = [], total_seats = 60):
    print(' Real Time Seating Chart '.center(100,'='))
    print('[Exit]' + '[ SCREEN ]'.center(80) + '[Entrance]')
    for seat in range(1, total_seats+1):
        if seat in occupied_seats:
            print('{:5}'.format(seat), ':[ x ]', end=' ')
        else:
            print('{:5}'.format(seat), ':[   ]', end=' ')
        if seat % 10 == 0:
            print()
    
    print('\n\n')

# get user input for seat numbers, check for invalid input and already occupied seats
def get_seats(occupied_seats = [], total_seats = 60):
    # get user input for seat numbers as a string
    seats = input('Please enter the seat numbers you want to book (separated by space): ')
    # split the string into a list of seat numbers
    seats = seats.split()
    # check if the seat numbers are valid
    for seat in seats:
        # check if seat is a digit
        if not seat.isdigit():
            print('Invalid seat number: {}'.format(seat))
            return 0
        # check if seat is in range
        elif int(seat) not in range(1, total_seats+1):
            print('Seat number out of range: {}'.format(seat))
            return 0
        # check if seat is already occupied
        elif int(seat) in occupied_seats:
            print('Seat already occupied: {}'.format(seat))
            return 0
        # if all checks passed, add seat to occupied seats list
        else:
            occupied_seats.append(int(seat))
    
    # if all seats are valid, return number of seats booked
    return len(seats)

# main function
def main():
    # initialize occupied seats list
    occupied_seats = []
    # show title
    show_title()
        
    while True:
        # show seating chart
        show_seats(occupied_seats)
        # get user input for seats, use while loop to keep asking for input until valid input is given
        booked_seat = 0
        while True:
            newbooked = get_seats(occupied_seats)
            # check if input is valid
            if newbooked == 0:
                print('Please try again.')
            else:
                show_seats(occupied_seats)
                booked_seat += newbooked
                if input('Do you want to book more seats? (y/n): ').lower() == 'n':
                    break
                else:
                    continue
        # show total seats booked
        print('Total seats booked: {}'.format(booked_seat))
        # show total price
        print('Total price: MOP {}'.format(booked_seat * 110))

        # ask for next session
        if input('Do you want to book for next session? (y/n): ').lower() == 'n':
            break
    

# call main function
if __name__ == '__main__':
    main()
