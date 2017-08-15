import random
import re
l_c = ['和']
l_u = ['的']
l_v = ['是', '在', '有']
l_n = ['牛顿', '毛泽东', '凯撒大帝']
l_nk = ['基本信息', '职业', '代表作品']
l_d = ['不']
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

    def add_node(node, n, m, idx_node, property):
        if n < m:
            if property == 'n':
                if random.random() > 0.6:  # add sub-tree
                    i = random.choice([2, 1, 0])
                    symbol = random.choice([l_c, l_v, l_u][i])
                    if i == 1:
                        if random.random() > 0.5:
                            symbol = random.choice(l_d) + symbol
                        else:
                            pass
                    child_node = Node(symbol, node.idx_node, node.id)
                    if i == 2:
                        x = add_node(child_node, n + 1, m, child_node.idx_node, 'n')
                        y = add_node(child_node, n + 1, m, child_node.idx_node, 'nk')
                    else:
                        x = add_node(child_node, n + 1, m, child_node.idx_node, 'n')
                        y = add_node(child_node, n + 1, m, child_node.idx_node, 'n')
                    ids = [x[0], child_node.id, y[0]]
                    parents = [x[1], node.id, y[1]]
                    expr = ['(', x[2], symbol, y[2], ')']
                else:  # add leaf (number)
                    expr = random.choice(l_n)
                    idx_node += 1
                    child_node = Node(expr, node.idx_node, node.id)
                    ids = child_node.id
                    parents = node.id
            else:
                if random.random() > 0.6:  # add sub-tree
                    symbol = random.choice(l_u)
                    child_node = Node(symbol, node.idx_node, node.id)
                    x = add_node(child_node, n + 1, m, child_node.idx_node, 'nk')
                    y = add_node(child_node, n + 1, m, child_node.idx_node, 'nk')
                    ids = [x[0], child_node.id, y[0]]
                    parents = [x[1], node.id, y[1]]
                    expr = ['(', x[2], symbol, y[2], ')']
                else:  # add leaf (number)
                    expr = random.choice(l_nk)
                    idx_node += 1
                    child_node = Node(expr, node.idx_node, node.id)
                    ids = child_node.id
                    parents = node.id
        else:
            # raise
            if property == 'n':
                expr = random.choice(l_n)
                idx_node += 1
                child_node = Node(expr, node.idx_node, node.id)
                ids = child_node.id
                parents = node.id
            else:
                expr = random.choice(l_nk)
                idx_node += 1
                child_node = Node(expr, node.idx_node, node.id)
                ids = child_node.id
                parents = node.id
        return ids, parents, expr

    property = random.choice(['n', 'nk'])
    ids, parents, expr = add_node(rroot, n, m, rroot.idx_node, property)
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


def num_bracket(ids, parents, i):
    num = 0
    if parents[i] == -1:
        return num
    elif if_left(parents, i):
        while if_left(parents, i):
            num += 1
            for j in range(len(ids)):
                if ids[j] == parents[i]:
                    i = j
                    break
    else:
        while (not if_left(parents, i)) and (parents[i] != -1):
            num += 1
            for j in range(len(ids)):
                if ids[j] == parents[i]:
                    i = j
                    break
    return num


def recover(ids, parents, expr_no_brackets):
    expr_recover = []
    for i in expr_no_brackets:
        expr_recover.append(i)
    for i in range(len(parents)):
        if not expr_no_brackets[i] in flatten([l_n, l_nk]) or parents[i] == -1:
            pass
        elif if_left(parents, i):
            num = num_bracket(ids, parents, i)
            string = []
            for j in range(num):
                string.append('(')
            expr_recover[i] = [string, expr_recover[i]]
        else:
            num = num_bracket(ids, parents, i)
            string = []
            for j in range(num):
                string.append(')')
            expr_recover[i] = [expr_recover[i], string]
    expr_recover = [str(el) for el in flatten(expr_recover)]
    return expr_recover


for i in range(100):
    lev = 0
    max_lev = random.randint(1, 5)
    s = make_nodes(lev, max_lev)
    ids, parents, expr = s
    expr_no_brackets = [j for j in expr if j not in '()']
    assert len(expr_no_brackets) == len(ids) == len(parents)
    print(ids, parents, ''.join(expr), ''.join(expr_no_brackets))
    expr_recover = recover(ids, parents, expr_no_brackets)
    print(''.join(expr_recover))
    assert expr_recover == expr