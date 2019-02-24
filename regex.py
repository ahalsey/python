import re

nums = list()
total = 0
file = open("regex_sum_173391.txt")

for line in file:
    if len(re.findall('([0-9]+)', line)) > 0:
        nums.append(re.findall('([0-9]+)', line))
	
for num in nums:
    for n in num:
        total = total + int(n)


print(total)