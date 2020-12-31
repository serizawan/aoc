import sys


if len(sys.argv) != 2:
    print("Missing input file: python {} file".format(sys.argv[0]))
    sys.exit()

f = open(sys.argv[1])
l = f.read().splitlines()
f.close()

l = [int(i) for i in l]

for i in range(len(l)):
    for j in range(i, len(l)):
        for k in range(j, len(l)):
            if l[i] + l[j] + l[k] == 2020:
                print(l[i] * l[j] * l[k])
