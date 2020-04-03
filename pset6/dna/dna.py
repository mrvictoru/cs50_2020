import sys, csv

def strcheck(dnastrs,dnasq):
    iden = {}
    for strs in dnastrs:
        i = 1
        # check consecutive repeat of STRs
        while strs*i in dnasq:
            i+=1
        # update the number of most repeat of a STR
        iden.update({strs:i-1})

    return iden

def match(dnastrs,iden,idenbase):

    for i in range(len(idenbase)):
        match = 1
        for j in dnastrs:
            if int(idenbase[i][j]) != int(iden[j]):
                match = 0
                break

        if match == 0:
            continue
        else:
            return idenbase[i]['name']

    return -1



def main():
    # check usage error
    if sys.argv[1] is None or sys.argv[2] is None:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit

    idenbase = []
    # open database
    with open(sys.argv[1], "r", newline='') as f:

        # read database data into dictionary
        reader = csv.DictReader(f)

        for i in reader:
            idenbase.append(i)

        # read STR sequence
        dnastrs = list(i.keys())
        dnastrs = dnastrs[1:]

    #open sequences sample
    with open(sys.argv[2]) as d:

        #read entire sequence
        dnasq = d.read()

    #look for STRs
    iden = strcheck(dnastrs,dnasq)

    #check against exisiting data base
    name = match(dnastrs,iden,idenbase)

    if name == -1:
        print("No match")
    else:
        print(name)



if __name__ == "__main__":
    main()