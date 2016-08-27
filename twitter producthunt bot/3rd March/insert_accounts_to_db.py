import sqlite3

conn = sqlite3.connect('botdb.db', check_same_thread = False)
print "[+] Opened database connection successfully"
c = conn.cursor()

## try to create the table if it does not exists
try:
    c.execute("""create table accounts (id INT, Gender TEXT,Name TEXT,Username TEXT,Password TEXT,Location TEXT,
                    Email TEXT,Recovery_Mail TEXT,Bio TEXT);""")
    conn.commit()
except Exception,e:
    print str(e)
    pass

f = open('20_accs.csv', 'rb')
data = f.read().split('\n')[1:-1]
data = [d.strip() for d in data]

count= 0
for line in data:
    count +=1
    line_split = line.strip().split(',')
    gender = line_split[0].strip()
    name = line_split[1].strip()
    username = line_split[2].strip()
    password = line_split[3].strip()
    location = line_split[4].strip()
    email = line_split[5].strip()
    recovery_email = line_split[7].strip()
    bio = line_split[9].strip()
    c.execute("""INSERT into accounts(id, Gender, Name, Username, Password, Location ,
                    Email, Recovery_Mail, Bio ) values (?,?,?,?,?,?,?,?,?)""" , (count, gender, name, username, password, \
                                                                                    location, email,recovery_email,\
                                                                                      bio) )

conn.commit()
conn.close()

    
    
    

