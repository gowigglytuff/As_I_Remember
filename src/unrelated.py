
consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
vowels = ["A", "E", "I", "O", "U"]

count = 0

for vow in vowels:
    for con1 in consonants:
        con_list = []
        for con2 in consonants:
            phrase = con1 + vow + con2
            con_list.append(phrase)
            count += 1
        print(con_list)
    print("-----")
print(count)
