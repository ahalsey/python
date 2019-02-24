#!/usr/bin/python
#
#name = input("Enter file:")
#if len(name) < 1 : name = "mbox-short.txt"
strings = list()
times = list()
hms = list()
hours = list()
counts = dict()

filehand = open("mbox-short.txt")


for line in filehand:
    strings = line.split()
    if not line.startswith('From '):
        continue
    times.append(strings[5])

for time in times:
    hms = time.split(':')
    hours.append(hms[0])


for hour in hours:
    counts[hour] = counts.get(hour,0)+1

hours = sorted((counts.items()))
for h,c in hours:
    print(h,c)
