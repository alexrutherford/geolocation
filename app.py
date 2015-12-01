from flask import Flask

import sys,os,re,csv,urllib2
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import pymysql
import pandas as pd
from secrets import * # PW
import logging
import utils,nltk

stopWords=nltk.corpus.stopwords.words('english')

hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)

app = Flask(__name__)
app.debug=True
app.logger.addHandler(hdlr)

######################
'''Test to see if country string is valid
'''
def isCountryStringValid(countryString):
    if not len(countryString)==2 or not all(map(lambda x:x.isalpha(),countryString)):
        return False

    return True

######################
def handleLocationString(locationString):
    '''Cleans location string
    '''
    try:
        locationString=utils.clean(locationString)
    except:
        app.logger.warning('Error parsing location string: %s' % locationString)
        return ('location string not parsed',400)
    return locationString
######################
@app.route('/loc=<string:locationString>&langs=<string:langString>', methods = ['GET'])
def searchByLang(locationString,langString):
    '''API call to get places matching @locationString
    and from countries with comma separated list of
    ISO 2 language codes @langs
    '''

    locationString=handleLocationString(locationString)

    conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
    cur = conn.cursor()

    try:
        langs=langString.split(',')

    except:
        app.logger.warning('Invalid langs: %s' % langString)
        return ('langs list not valid',400)

    if not all([len(l)==2 for l in langs]):
        app.logger.warning('Invalid langs: %s' % langString)
        return ('langs must be 2 letter ISO codes',400)

    query="""select distinct iso2 from language where lang_iso in (%s)""" % (','.join(["'%s'" % l for l in langs]))
    res=pd.read_sql_query(query,conn)
    countries=res.iso2.values
    conn.commit()
    # Get countries that match languages

    if res.shape[0]==0:
        app.logger.warning('Langs not found: %s' % langString)
        return ('langs list not found',400)

    query="""select * from places where name='%s' and country in (%s)""" % (locationString,','.join(["'%s'" % c for c in countries]))
    res=pd.read_sql_query(query,conn)
    conn.commit()
    # Get places that match location in countries that match languages

    return (res.to_json(orient='records'),200)

######################
@app.route('/loc=<string:locationString>&country=<string:countryString>', methods = ['GET'])
def searchInCountry(locationString,countryString):
    '''API call to get places matching @locationString
    located in country given by ISO 2 code @countryString
    '''

    locationString=handleLocationString(locationString)

    conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
    cur = conn.cursor()

    if not isCountryStringValid(countryString):
        return ('country string not valid: must be ISO 2 letter code',400)

    query="""select * from places where name='%s' and country='%s'""" % (locationString,countryString)
    res=pd.read_sql_query(query,conn)
    conn.commit()

    return (res.to_json(orient='records'),200)

######################
@app.route('/loc=<string:locationString>', methods = ['GET'])
def search(locationString):
    '''API call to search for places matching @locationString
    '''

    locationString=handleLocationString(locationString)

    conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
    cur = conn.cursor()

    query="""select * from places where name='%s'""" % locationString

    res=pd.read_sql_query(query,conn)
    res=res.sort(columns=['pop'],ascending=False)

    conn.commit()

    return (res.to_json(orient='records'),200)
######################
@app.route('/raw/loc=<string:locationString>&country=<string:countryString>', methods = ['GET'])
def searchRawCountry(locationString,countryString):
    '''API call to search for places matching @locationString
    which can be raw free form text i.e. a phrase, sentence or post
    With country restriction
    '''

    locationString=handleLocationString(locationString)
    # Returns cleaned string

    if not isCountryStringValid(countryString):
        return ('country string not valid: must be ISO 2 letter code',400)

    conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
    cur = conn.cursor()

    tokenResults=[]

    tokens=locationString.split(' ')
    tokens=set(tokens)
    tokens=filter(lambda x:len(x)>0,tokens)

    for token in filter(lambda x:x not in stopWords and len(x)>2,tokens):

        query="""select * from places where name='%s' and country='%s'""" % (token,countryString)

        res=pd.read_sql_query(query,conn)

        tokenResults.append(res)

        conn.commit()

    res=pd.concat(tokenResults)
    res.drop_duplicates()
    res=res.sort(columns=['pop'],ascending=False)

    return (res.to_json(orient='records'),200)

######################
@app.route('/raw/loc=<string:locationString>', methods = ['GET'])
def searchRaw(locationString):
    '''API call to search for places matching @locationString
    which can be raw free form text i.e. a phrase, sentence or post
    '''

    locationString=handleLocationString(locationString)
    # Returns cleaned string

    conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
    cur = conn.cursor()

    tokenResults=[]

    tokens=locationString.split(' ')
    tokens=set(tokens)
    tokens=filter(lambda x:len(x)>0,tokens)

    for token in filter(lambda x:x not in stopWords and len(x)>2,tokens):

        query="""select * from places where name='%s'""" % token

        res=pd.read_sql_query(query,conn)

        tokenResults.append(res)

        conn.commit()

    res=pd.concat(tokenResults)
    res.drop_duplicates()
    res=res.sort(columns=['pop'],ascending=False)

    return (res.to_json(orient='records'),200)
######################
if __name__ == "__main__":
    app.run()
