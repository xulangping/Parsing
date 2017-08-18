import random

l_config = [
    ['n', [['(', 'n', 'c', 'n', ')'], [1, -1, 1]]],
    ['n', [['(', 'n', 'v', 'n', ')'], [1, -1, 1]]],
    ['n', [['(', 'n', 'u', 'nk', ')'], [1, -1, 1]]],
    ['v', [['(', 'd', 'v', ')'], [1, -1]]],
    ['v', [['(', 'p', 'n', 'v', ')'], [2, 0, -1]]],
]

d_node = {}


class Node:
    def __init__(self, content, id, parent):
        self.content = content
        self.id = id
        self.parent = parent


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


def divide_node(node, id):
    global d_node
    a = []
    for i in l_config:
        if i[0] == node.content:
            a.append(i[1])
    if a == []:
        return [node.id, id]
    else:
        [b, c] = random.choice(a)
        node_num = len(b) - 2
        if node_num == 3:
            d_node[id + 1] = Node(b[1], id + 1, node.id)
            d_node[node.id] = Node(b[2], node.id, node.parent)
            d_node[id + 2] = Node(b[3], id + 2, node.id)
            x = ['(', id + 1, node.id, id + 2, ')']
            id += 2
        else:
            d_node[id + 1] = Node(b[1], id + 1, node.id)
            d_node[node.id] = Node(b[2], node.id, node.parent)
            x = ['(', id + 1, node.id, ')']
            id += 1
        return [x, id]


def if_left(parents, i):
    if parents[i] == -1:
        return False
    for j in parents[:i]:
        if j == parents[i]:
            return False
    return True


def if_right(parents, i):
    if parents[i] == -1:
        return False
    for j in parents[i + 1:]:
        if j == parents[i]:
            return False
    return True


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
        while (if_right(parents, i)) and (parents[i] != -1):
            num += 1
            for j in range(len(ids)):
                if ids[j] == parents[i]:
                    i = j
                    break
    return num


def recover(ids, parents, sentence_no_brackets):
    sentence_recover = []
    for i in sentence_no_brackets:
        sentence_recover.append(i)
    for i in range(len(parents)):
        if sentence_no_brackets[i] in ['v', 'c', 'u'] or parents[i] == -1:
            pass
        elif if_left(parents, i):
            num = num_bracket(ids, parents, i)
            string = []
            for j in range(num):
                string.append('(')
            sentence_recover[i] = [string, sentence_recover[i]]
        elif if_right(parents, i):
            num = num_bracket(ids, parents, i)
            string = []
            for j in range(num):
                string.append(')')
            sentence_recover[i] = [sentence_recover[i], string]
    sentence_recover = [str(el) for el in flatten(sentence_recover)]
    return sentence_recover


def make_nodes(n):
    for j in range(n):
        rroot = Node('*root*', -1, None)
        d_node[-1] = rroot
        d_node[0] = Node('n', 0, -1)
        expr = [0]
        id = 0
        while random.random() > 0.05:
            i = random.randint(0, len(expr) - 1)
            if expr[i] in d_node.keys():
                a = divide_node(d_node[expr[i]], id)
                expr = list(flatten([expr[:i], a[0], expr[i + 1:]]))
                id = a[1]
            else:
                pass
        sentence = []
        parents = []
        ids = []
        for i in expr:
            if i in d_node.keys():
                sentence.append(d_node[i].content)
                ids.append(i)
                parents.append(d_node[i].parent)
            else:
                sentence.append(i)
        sentence_no_brackets = [j for j in sentence if j not in '()']
        print(ids, ''.join(sentence), ''.join(sentence_no_brackets), parents)
        sentence_recover = recover(ids, parents, sentence_no_brackets)
        print(sentence_recover)


make_nodes(100)
