import sys,os,re,csv,urllib2,glob
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import pymysql,logging
import pandas as pd
from secrets import *
import BeautifulSoup as bs4

names=[]
names.append('id')
names.append('name')
names.append('ascii_name')
names.append('alternate_names')
names.append('lat')
names.append('long')
names.append('feature') # feature class http://www.geonames.org/export/codes.html
names.append('feature code')
names.append('country')
names.append('country_alt') # weird other country something
names.append('admin1')
names.append('admin2')
names.append('admin3')
names.append('admin4')
names.append('population')
names.append('elevation')
names.append('elevation_dem')
names.append('timezone')
names.append('mod') # Date modified


files=glob.glob('files/*txt')

conn = pymysql.connect(host='localhost',user='root',passwd=PW, db='geo',charset='utf8')
cur = conn.cursor()

res=cur.execute('create table places (name varchar(100) character set utf8,clean_name varchar(100) character set utf8, lat float,lon float,country varchar(2),pop int, elevation mediumint)',)

#################
def clean(s):    
    return re.sub(r'\'|\.','',s.lower())

#################
def putFileInDB(f='files/AE.txt'):

    data=pd.read_csv(f,sep='\t',header=None)

    data.columns=names

    cmd="INSERT INTO places (name,clean_name,lat,lon,country,pop,elevation) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    for row in data.iterrows():

        ############################
        ## Original name
        temp=(row[1]['name'],clean(row[1]['name']),row[1].lat,row[1]['long'],row[1].country,row[1].population,row[1].elevation_dem)
        print temp
        
        res=cur.execute(cmd,temp)
        conn.commit()
        assert cur.rowcount==1
        
        ############################
        ## All alternate names
        try:
            for name in row[1]['alternate_names'].split(','):
                temp=(name,clean(name),row[1].lat,row[1]['long'],row[1].country,row[1].population,row[1].elevation_dem)

            res=cur.execute(cmd,temp)
            conn.commit()
        except:
            logging.warning('Error alternate names :%s' % row[1])
        
########################
def main():
    putFileInDB()

#########################
if __name__=="__main__":
    main()