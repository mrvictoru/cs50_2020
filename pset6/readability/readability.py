from cs50 import get_string

def main():
    sentence = get_string("Text: ")
    length = len(sentence)
    print(f"length: {length}")
    letters = words = sentences = L = S = index = 0

    for i in range(length):
        print(i)
        if sentence[i].isalpha():
            letters += 1
            print(f"letters plus: {letters}")
        if i == 0:
            print(f"words plus: {words}")
            words += 1
        elif sentence[i].isalpha() and sentence[i-1].isspace() or sentence[i-1] =='"' or sentence[i-1] == "'":
            print(f"words plus: {words}")
            words += 1

        if sentence[i] == '?' or sentence[i] == "!" or sentence[i] == ".":
            print(f"sentence plus: {sentences}")
            sentences += 1

    print(f"words:{words} sentences:{sentences} letters: {letters}")
    if words <= 100:
        L = letters/words*100
        S = sentences/words*100
    else:
        L = letters/(words/100)
        S = sentences/(words/100)

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index > 16:
        print("Grade 16+")
    elif index <= 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


main()