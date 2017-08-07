from sympy import *
import random
import re
symbol = ['+', '-', '*']


class node:
    nod_count = 0

    def __init__(self, string, id, father):
        self.string = string
        self.id = id
        self.father = father
        node.nod_count += 1


def f(nod, n, m):
    a = random.randint(0, 8)
    if n < m:
        if a < 3:
            d = node(symbol[a], nod.nod_count + 1, nod.id)
            x = f(d, n + 1, m)
            y = f(d, n + 1, m)
            expression = '(' + x[0] + symbol[a] + y[0] + ')'
            relation = x[1] + ',' + str(nod.id) + ',' + y[1]
            id = x[2] + ',' + str(d.id) + ',' + y[2]
        else:
            expression = str(random.randint(1, 9))
            d = node(expression, nod.nod_count + 1, nod.id)
            relation = str(nod.id)
            id = str(d.id)
    else:
        expression = str(random.randint(1, 9))
        d = node(expression, nod.nod_count + 1, nod.id)
        relation = str(nod.id)
        id = str(d.id)
    return [expression, relation, id]


def position(l):
    id = ''
    k = 0
    l[1] = re.sub(',1,', ', -1,', l[1])
    for i in l[2][1:]:
        if i == ',':
            id = ',' + id + ','
            id1 = ', ' + str(k) + ','
            l[1] = re.sub(id, id1, l[1])
            id = ''
            k += 1
        else:
            id += i
    return [l[0], l[1]]


def trans(l):
    id = ''
    rela = []
    for i in l[1][1:]:
        if i == ',':
            rela.append(int(id))
            id = ''
        else:
            id += i
    x = re.sub('\(', '', l[0])
    x = re.sub('\)', '', x)
    return [l[0], x, rela]


def if_left(l, i):
    for j in l[2][i + 1:]:
        if(j == l[2][i]):
            return True
    return False


def num_bracket(l, i):
    num = 0
    if l[2][i] == -1:
        return num
    elif if_left(l, i):
        while if_left(l, i):
            num += 1
            i = l[2][i]
    else:
        while (not if_left(l, i)) & (l[2][i] != -1):
            num += 1
            i = l[2][i]
    return num


def recover(l):
    p1 = re.compile('^[0-9]*$')
    l.append([])
    for i in l[1]:
        l[3].append(i)
    for i in range(len(l[2])):
        if (not p1.match(l[1][i])) or (l[2][i] == -1):
            pass
        elif if_left(l, i):
            num = num_bracket(l, i)
            string = ''
            for j in range(num):
                string += '('
            l[3][i] = string + l[3][i]
        else:
            num = num_bracket(l, i)
            string = ''
            for j in range(num):
                string += ')'
            l[3][i] = l[3][i] + string
    x = ''
    for i in l[3]:
        x += i
    l[3] = x
    return l
for i in range(100):
    n = 0
    m = random.randint(1, 5)
    root = node('', 1, 0)
    node.nod_count = 1
    s = f(root, n, m)
    print(s[0], s[1], s[2])
    s[1] = ',' + s[1] + ','
    s[2] = ',' + s[2] + ','
    x = recover(trans(position(s)))
    print(x[3])
    assert s[0] == x[3]
