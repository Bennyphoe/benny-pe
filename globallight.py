import sqlite3
from flask import make_response, abort

from joblib import dump, load



def read():
    
    lights = []
    
    conn = sqlite3.connect('light.db')
    
    c = conn.cursor()
    c.execute('SELECT id, devicename, light, timestamp FROM light ORDER BY id ASC')
    results = c.fetchall()
    
    for result in results:
                
        lights.append({'id':result[0],'devicename':result[1],'light':result[2],'timestamp':result[3]})
    
    conn.close()
    
    return lights



def create(globallight):
    '''
    This function creates a new light record in the database
    based on the passed in light data
    :param globallight:  Global light record to create in the database
    :return:        200 on success
    '''
    devicename = globallight.get('devicename', None)
    light = globallight.get('light', None)
    timestamp = globallight.get('timestamp', None)
    
    conn = sqlite3.connect('light.db')
    
    c = conn.cursor()    
    sql = "INSERT INTO light (devicename, light, timestamp) VALUES('" + devicename + "', " + str(light) + ", '" + timestamp + "')"
    print(sql)
    c.execute(sql)
    conn.commit()
    conn.close()
    
    return make_response('Global light record successfully created', 200)



def cluster(light):
    
    try:
    
        print('here 1: ' + str(light))
        
        # predict new temperature and humidity observation
        kmeans = load('lightcluster.joblib')
        print('here 2')
        # temperature, humidity
        newX = [[light]]
        result = kmeans.predict(newX)
        print('Cluster Light: light={}; cluster={}'.format(light, result[0]))

        return str(result[0])
        
    except Exception as error:

        print('Error: {}'.format(error.args[0]))

        return 'Unknown'
