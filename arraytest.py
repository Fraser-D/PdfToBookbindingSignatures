array = []
x = 2
for i in range(x*4):
    array.append(i)

print(array)


def shuffle(l, n):
    s = []
    n = n * 2
    s.append(l[(-1 - n)])
    s.append(l[(0 + n)])
    s.append(l[(1 + n)])
    s.append(l[(-2 - n)])
    return s

# feed this a list of pages, multiple of 4


def signature_shuffle(pagelist):
    out = []
    for i in range(len(pagelist)//4):
        out.extend(shuffle(pagelist, i))
    return out


print(signature_shuffle(array))
