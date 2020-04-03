import sys, csv
import cs50


def main():
    # check usage error
    if sys.argv[1] is None:
        print("Usage: python import.py characters.csv")
        sys.exit

    # create database by opening and closing an empty file first
    open(f"students.db","w").close()
    db = cs50.SQL("sqlite:///students.db")

    db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

    # open database
    with open(sys.argv[1], "r") as f:

        # read database data into dictionary
        reader = csv.reader(f)
        next(reader, None)  # skip the headers

        # loop through csv
        for row in reader:

            # split name into first, middle and last
            name = row[0].split()

            # check for middle name
            if len(name) == 2:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", name[0], None, name[1], row[1], row[2])

            else:
                db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?,?,?,?,?)", name[0], name[1], name[2], row[1], row[2])


main()