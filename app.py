from flask import Flask

import sys,os,re,csv,urllib2
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import pymysql
import pandas as pd
from secrets import *

conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
cur = conn.cursor()

app = Flask(__name__)
app.debug=True

@app.route('/loc=<string:locationString>', methods = ['GET'])
def search(locationString):
    
    query="""select * from places where clean_name='%s'""" % locationString
    
#    cur.execute(query)
 
    res=pd.read_sql_query(query,conn)

    return res.to_json(orient='records')

if __name__ == "__main__":
    app.run()