import sys
import numpy

toe = {'冠词': 0, '单复数': 0, '介词': 0, '词语形态': 0, '拼写': 0, '标点': 0, '大小写': 0}


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
    diff_new = []
    i = 0
    while i < len(diff) - 1:
        if diff[i][2] + 1 == diff[i + 1][2]:
            diff_new.append([diff[i][0] + ' ' + diff[i + 1][0], diff[i][1] + ' ' + diff[i + 1][1], diff[i][2]])
            i += 2
        else:
            diff_new.append(diff[i])
            i += 1
    if i < len(diff):
        diff_new.append(diff[i])
    return diff_new


def type_of_error(d):
    global toe
    for i in d:
        if i[0].upper() == i[1].upper():
            toe['大小写'] += 1
        elif i[1] in ['a', 'an', 'the', 'The'] or i[0] in ['a', 'an', 'the', 'The']:
            toe['冠词'] += 1
        elif i[1] in ['on', 'at', 'in', 'of', 'to', 'for', 'about'] or i[0] in ['on', 'at', 'in', 'of', 'to', 'for',
                                                                                'about']:
            toe['介词'] += 1
        elif i[0] + 's' == i[1] or i[0] + 'es' == i[1] or i[1] + 's' == i[0] or i[1] + 'es' == i[0]:
            toe['单复数'] += 1
        elif i[0] + 'ing' == i[1] or i[0] + 'ed' == i[1] or i[1] + 'ing' == i[0] or i[1] + 'ed' == i[0] or i[
            0] + 'ly' == i[1] or i[1] + 'ly' == i[0]:
            toe['词语形态'] += 1
        elif i[0] in [',', '.', '?', '-'] or i[1] in [',', '.', '?', '-']:
            toe['标点'] += 1

        else:
            print(i[0], i[1])


def main():
    f = open('aa_nlc_nlc2', encoding='UTF-8')
    lines = f.readlines()
    num_0 = 0
    for line in lines:
        line = line.strip()
        [sentence1, sentence2] = line.split('\t')
        sentence1, sentence2 = sentence1.split(' '), sentence2.split(' ')
        sentence1 = ['*'] + sentence1
        sentence2 = ['*'] + sentence2
        if sentence1 == sentence2:
            num_0 += 1
        else:
            d = wer(sentence2, sentence1)
            type_of_error(d)


def test(line):
    line = line.strip()
    [sentence1, sentence2] = line.split('\t')
    sentence1, sentence2 = sentence1.split(' '), sentence2.split(' ')
    sentence1 = ['*'] + sentence1
    sentence2 = ['*'] + sentence2
    if sentence1 == sentence2:
        pass
    else:
        print(wer(sentence2, sentence1))


main()
