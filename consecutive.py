

def consecutive(s):
    count = 0
    maxcount = 0
    maxchar = ""
    lastchar = ""
    for char in s:
        if (char != lastchar):
            count = 1
        elif (char == lastchar):
            count = count + 1
        if (count > maxcount):
            maxcount = count
            maxchar = char
        lastchar = char

    print(maxcount, maxchar)


s = input("Enter a string: ")

consecutive(s)
