def delete_ht(s1, s2):
    a1 = s1.split(' ')
    a2 = s2.split(' ')
    i = 0
    try:
        while a1[i] == a2[i]:
            i += 1
    except:
        pass
    a1 = a1[i:]
    a2 = a2[i:]
    a1_re = a1[::-1]
    a2_re = a2[::-1]
    i = 0
    try:
        while a1_re[i] == a2_re[i]:
            i += 1
    except:
        pass
    a1_re = a1_re[i:]
    a2_re = a2_re[i:]
    return a1_re[::-1], a2_re[::-1]

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


def group_2(s):
    a = []
    if len(s) % 2 ==0:
        for i in range(0, len(s), 2):
            a.append([s[i], s[i + 1]])
    else:
        for i in range(0, len(s) - 1, 2):
            a.append([s[i], s[i + 1]])
        a.append(s[-1])
    return a
def delete_mid(s1, s2):
    a1 = group_2(s1)
    a2 = group_2(s2)
    a1_left = [i for i in a1 if i not in a2]
    a2_left = [i for i in a2 if i not in a1]
    return a1_left, a2_left


f = open('aa_nlc_nlc2', encoding='UTF-8')
lines = f.readlines()
num_0 = 0
num_1 = 0
num_2 = 0
for line in lines:
    [sentence1, sentence2] = line.split('\t')
    sentence2 = sentence2.split('\n')[0]
    if sentence1 == sentence2:
        num_0 += 1
    else:
        sentence1, sentence2 = delete_ht(sentence1, sentence2)
        if len(sentence1) > 1 and len(sentence2) > 1:
            if set(sentence1) == set(sentence2):
                num_1 += 1
            else:
                sentence1, sentence2 = delete_mid(sentence1, sentence2)
                print(sentence1)
                print(sentence2)
                print(line)
                num_2 += 1
        else:
            num_1 += 1
print(num_0, num_1, num_2)