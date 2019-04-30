#!/bin/python3


def arrange(sentence):
    sentence = sentence.replace('.','')
    sentence = sentence.lower()
    l = sentence.split()
    l.sort(key = len)
    l[0] = l[0].capitalize()
    l[len(l)-1] = l[len(l)-1] + '.'
    result = (' '.join(l))

    return result


sentence = input()

result = arrange(sentence)

print(result)