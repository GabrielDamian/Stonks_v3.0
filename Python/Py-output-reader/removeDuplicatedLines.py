
if __name__ == "__main__":
    lines = []
    file1 = open('apollo.txt', 'r')
    Lines = file1.readlines()

    for a in Lines:
        lines.append(a)

    print("before:",len(lines))
    distinct = list(set(lines))

    print("after:",len(distinct))

    format = ""
    for a in distinct:
        format += a

    #write into file
    text_file = open("apollo.txt", "w")
    n = text_file.write(format)
