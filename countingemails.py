#countingemails.py
#
import sqlite3

connection = sqlite3.connect('emails.sqlite')
cursor = connection.cursor()

cursor.execute('create table Counts (org text, count integer)')

interations = 0
fname = input('Enter file name: ')
fhandle = open(fname)
for line in fhandle:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    cursor.execute('select count from Counts where org = ? ', (org,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('insert into Counts (org, count) values (?,1)', (org,))
    else:
        cursor.execute('update Counts set count = count + 1 where email = ?', (org,))
    iterations = interations + 1
    if iterations % 10 == 0:
        connection.commit()

sequel = 'select org, count from Counts order by count'

for row in cursor.execute(sequel):
    print(str(row[0]), row[1])
