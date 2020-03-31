#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
from sys import argv, stderr, exit
import entryInfo 

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db

# inserts userEntry into database
def insertEntry(entryInfo):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()

        sql = """INSERT INTO userInformation (netid, name, phone, email, description, address) 
               VALUES(%s, %s, %s, %s, %s, %s)"""

             
        # execute a statement
        name = entryInfo.getName()
        netid = entryInfo.getNetid()
        phone = entryInfo.getPhone()
        email = entryInfo.getEmail()
        address = entryInfo.getAddress()
        description = entryInfo.getDescription()

        
        cur.execute(sql, (netid, name, phone, email, description, address))

        conn.commit()            
        print('success')
        # close the communication with the PostgreSQL
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

# based on fields of entry, queries all rows in database containing these fields
def searchEntry(entry):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
    
        sql = """
            SELECT *
            FROM userInformation
            WHERE userInformation.netid LIKE %s AND
            userInformation.name LIKE %s AND
            userInformation.email LIKE %s AND
            userInformation.phone LIKE %s AND
            userInformation.description LIKE %s AND
            userInformation.address LIKE %s;
        """

             
        # execute a statement
        name = entry.retName()
        netid = entry.retNetid()
        phone = entry.retPhone()
        email = entry.retEmail()
        address = entry.retAddress()
        description = entry.retDescription()

        
        cur.execute(sql, (netid, name, email, phone, description, address))
        row = cur.fetchone()

        entries = []
        while row is not None:
            user = entryInfo.entryInfo()
            print(row[0])
            user.setNetid(str(row[0]))
            user.setName(str(row[1]))
            user.setEmail(str(row[2]))
            user.setPhone(str(row[3]))
            user.setDescription(str(row[4]))
            user.setAddress(str(row[5]))
            entries.append(user)
            row = cur.fetchone()
          
        print('success')
        # close the communication with the PostgreSQL
        cur.close()
        return entries
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# prints all rows in userInformation table
def displayRows():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
   # execute a statement
        cur.execute('SELECT * from userInformation;')
        
        
        row = cur.fetchone()

        while row is not None:
            for item in row:
                print(item + " ", end=' ')
            print() 
            row = cur.fetchone()

       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def main(argv):

    info = entryInfo.entryInfo()
    info.setAddress(str(argv[1]))
    print(info.getAddress())
    # insertEntry(info)
    query = searchEntry(info)
    for entry in query:
        print(entry.retUserInfo())

 
 
if __name__ == '__main__':
    main(argv)