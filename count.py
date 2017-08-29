#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# scp count gdm:/dat1/count.py

from __future__ import unicode_literals
import sys
from collections import Counter
import codecs
import os


def _counter(alist, n=None, min_count=None):
    if min_count:
        for i in Counter(alist).most_common(n):
            # if i[1] < min_count:
            #     break
            yield i
    else:
        for i in Counter(alist).most_common(n):
            yield i


def gen_txt(fname, aencode='utf-8', errors='strict'):  # ignore
    fname = os.path.abspath(fname)
    if os.path.isfile(fname):
        # with open(fname, 'rU') as f:
        # with codecs.open(fname, 'r', 'utf-8') as f:
        with codecs.open(fname, 'r', 'utf-8', errors='ignore') as f:
            for word in f:
                # print(str, unicode_type, str is unicode_type)
                # print(word)
                # if str is not unicode_type:  # py2 # todo:py3 coverage
                #     word = word.decode(aencode, errors=errors)
                yield word.rstrip('\n')
    else:
        print('file %s not found' % fname)

afile = sys.argv[1]
f_out = '%ss' % afile
min_count = 1
if len(sys.argv) > 2:
    min_count = int(sys.argv[2])
res = gen_txt(afile)
# azlib._print_counter(res, min_count=min_count)

f2 = open(f_out, 'w')
for i in _counter(res):
    ret = '%s\t%s\n' % (i[1], i[0])
    # f2.write(ret.encode('u8'))
    f2.write(ret)
f2.close()
