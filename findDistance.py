import psycopg2
from configparser import ConfigParser
from sys import argv, stderr, exit
import entryInfo
import googlemaps
from datetime import datetime
import requests

# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyDQe5G3tqd5Vfwefn7w3Djrv1L1bmlKkTw') 

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


def calcDist(adr1, adr2):
    # Requires cities name 
    print(adr1)
    print(adr2)
    my_dist = gmaps.distance_matrix(adr1, adr2)

    distance = my_dist['rows'][0]['elements'][0]['distance']['value'] 
    
    # Printing the result 
    return distance


def findNearbyPeople(address):
    conn = None
    # try:
        # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    sql = """
        SELECT address, email
        FROM userInformation;
    """

    cur.execute(sql)
    row = cur.fetchone()

    entries = []
    while row is not None:
        potAddress = row[0]
        email = row[1]
        if (calcDist(address, potAddress) < 1000):
            entries.append(email)
        row = cur.fetchone()


    # close the communication with the PostgreSQL
    cur.close()
    conn.close()

    return entries

    # except (Exception, psycopg2.DatabaseError) as error:
    #     print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')



def main(argv):
   print(findNearbyPeople('New York, NY'))


if __name__ == '__main__':
    main(argv)

