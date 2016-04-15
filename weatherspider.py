# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia  
# @Email: alwaysxiaop@gmail.com
# @Date:   2016-04-14 22:07:17
# @Last Modified time: 2016-04-16 01:39:01
# @FileName: weatherspider.py

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
        self.fileds = ['RunID','TemperatureH','TemperatureL','Description','Precip','Wind','Humidity','Time']
        self.quiet=quiet

    # ok
    def create_table(self):
        cu = self.con.cursor()
        cu.execute('''CREATE TABLE [WeatherBoulder] (
              [RunID] integer NOT NULL ON CONFLICT REPLACE PRIMARY KEY,
              [TemperatureH] integer,
              [TemperatureL] integer,
              [Description] varchar(10),
              [Precip] varchar(10),
              [Wind] varchar(40),
              [Humidity] varchar(40),
              [Time] datetime);
        ''')
        cu.execute('CREATE INDEX [RunID] ON [WeatherBoulder] ([RunID] ASC);')
        cu.close()

    def fetch_html(self):
        url = "https://weather.com/weather/5day/l/USCO0038:1:US"
        while True:
            success = True
            print("fetch ok {0}".format(time.localtime()))
            try:
                resp = self.s.get(url,timeout=5)
            except Exception, e:
                print e
                success = False
            else:
                print "status code=%s" % resp.status_code
                if resp.status_code != 200:
                    success = False
                if re.search(r'Please retry after (?P<time>\d+)ms\.Thank you\.',resp.text):
                    success = False
                    retry_time = re.search(r'Please retry after (?P<time>\d+)ms\.Thank you\.',resp.text).group('time');
                    retry_time = int(retry_time)/1000.0
                    print "too_often  retry after %.3f s" % retry_time
                    time.sleep(retry_time)
            if  success :
                break
        return resp

    def fetch(self):

        resp = self.fetch_html()
        print resp.encoding,type(resp)
        resp.encoding = "utf-8"
        f = open('t','wb')
        f.write(resp.content)
        f.close()
        patternstr = r'''
        <tr\s(bgcolor=\#D7EBFF\s)?align=center\s>
          <td.*?>(?P<RunID>\d+)</td>
          <td.*?>(?P<Submit_Time>.*?)</td>
          <td>(<a.*?>)?<font\scolor=.*?>(?P<Result>.*?)</font>(</a>)?</td>
          <td><a.*?>(?P<Problem>\d+)</a></td>
          <td>(?P<Time>\d+)MS</td>
          <td>(?P<Memory>\d+)K</td>
          <td>(?P<Code_Length>\d+)B</td>
          <td>(?P<Language>.*?)</td>
          <td.*?><a\shref=\"/userstatus.php\?user=(?P<User>.*?)\">.*?</a></td>
        </tr>
        '''
        pattern = re.compile(patternstr, re.S | re.VERBOSE)
        results = []
        for m in pattern.finditer(resp.text):
            line = {
                'RunID':m.group('RunID'),
                'TemperatureH':m.group('TemperatureH'),
                'TemperatureL':m.group('TemperatureL'),
                'Description':m.group('Description'),
                'Precip':m.group('Precip'),
                'Wind':m.group('Wind'),
                'Humidity':m.group('Humidity'),
                'Time':m.group('Time'),
                }
            results.append(line)
            # print line
        # print results
        print "got %d status" % len(results)
        if len(results) == 0:
            print resp.text
        self.insert(results)
        return results

    def insert(self,status):
        cu = self.con.cursor()
        status_array = []
        for s in status:
            sarr = []
            for key in self.fileds:
                sarr.append(s[key])
            status_array.append(sarr)
            if not self.quiet:
                print sarr
        # print status_array
        cu.executemany('INSERT OR REPLACE INTO HDU_Status Values(?,?,?,?,?,?,?,?,?)',status_array)
        self.con.commit()
        
    def make_up(self,detla,only_print=False,verify=False):
        cu = self.con.cursor()
        cu.execute("SELECT S1.RunID as A, S2.RunID as B from HDU_Status as S1,HDU_Status as S2 where B - A > ? and B = (select min(RunID) from HDU_Status where RunID > A) ORDER BY S1.RunID",[detla])
        bk = cu.fetchall()
        for A,B in bk:
            if verify:
                print "%8d --> %8d --> %8d  : %s" %(A,B-A,B,int(self.fetch(B)[0]['RunID']) == A)
            else:
                print "%8d --> %8d --> %8d" %(A,B-A,B)
            if not only_print:
                for i in xrange(A+20,B+20,20):
                    self.fetch(i)
    def main(self):
        # if begin == None:
        #     cu = self.con.cursor()
        #     cu.execute("select RunID from HDU_Status order by RunID DESC LIMIT 1")
        #     begin = cu.fetchone()
        #     if begin:
        #         begin = int(begin[0])
        #     else:
        #         begin = 15
        # if end == None:
        #     end = begin + 5000000
        # if end < begin:
        #     begin,end = end,begin
        # for i in xrange(begin,end,15):
        self.fetch()
            # time.sleep(0.1)

if __name__ == '__main__':
    filename = "weather.db"
    begin = None
    end = None
    detla = None
    quiet = False
    only_print = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],'f:b:e:m:hqp')
        for opt, val in opts:
            if opt == '-f':
                filename=val
            elif opt == '-b':
                begin = int(val)
            elif opt == '-e':
                end = int(val)
            elif opt == '-m':
                detla = int(val)
            elif opt == '-q':
                quiet = True
            elif opt == '-p':
                only_print = True
            elif opt == '-h':
                print "Usage:[-f filename],[-b begin_runid],[-e end_runid]"
                sys.exit()
    except getopt.GetoptError:
        print "Usage:[-f filename],[-b begin_runid],[-e end_runid],[-d missing_detla]"
        # print help information and exit:
    fetcher = weatherFetcher(filename=filename,quiet=quiet)
    if detla == None:
        fetcher.main()
    else:
        fetcher.make_up(detla=detla,only_print=only_print)

#合并表的方法
#INSERT OR REPLACE INTO HDU_Status SELECT * FROM HDU_status.HDU_Status
