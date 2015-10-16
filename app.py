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

######################
@app.route('/loc=<string:locationString>&langs=<string:langs>', methods = ['GET'])
def searchByLang(locationString,langs):
    
    try:
        langs=langs.split(',')
    except:
        return ('langs list not valid',400)
    
#    return ','.join(["'%s'" % l for l in langs])

    query="""select distinct iso2 from language where lang_iso in (%s)""" % (','.join(["'%s'" % l for l in langs]))
    # select distinct iso2 from language where language in ('spanish','english');
 
    res=pd.read_sql_query(query,conn)

    countries=res.iso2.values
        
#    return query
        
#    return '>>'+','.join(["'%s'" % c for c in countries])

    query="""select * from places where clean_name='%s' and country in (%s)""" % (locationString,','.join(["'%s'" % c for c in countries]))

    res=pd.read_sql_query(query,conn)
    
    conn.commit()
    
    return (res.to_json(orient='records'),200)
    
    return '%s' % langs

######################
@app.route('/loc=<string:locationString>&country=<string:countryString>', methods = ['GET'])
def searchInCountry(locationString,countryString):
    
    if not len(countryString)==2:
        return ('country string not valid: must be ISO 2 letter code',400)
    
    query="""select * from places where clean_name='%s' and country='%s'""" % (locationString,countryString)

    res=pd.read_sql_query(query,conn)
    
    conn.commit()
    
    return (res.to_json(orient='records'),200)

######################
@app.route('/loc=<string:locationString>', methods = ['GET'])
def search(locationString):
    
    query="""select * from places where clean_name='%s'""" % locationString
     
    res=pd.read_sql_query(query,conn)
    
    conn.commit()

    return (res.to_json(orient='records'),200)

######################
if __name__ == "__main__":
    app.run()