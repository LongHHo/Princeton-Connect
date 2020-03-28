#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
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

def main():

    info = entryInfo.entryInfo('Test Ho', 'test', 'test@gmail.com', '111')
    # insertEntry(info)
    displayRows()

 
 
if __name__ == '__main__':
    main()