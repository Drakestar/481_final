import random
boolboy = True
while boolboy:
    for x in range(1, random.randint(1, 4)):
        print(x)
        if x == 3:
            boolboy = False

print("dank")