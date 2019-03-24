#countingemails.py
#
import sqlite3

connection = sqlite3.connect('orgs.sqlite')
cursor = connection.cursor()

cursor.execute('drop table if exists Counts')

cursor.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

interations = 0
fname = input('Enter file name: ')
fhandle = open(fname)
for line in fhandle:
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    pieces = email.split("@")
    org = pieces[1]
    cursor.execute('SELECT count from Counts where org = ? ', (org,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute('INSERT into Counts (org, count) values (?,1)', (org,))
    else:
        cursor.execute('UPDATE Counts set count = count + 1 where org = ?', (org,))
    iterations = interations + 1
    if iterations % 10 == 0:
        connection.commit()

connection.commit()

sequel = 'SELECT org, count from Counts order by count desc'

for row in cursor.execute(sequel):
    print(str(row[0]), row[1])

cursor.close()