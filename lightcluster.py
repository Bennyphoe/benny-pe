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
            c.execute('SELECT id, devicename, abright, atemp, ahum, timestamp FROM light ORDER BY id ASC')
            results = c.fetchall()
            
            df = pd.DataFrame(columns=['id', 'devicenane', 'abright', 'atemp', 'ahum', 'timestamp'])
            # print(df)
            
            for result in results:                                
                
                df = df.append({'id': result[0], 'devicename': str(result[1]), 'abright': result[2], 'atemp': result[3], 'ahum': result[4], 'timestamp': str(result[5])}, ignore_index=True)
                
            # print(df)
            
            X = df['abright'].values.reshape(-1,1)
            X = df['atemp'].values.reshape(-1,1)
            X = df['ahum'].values.reshape(-1,1)
            
            # print(X)
            
            kmeans = KMeans(n_clusters=2, random_state=0)
            kmeans = kmeans.fit(X)
            result = pd.concat([df['abright'], df['atemp']])
            result = pd.concat([result, df['ahum']])
            result = pd.concat([result, pd.DataFrame({'cluster':kmeans.labels_})], axis=1)
            
            # print(result)
            
            for cluster in result.cluster.unique():
                print('{:d}\t{:.3f} ({:.3f})'.format(cluster, result[result.cluster==cluster].abright.mean(), result[result.cluster==cluster].abright.std()))
                print('{:d}\t{:.3f} ({:.3f})'.format(cluster, result[result.cluster==cluster].atemp.mean(), result[result.cluster==cluster].atemp.std()))
                print('{:d}\t{:.3f} ({:.3f})'.format(cluster, result[result.cluster==cluster].ahum.mean(), result[result.cluster==cluster].ahum.std()))
            
            
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
