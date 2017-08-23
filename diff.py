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
f = open('aa_nlc_nlc2', encoding = 'UTF-8')
lines = f.readlines()
for line in lines:
    [sentence1, sentence2] = line.split('\t')
    sentence2 = sentence2.split('\n')[0]
    if sentence1 == sentence2:
        pass
    else:
        sentence1, sentence2 = delete_ht(sentence1, sentence2)
        print(sentence1)
        print(sentence2)