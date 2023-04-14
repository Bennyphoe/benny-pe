import time

import sqlite3

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from joblib import dump, load



def main():
    
    print('Starting light cluster training process')
    
    np.random.seed(int(round(time.time())))

    while True:

        try:                        
            
            conn = sqlite3.connect('lightcloud.db')
    
            c = conn.cursor()
            c.execute('SELECT id, devicename, light, timestamp FROM light ORDER BY id ASC')
            results = c.fetchall()
            
            df = pd.DataFrame(columns=['id', 'devicename', 'light', 'timestamp'])
            # print(df)
            
            for result in results:                                
                
                df = df.append({'id': result[0], 'devicename': str(result[1]), 'light': result[2], 'timestamp': str(result[3])}, ignore_index=True)
                
            # print(df)
            
            X = df['light'].values.reshape(-1,1)
            
            # print(X)
            
            kmeans = KMeans(n_clusters=2, random_state=0)
            kmeans = kmeans.fit(X)
            result = pd.concat([df['light'], pd.DataFrame({'cluster':kmeans.labels_})], axis=1)
            
            # print(result)
            
            for cluster in result.cluster.unique():
                print('{:d}\t{:.3f} ({:.3f})'.format(cluster, result[result.cluster==cluster].light.mean(), result[result.cluster==cluster].light.std()))
            
            
            dump(kmeans, 'lightcluster.joblib')
            
            time.sleep(10)
                           

        except Exception as error:

            print('Error: {}'.format(error.args[0]))
            continue

        except KeyboardInterrupt:

            print('Program terminating...')    
            break



if __name__ == '__main__':
    
    main()
