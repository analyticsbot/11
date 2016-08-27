import sqlite3

conn = sqlite3.connect('accounts.db', check_same_thread = False)
print "[+] Opened database connection successfully"
c = conn.cursor()

## try to create the table if it does not exists
try:
    c.execute("""create table accounts (id INT, Gender TEXT,Name TEXT,Username TEXT,Password TEXT,Location TEXT,
                    Email TEXT,Email_pwd TEXT, Bio TEXT,Phone TEXT);""")
    conn.commit()
except Exception,e:
    print str(e)
    pass

f = open('gberelia_60_PVA_10_05_2016.xlsx - Sheet1.csv', 'rb')
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
    emai_pwd = line_split[6].strip()
    bio = line_split[7].strip()
    phone = line_split[8].strip()
    try:
        c.execute("""INSERT into accounts(id, Gender, Name, Username, Password, Location ,
                    Email, Email_pwd,  Bio , Phone) values (?,?,?,?,?,?,?,?,?,?)""" , (count, gender, name, username,\
                                                                                     password, \
                                                                                    location, email,emai_pwd,\
                                                                                      bio, phone) )
    except Exception,e:
        print str(e)

conn.commit()
conn.close()

    
    
    

