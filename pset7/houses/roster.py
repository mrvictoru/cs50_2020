import sys, csv
import cs50

db = cs50.SQL("sqlite:///students.db")

def main():
    # check usage error
    if sys.argv[1] is None:
        print("Usage: python roster.py House")
        sys.exit

    db = cs50.SQL("sqlite:///students.db")
    print(sys.argv[1])

    house = sys.argv[1]

    students = db.execute("SELECT * FROM students WHERE house == ? ORDER BY last, first;", house)

    for row in students:
        if row["middle"] == None:
            print("{} {}, born {}".format(row["first"], row["last"], row["birth"]))
        else:
            print("{} {} {}, born {}".format(row["first"], row["middle"], row["last"], row["birth"]))

main()