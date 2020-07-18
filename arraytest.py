array = []
x = 4
for i in range(x*4):
    array.append(i)

# print(array)

hc = [[0, 1, 2, 3], [4, 5, 6, 7, ], [8, 9, 10, 11], [12, 13, 14, 15]]

for line in hc:
    print(line)


def shuffle(l, n):
    s = []
    n = n * 2
    s.append(l[(-1 - n)])
    s.append(l[(0 + n)])
    s.append(l[(1 + n)])
    s.append(l[(-2 - n)])
    return s


def signature_shuffle(pagelist):
    out = []
    for i in range(len(pagelist)//4):
        out.extend(shuffle(pagelist, i))
    return out


def shufoutput(arrayofarrays):
    shuf = []
    for line in hc:
        shuf.append(signature_shuffle(line))
    flat = []
    for x in shuf:
        flat.extend(x)
    return flat


# print(signature_shuffle(array))
print("\n")

thing = shufoutput(hc)


print(thing)
