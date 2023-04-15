import sys
import random
import time
import json
import requests

import paho.mqtt.client as mqtt



def main():
    
    n = len(sys.argv)
    
    if n > 1:
        
        arg = sys.argv[1]
        print('Light to cluster: ' + arg)
        values = arg.split(",")
        
        
        base_uri = 'http://localhost:5000/'
        lightcluster_uri = base_uri + 'api/lightcluster'
        headers = {'content-type': 'application/json'}       
        res = requests.post(lightcluster_uri, data = json.dumps({"abright": values[0], "atemp": values[1], "ahum": values[2]}), headers = headers)
        print(res)
        cluster_label = str(res.text).replace('"', '')
        cluster_label = cluster_label.strip()
        print('Cluster Label: ' + cluster_label)
        
        smartlight = 'off'
        
        if cluster_label == '1':       
        
            smartlight = 'off'
                
        broker = 'broker.emqx.io'
        port = 1883
        topic = "/benny/pe"
        client_id = f'python-mqtt-{random.randint(0, 10000)}'
        username = 'emqx'
        password = 'public'        
        client = mqtt.Client(client_id)
        client.username_pw_set(username, password)
        client.connect(broker, port)
        client.publish(topic, smartlight)
        client.disconnect()
        
        print('Smartlight command published: ' + smartlight)


if __name__ == '__main__':
    
    main()