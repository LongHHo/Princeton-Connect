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
    oLat = secrets.choice(range(3200, 8000)) #offset in metres (2 - 5 miles)
    if (sign == 0):
        oLat = -1 * oLat
    sign = secrets.choice(range(0, 2)) #used to determine sign of the offset
    oLong = secrets.choice(range(3200, 8000)) #offset in metres (2 - 5 miles)
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
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        insertUser = """INSERT INTO userInformation (netid, name, phone, email, description, address, city)
               VALUES(%s, %s, %s, %s, %s, %s, %s) 
               ON CONFLICT (netid) 
               DO UPDATE SET
               (name, phone, email, description, address, city) 
                  = (EXCLUDED.name, EXCLUDED.phone, EXCLUDED.email, EXCLUDED.description, EXCLUDED.address, EXCLUDED.city);"""

        # insertCoordinates = """INSERT INTO coordinates (netid, address, latitude, longitude)
        #        VALUES(%s, %s, %s, %s) 
        #        ON CONFLICT (netid) 
        #        DO UPDATE SET
        #        (address, latitude, longitude) 
        #           = (EXCLUDED.address, EXCLUDED.latitude, EXCLUDED.longitude);"""
        # execute a statement
        name = entryInfo.getName()
        netid = entryInfo.getNetid()
        phone = entryInfo.getPhone()
        email = entryInfo.getEmail()
        address = entryInfo.getAddress()
        description = entryInfo.getDescription()
        city = entryInfo.getCity()


        cur.execute(insertUser, (netid, name, phone, email, description, address, city))

        # print('before')
        # coordinates = geocode(address)
        # print('after')

        # latitude = float(coordinates[0])
        # longitude = float(coordinates[1])

        # print(latitude)
        # print(longitude)

        # cur.execute(insertCoordinates, (netid, address, latitude, longitude))


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
            WHERE userInformation.netid LIKE %s AND
            userInformation.name LIKE %s AND
            userInformation.email LIKE %s AND
            userInformation.phone LIKE %s AND
            userInformation.description LIKE %s AND
            userInformation.address LIKE %s AND
            userInformation.city LIKE %s;
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
        while row is not None:
            sub.append(str(row[0]))
            sub.append(str(row[1]))
            sub.append(str(row[2]))
            sub.append(str(row[3]))
            sub.append(str(row[4]))
            # change actual address to coordinates
            coordinates = geocode(str(row[5]))
            if (coordinates is not None):
                print('******')
                offcoordinates = coordinateOffset(coordinates[0], coordinates[1])
                sub.append(offcoordinates[0])
                sub.append(offcoordinates[1])
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
    """ Connect to the PostgreSQL database server """
    print('sending message')
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        insertUser = """INSERT INTO msg_id_timestamp (msg, reciever, sender)
               VALUES(%s, %s, %s) 
               ON CONFLICT DO NOTHING;"""


        cur.execute(insertUser, (message, reciever, sender))
        conn.commit()
        print('success')
        print('inserted')
        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

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
        return messages

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')





    

def main(argv):
    
    user = entryInfo.entryInfo('Long Ho', 'lhho', 'lhho@princeton.edu', '7142602003', 'just a cali boy looking for kangaroos', 'Churchill Ave, Hobart TAS 7005, Australia')
    userTwo = entryInfo.entryInfo('Slim Jim', 'sjim', 'sjim@princeton.edu', '1234567', 'im a stick', '4000 Union Pacific Ave, Commerce, CA')
    print(getMessages('jaitegs', 'billy'))
   

if __name__ == '__main__':
    main(argv)
