import sys,os,re,csv,urllib2,glob
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import pymysql,logging,traceback
import pandas as pd
from secrets import *
import bs4

hdlr = logging.FileHandler('log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)

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

res=cur.execute('create table places (name varchar(100) character set utf8,clean_name varchar(100) character set utf8, \
lat float,lon float,country varchar(2),pop int, elevation mediumint, admin_name varchar(10), feature varchar(10))',)
## Create table

res=cur.execute('create index place_index on places(name)',)
# Create index

#################
def clean(s):
    return re.sub(r'\'|\.','',s.lower())

#################
def putFileInDB(f='files/AE.txt'):

    nError=0
    
    logging.info('Reading in %s' % f)
        
    try:
        data=pd.read_csv(f,sep='\t',header=None,low_memory=False)

        data.columns=names
    except:
        print 'Error reading in %s' % f
        logging.warning('Error reading in %s' % f)
        return

    cmd="INSERT INTO places (name,clean_name,lat,lon,country,pop,elevation,admin_name,feature) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    for row in data.iterrows():

        ############################
        ## Original name

        tempAdmin=row[1].admin1
        if pd.isnull(tempAdmin):
            tempAdmin=''
        # Check if admin level 1 is null
        # Update this later to level 2
        try:
            temp=(row[1]['name'],clean(row[1]['name']),row[1].lat,row[1]['long'],row[1].country,row[1].population,row[1].elevation_dem,tempAdmin,row[1]['feature code'])

            res=cur.execute(cmd,temp)
            conn.commit()
            assert cur.rowcount==1
        except:
            nError+=1
            print traceback.print_exc()
        ############################
        ## All alternate names
        if not pd.isnull(row[1]['alternate_names']):
            try:
                for name in row[1]['alternate_names'].split(','):
                    temp=(name,clean(name),row[1].lat,row[1]['long'],row[1].country,row[1].population,row[1].elevation_dem,tempAdmin,row[1]['feature code'])

                    res=cur.execute(cmd,temp)
                    conn.commit()
            except:
    #            logging.warning('Error alternate names')
                nError+=1
                pass
    print '%d errors, %d total' % (nError,data.shape[0])
    logging.info('%d errors, %d total' % (nError,data.shape[0]))

########################
def main():
    files=glob.glob('files/*txt')
    files.sort()

    switch=True

    for f in files:
        print f

        #if f=='files/SY.txt':
        #    switch=True

        if True:#f=='files/SY.txt':
            putFileInDB(f=f)
        else:
            print 'Skipping',f
#########################
if __name__=="__main__":
    main()
