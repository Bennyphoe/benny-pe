import sqlite3
from flask import make_response, abort

from joblib import dump, load

def read():
    conn = sqlite3.connect('lightcloud.db')
    readings = []
    c = conn.cursor()
    c.execute('SELECT id, devicename, abright, atemp, ahum, timestamp FROM light ORDER BY id DESC')
    results = c.fetchall()
    
    for result in results:

        readings.append({'id':result[0],'devicename':result[1],'abight':result[2], 'atemp': result[3], 'ahum': result[4], 'timestamp':result[5]})
    conn.close()
    return readings



def create(payload):
    conn = sqlite3.connect('lightcloud.db')
    devicename = payload.get('devicename', None)
    abright = payload.get('abright', None)
    atemp = payload["atemp"]
    ahum = payload["ahum"]
    timestamp = payload.get('timestamp', None)
    
    c = conn.cursor()    
    sql = "INSERT INTO light (devicename, abright, atemp, ahum, timestamp) VALUES('{}', {}, '{}')".format(devicename, abright, atemp, ahum, timestamp)
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()
    return make_response('Global record successfully created', 200)



def cluster(values):
    
    try:
        print(values)
        abright = values["abright"]
        atemp = values["atemp"]
        ahum = values["ahum"]
        print('here 1: ' + abright + atemp + ahum)
        
        # predict new temperature and humidity and lightlevel observation
        kmeans = load('lightcluster.joblib')
        print('here 2')
        # temperature, humidity
        newX = [[abright, atemp, ahum]]
        result = kmeans.predict(newX)
        print('Cluster Light: values={}; cluster={}'.format(values, result[0]))

        return make_response(str(result[0]), 200)
        
    except Exception as error:

        print('Error: {}'.format(error.args[0]))

        return 'Unknown'
