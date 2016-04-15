# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia  
# @Email: alwaysxiaop@gmail.com
# @Date:   2016-04-15 19:02:42
# @Last Modified time: 2016-04-16 01:45:45
# @FileName: weather.py

import urllib2, urllib, json
import sqlite3
import requests
import re
import datetime
import time
import getopt, sys

class weatherFetcher(object):
    """docstring for weatherFetcher"""
    def __init__(self, arg=None,filename=None,quiet=False):
        super
        (weatherFetcher, self).__init__()
        self.arg = arg
        #Sqlite
        self.con = sqlite3.connect(filename)
        try:
            self.create_table()
        except Exception, e:
            if re.match(r'table .* already exists',e.message):
                print "table already exists"
            else:
                raise e
        else:
            print "create table WeatherBoulder successfully"
        #requests
        self.s = requests.Session()
        self.fileds = ['RunID','Temperature','Description','Wind','Humidity','Time']
        self.quiet=quiet

    def create_table(self):
        cu = self.con.cursor()
        cu.execute('''CREATE TABLE [WeatherBoulder] (
              [RunID] integer NOT NULL ON CONFLICT REPLACE PRIMARY KEY,
              [TemperatureL] integer,
              [Description] varchar(10),
              [Wind] integer,
              [Humidity] integer,
              [Time] varchar(40));
        ''')
        cu.execute('CREATE INDEX [RunID] ON [WeatherBoulder] ([RunID] ASC);')
        cu.close()

    def fetch_html(self,url):
        while True:
            success = True
            print("fetch ok {0}".format(time.localtime()))
            try:
                resp = self.s.get(url,timeout=5)
            except Exception, e:
                print e
                success = False
                time.sleep(5)
            else:
                print "status code=%s" % resp.status_code
                if resp.status_code != 200:
                    success = False
                    time.sleep(5)
            if  success :
                break
        return resp 


    def cacl(self,ftemp):
        return round((float(ftemp) - 32.0) / 1.8)

    def fetch(self):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid=2367231"
        yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"

        resp = self.fetch_html(yql_url)
        # result = urllib2.urlopen(yql_url).read()
        data = json.loads(resp.content)

        line = {
            'RunID':data['query']['results']['channel']['item']['condition']['date'],
            'Temperature':self.cacl(data['query']['results']['channel']['item']['condition']['temp']),
            'Description':data['query']['results']['channel']['item']['condition']['text'],
            'Wind':int(data['query']['results']['channel']['wind']['speed']),
            'Humidity':int(data['query']['results']['channel']['atmosphere']['humidity']),
            'Time':data['query']['results']['channel']['item']['condition']['date'],
        }
        print line        
        print "got %d status" % len(line)
        
        self.getRunID()
        # self.insert(line)
        return line

    def getRunID(self):
        RunID = 1
        cu = self.con.cursor()
        cu.execute("SELECT RunID from WeatherBoulder ORDER by RunID DESC LIMIT 1")
        bk = cu.fetchall()
        if len(bk) == 0:
            RunID = 1
        else:
            RunID = bk[0] + 1
        print RunID
        return RunID

    def insert(self,status):
        cu = self.con.cursor()
        status_array = []
        
        for key in self.fileds:
            status_array.append(status[key])
        print status_array
        cu.executemany('INSERT OR REPLACE INTO HDU_Status Values(?,?,?,?,?,?,?,?,?)',status_array)
        self.con.commit()



def fetch():
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = "select * from weather.forecast where woeid=2367231"
    yql_url = baseurl + urllib.urlencode({'q':yql_query}) + "&format=json"
    result = urllib2.urlopen(yql_url).read()
    data = json.loads(result)
    # print data['query']['results']
    line = {
        'RunID':data['query']['results']['channel']['item']['condition']['date'],
        'Temperature':cacl(data['query']['results']['channel']['item']['condition']['temp']),
        'Description':data['query']['results']['channel']['item']['condition']['text'],
        'Wind':int(data['query']['results']['channel']['wind']['speed']),
        'Humidity':int(data['query']['results']['channel']['atmosphere']['humidity']),
        'Time':data['query']['results']['channel']['item']['condition']['date'],
        }
    print line
    # print data['query']['results']['channel']['item']['condition']['date']
    # print data['query']['results']['channel']['item']['condition']['text']
    # print data['query']['results']['channel']['item']['condition']['temp']
    # print data['query']['results']['channel']['wind']['speed']
    # print data['query']['results']['channel']['atmosphere']['humidity']

if __name__ == '__main__':
    filename = "weather.db"
    begin = None
    end = None
    detla = None
    quiet = False
    only_print = False
    # try:
    #     opts, args = getopt.getopt(sys.argv[1:],'f:b:e:m:hqp')
    #     for opt, val in opts:
    #         if opt == '-f':
    #             filename=val
    #         elif opt == '-b':
    #             begin = int(val)
    #         elif opt == '-e':
    #             end = int(val)
    #         elif opt == '-m':
    #             detla = int(val)
    #         elif opt == '-q':
    #             quiet = True
    #         elif opt == '-p':
    #             only_print = True
    #         elif opt == '-h':
    #             print "Usage:[-f filename],[-b begin_runid],[-e end_runid]"
    #             sys.exit()
    # except getopt.GetoptError:
    #     print "Usage:[-f filename],[-b begin_runid],[-e end_runid],[-d missing_detla]"
        # print help information and exit:
    fetcher = weatherFetcher(filename=filename,quiet=quiet)
    if detla == None:
        fetcher.fetch()
    else:
        fetcher.make_up(detla=detla,only_print=only_print)