import random
import re
symbols = ['+', '-', '*']


class Node:
    idx_node = -1
    def __init__(self, content, id, parent):
        self.content = content
        self.id = id
        self.parent = parent
        Node.idx_node += 1

def make_nodes(n, m):
    rroot = Node('*root*', -1, None)
    Node.idx_node = 0

    def add_node(node, n, m, idx_node):
        if n < m:
            if random.random() > 0.6:  # add sub-tree
                symbol = random.choice(symbols)
                child_node = Node(symbol, node.idx_node, node.id)
                x = add_node(child_node, n + 1, m, child_node.idx_node)
                y = add_node(child_node, n + 1, m, child_node.idx_node)
                ids = [x[0], child_node.id, y[0]]
                parents = [x[1], node.id, y[1]]
                expr = ['(', x[2], symbol, y[2], ')']
            else:  # add leaf (number)
                expr = random.randint(1, 9)
                idx_node += 1
                child_node = Node(expr, node.idx_node, node.id)
                ids = child_node.id
                parents = node.id
        else:
            # raise
            expr = random.randint(1, 9)
            idx_node += 1
            child_node = Node(expr, node.idx_node, node.id)
            ids = child_node.id
            parents = node.id
        return ids, parents, expr
    ids, parents, expr = add_node(rroot, n, m, rroot.idx_node)
    # flatten
    ids = list(flatten(ids))
    parents = list(flatten(parents))
    expr = [str(el) for el in flatten(expr)]
    return ids, parents, expr


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


def if_left(parents, i):
    for j in parents[i + 1:]:
        if j == parents[i]:
            return True
    return False


def num_bracket(parents, i):
    num = 0
    if parents[i] == -1:
        return num
    elif if_left(parents, i):
        while if_left(parents, i):
            num += 1
            i = parents[i]
    else:
        while not if_left(parents, i) and parents[i] != -1:
            num += 1
            i = parents[i]
    return num


def recover(ids, parents, expr_no_brackets):
    expr_recover = []
    p1 = re.compile('^[0-9]*$')
    for i in expr_no_brackets:
        expr_recover.append(i)
    for i in range(len(parents)):
        if not p1.match(expr_no_brackets[i]) or parents[i] == -1:
            pass
        elif if_left(parents, i):
            num = num_bracket(parents, i)
            string = ''
            for j in range(num):
                string += '('
            expr_recover[i] = string + expr_recover[i]
        else:
            num = num_bracket(parents, i)
            string = ''
            for j in range(num):
                string += ')'
            expr_recover[i] = expr_recover[i] + string

    return expr_recover


for i in range(100):
    lev = 0
    max_lev = random.randint(1, 5)
    s = make_nodes(lev, max_lev)
    ids, parents, expr = s
    expr_no_brackets = [j for j in expr if j not in '()']
    assert len(expr_no_brackets) == len(ids) == len(parents)
    print(ids, parents, ''.join(expr), ''.join(expr_no_brackets))
    #expr_recover = recover(ids, parents, expr_no_brackets)
    #print(expr_recover)
