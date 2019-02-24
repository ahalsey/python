counts = dict()
emails = list()

handle = open('mbox-short.txt')
for line in handle:
    line = line.strip()
    if not line.startswith('From '):
        continue
    words = line.split()
    emails.append(words[1])
    #print(emails)
    
for email in emails:
    counts[email] = counts.get(email,0) + 1
        

        
bigcount = None
bigemail = None

for email,count in counts.items():
    if bigcount is None or count > bigcount:
        bigcount = count
        bigemail = email
        
print(bigemail, bigcount)

