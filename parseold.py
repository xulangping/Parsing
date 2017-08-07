from sympy import *
import random
import re
symbol = ['+', '-', '*']


class node:
    nod_count = 0

    def __init__(self, str, id, father):
        self.str = str
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
    l[1] = re.sub(',1,', ',-1,', l[1])
    for i in l[2][1:]:
        if i == ',':
            id = ',' + id + ','
            id1 = ',' + str(k) + ','
            l[1] = re.sub(id, id1, l[1])
            id = ''
            k += 1
        else:
            id += i
    return [l[0], l[1]]
for i in range(100):
    n = 0
    m = random.randint(1, 5)
    root = node('', 1, 0)
    node.nod_count = 1
    s = f(root, n, m)
    s[1] = ',' + s[1] + ','
    s[2] = ',' + s[2] + ','
    print(position(s))
