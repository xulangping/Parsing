import random

l_config = [
    ['n', ['(', 'n', 'c', 'n', ')']],
    ['n', ['(', 'n', 'v', 'n', ')']],
    ['n', ['(', 'n', 'u', 'nk', ')']],
    ['v', ['(', 'd', 'v', ')']]
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
        b = random.choice(a)
        node_num = len(b) - 2
        if node_num == 3:
            d_node[id + 1] = Node(b[1], id + 1, id)
            d_node[node.id] = Node(b[2], node.id, node.parent)
            d_node[id + 2] = Node(b[3], id + 2, id)
            x = ['(', id + 1, node.id, id + 2, ')']
            id += 2
        else:
            d_node[id + 1] = Node(b[1], id + 1, id)
            d_node[node.id] = Node(b[2], node.id, node.parent)
            x = ['(', id + 1, node.id, ')']
            id += 1
        return [x, id]
rroot = Node('*root*', -1, None)
d_node[-1] = rroot
d_node[0] = Node('n', 0, -1)
expr = [0]
id = 0
while random.random() > 0.1:
    i = random.randint(0, len(expr) - 1)
    if expr[i] in d_node.keys():
        a = divide_node(d_node[expr[i]], id)
        expr = list(flatten([expr[:i], a[0], expr[i + 1:]]))
        id = a[1]
    else:
        pass
sentence = []
parent = []
for i in expr:
    if i in d_node.keys():
        sentence.append(d_node[i].content)
        parent.append(d_node[i].parent)
    else:
        sentence.append(i)
print(expr, ''.join(sentence), parent)


