#!/usr/bin/python
import psycopg2
from configparser import ConfigParser
from sys import argv, stderr, exit
import entryInfo
import googlemaps
from datetime import datetime
import requests
import secrets
import math
import time 

# gmaps = googlemaps.Client(key='AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw')

def coordinateOffset(latitude, longitude):
    radius = 6371000.0 #radius of earth 
    sign = secrets.choice(range(0, 2)) #used to determine sign of the offset
    oLat = secrets.choice(range(500, 1200)) #offset in metres (700m - 1 mile)
    if (sign == 0):
        oLat = -1 * oLat
    sign = secrets.choice(range(0, 2)) #used to determine sign of the offset
    oLong = secrets.choice(range(500, 1200)) #offset in metres (700m - 1 mile)
    if (sign == 0):
        oLong = -1 * oLong
    new_latitude  = latitude  + (oLat / radius) * (180 / math.pi)
    new_longitude = longitude + (oLong / radius) * (180 / math.pi) / math.cos(latitude * math.pi/180)
    coordinates = [new_latitude, new_longitude]
    return coordinates


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


# returns latitude and longitude of a given address
def geocode(address):
    try:
        url = ('https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'
            .format(address.replace(' ','+'), 'AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw'))

        response = requests.get(url)
        resp_json_payload = response.json()
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        return lat, lng
    except Exception as e:
        print(e)


# deletes entry based on just the netid
def deleteEntry(netid):
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

        deleteUserInfo = """
            DELETE FROM userInformation WHERE netid = %s;
        """
        deleteCoordinates = """
            DELETE FROM coordinates WHERE netid = %s;
        """

        cur.execute(deleteUserInfo, (netid,))
        cur.execute(deleteCoordinates, (netid,))
        

        conn.commit()
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# inserts userEntry into database
# entryInfo is an entryInfo object
# if entryInfo already exists in database, then updates it

def insertUser(netid):
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

        User = """INSERT INTO users (netid)
               VALUES(%s) 
               ON CONFLICT DO NOTHING;"""


        cur.execute(User, (netid,))
        conn.commit()
        print('success')
        print('inserted', netid)
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def insertEntry(entryInfo):
    """ Connect to the PostgreSQL database server """
    conn = None

    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    insertUser = """INSERT INTO userInformation (netid, name, phone, email, description, address, city, latitude, longitude)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (netid) 
            DO UPDATE SET
            (name, phone, email, description, address, city, latitude, longitude) 
                = (EXCLUDED.name, EXCLUDED.phone, EXCLUDED.email, EXCLUDED.description, EXCLUDED.address, EXCLUDED.city, 
                EXCLUDED.latitude, EXCLUDED.longitude);"""

    name = entryInfo.getName()
    netid = entryInfo.getNetid()
    phone = entryInfo.getPhone()
    email = entryInfo.getEmail()
    address = entryInfo.getAddress()
    description = entryInfo.getDescription()
    city = entryInfo.getCity()

    coordinates = geocode(str(address))
    latitude = None
    longitude = None
    if (coordinates is not None):
        offcoordinates = coordinateOffset(coordinates[0], coordinates[1])
        latitude = float(offcoordinates[0])
        longitude = float(offcoordinates[1])

    cur.execute(insertUser, (netid, name, phone, email, description, address, city, latitude, longitude))

    conn.commit()
    conn.close()
    print('success')
    print('Database connection closed.')
    # close the communication with the PostgreSQL



# based on fields of entry, returns a list of all rows in database containing these fields
# in which each row is a userInfo object
# entry is a entryInfo object
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
            WHERE userInformation.netid ILIKE %s AND
            userInformation.name ILIKE %s AND
            userInformation.email ILIKE %s AND
            userInformation.phone ILIKE %s AND
            userInformation.description ILIKE %s AND
            userInformation.address ILIKE %s AND
            userInformation.city ILIKE %s;
        """


        # execute a statement
        name = entry.retName()
        netid = entry.retNetid()
        phone = entry.retPhone()
        email = entry.retEmail()
        address = entry.retAddress()
        description = entry.retDescription()
        city = entry.retCity()


        cur.execute(sql, (netid, name, email, phone, description, address, city))
        row = cur.fetchone()

        print(str(row))
        entries = []
        while row is not None:
            user = entryInfo.entryInfo()
            user.setNetid(str(row[0]))
            user.setName(str(row[1]))
            user.setEmail(str(row[2]))
            user.setPhone(str(row[3]))
            user.setDescription(str(row[4]))
            user.setAddress(str(row[5]))
            user.setCity(str(row[6]))
            entries.append(user)
            row = cur.fetchone()


        # close the communication with the PostgreSQL
        cur.close()
        return entries

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def searchName(netid):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        sql = """
            SELECT name
            FROM userInformation
            WHERE userInformation.netid ILIKE %s;
        """


        cur.execute(sql, (netid,))
        row = cur.fetchone()

        name = netid

        if row is not None:
            name = str(row[0])


        # close the communication with the PostgreSQL
        cur.close()
        return name

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')




def getAll():
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
        """


        cur.execute(sql)
        row = cur.fetchone()

        entries = []
        sub = []
        # Entries with an address will have 7 fields, entries without will have 5
        while row is not None:
            sub.append(str(row[0]))
            sub.append(str(row[1]))
            sub.append(str(row[2]))
            sub.append(str(row[3]))
            sub.append(str(row[4]))
            if ((row[7] is not None) and (row[8] is not None)):
                # append addresses if not null
                sub.append(row[7])
                sub.append(row[8])
            sub.append(str(row[6]))
            entries.append(sub)
            sub = []
            row = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
        return entries
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def checkNetid(netid):
    query = """
            SELECT *
            FROM users
            WHERE users.netid LIKE %s;
            """

    conn = None
    try:
        # read connection parameters
        params = config()
        user = netid + '%'

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        cur.execute(query, (user,))
        row = cur.fetchone()
        cur.close()
        print(row, '***************')
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def sendMessage(sender, reciever, message):
    
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
       
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        insertUser = """INSERT INTO msg_id_timestamp (msg, reciever, sender, rd)
               VALUES(%s, %s, %s, %s) 
               ON CONFLICT DO NOTHING;"""


        cur.execute(insertUser, (message, reciever, sender, 1))
        conn.commit()
       
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def getContacts(netid):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        getContacts = """SELECT * 
                        FROM msg_id_timestamp
                        WHERE sender = %s OR reciever = %s
                        ORDER BY timestamp DESC;"""


        cur.execute(getContacts, (netid, netid))

        row = cur.fetchone()
        contacts = []

        while row is not None:
            if (row[1] != netid and row[1] not in contacts):
                contacts.append(row[1])
            
            if (row[2] != netid and row[2] not in contacts):
                contacts.append(row[2])
            
            row = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()
        return contacts 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def getMessages(netid, contact):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        getMessages = """SELECT * 
                        FROM msg_id_timestamp
                        WHERE (sender = %s AND reciever = %s)
                        OR (sender = %s AND reciever = %s)
                        ORDER BY timestamp                        
                        """


        cur.execute(getMessages, (netid, contact, contact, netid))

        markMessagesAsRead = """
                        UPDATE msg_id_timestamp
                        SET rd=0
                        WHERE sender = %s AND reciever = %s;
                        COMMIT;              
                        """

        row = cur.fetchone()
        messages = []

        while row is not None:
            msg = []
            msg.append(row[1])
            msg.append(row[3])
            
            messages.append(msg)
            row = cur.fetchone()

        # close the communication with the PostgreSQL
        cur.close()

        cur2 = conn.cursor()
        cur2.execute(markMessagesAsRead, (contact, netid))
        cur2.close()
        return messages

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')



def getNotification(netid):
    "SELECT COUNT(*) FROM users WHERE name = @Name"
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        getNotification = """SELECT COUNT(*) 
                        FROM msg_id_timestamp
                        WHERE reciever = %s AND rd=1;                   
                        """


        cur.execute(getNotification, (netid,))

        row = cur.fetchone()
        

        # close the communication with the PostgreSQL
        cur.close()
        return row[0]

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def getNotificationDetails(netid):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        getContacts = """SELECT * 
                        FROM msg_id_timestamp
                        WHERE reciever = %s AND rd=1
                        ORDER BY timestamp DESC;"""


        cur.execute(getContacts, (netid,))

        row = cur.fetchone()
        details = []

        getMessagesFromContact= """ 
        SELECT COUNT(*) 
        FROM msg_id_timestamp
        WHERE (sender = %s AND reciever = %s) AND rd=1;                   
        """

        while row is not None:
            if (row[1] not in details):
                details.append(row[1])
                cur2 = conn.cursor()
                cur2.execute(getMessagesFromContact, (row[1], netid))
                details.append(cur2.fetchone()[0])
                cur2.close()
                
            
            row = cur.fetchone()


        # close the communication with the PostgreSQL
        cur.close()
        x = getNotification(netid)
        detailsf = 'Welcome! You have '
        if (x == 1):
            detailsf = detailsf +  str(x) + ' new message: \n'
        else:
            detailsf = detailsf +  str(x) + ' new messages: \n'
        
        length = len(details)
        for i in range(0, length, 2):
            s = ''
            s = s + str(details[i+1]) + '   '
            if(details[i + 1] == 1):
                s = s + 'New message from   ' + details[i]
            else:
                s = s + 'New messages from  ' + details[i]
            s = s + '\n'
            detailsf = detailsf + s


            

        return detailsf 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


    

def main(argv):
    # for i in range (0, 10):
    #     sendMessage('dora', 'jaitegs', 'hello ')

    # for i in range (0, 2):
    #     sendMessage('lola', 'jaitegs', 'hello ')

    # for i in range (0, 7):
    #     sendMessage('blake', 'jaitegs', 'hello ')

    for i in range (0, 4):
        sendMessage('longgg', 'jaitegs', 'hello ')
    deleteEntry('lhho')

    

    


    


   

if __name__ == '__main__':
    main(argv)
