import sys
import numpy


def flatten(l):
    if isinstance(l, list):
        for el in l:
            if isinstance(el, list):
                for sub in flatten(el):
                    yield sub
            else:
                yield el
    else:
        yield l


def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    # build the matrix
    diff = []
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8).reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitute = d[i - 1][j - 1] + 1
                insert = d[i][j - 1] + 1
                delete = d[i - 1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result) + "%"

    # find out the manipulation steps
    x = len(r)
    y = len(h)
    l = []
    while True:
        if x == 0 and y == 0:
            break
        else:
            if d[x][y] == d[x - 1][y - 1] and r[x - 1] == h[y - 1]:
                l.append("e")
                x = x - 1
                y = y - 1
            elif d[x][y] == d[x][y - 1] + 1:
                l.append("i")
                x = x
                y = y - 1
            elif d[x][y] == d[x - 1][y - 1] + 1:
                l.append("s")
                x = x - 1
                y = y - 1
            else:
                l.append("d")
                x = x - 1
                y = y
    l = l[::-1]

    # print the result in aligned way

    for i in range(len(l)):
        if l[i] == "d":
            diff.append(['', r[i], i])
            h = list(flatten([h[:i], '', h[i:]]))
        elif l[i] == "i":
            diff.append([h[i], '', i])
            r = list(flatten([r[:i], '', r[i:]]))
        elif l[i] == "s":
            diff.append([h[i], r[i], i])
        else:
            pass
    return diff
f = open('aa_nlc_nlc2', encoding='UTF-8')
lines = f.readlines()
num_0 = 0
for line in lines:
    line = line.strip()
    [sentence1, sentence2] = line.split('\t')
    sentence1, sentence2 = sentence1.split(' '), sentence2.split(' ')
    if sentence1 == sentence2:
        num_0 += 1
    else:
        print(wer(sentence2, sentence1))
        print(line)
