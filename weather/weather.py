# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia
# @Email: alwaysxiaop@gmail.com
# @Date:   2016-04-15 19:02:42
# @Last Modified time: 2016-04-24 20:25:11
# @FileName: weather.py

import urllib2
import urllib
import json
import sqlite3
import requests
import re
import datetime
import time
import getopt
import sys
import os
import Mail


class weatherFetcher(object):
    """docstring for weatherFetcher"""

    def __init__(self, arg=None, filename=None, quiet=False):
        super
        (weatherFetcher, self).__init__()
        self.arg = arg
        # Sqlite
        self.con = sqlite3.connect(filename)
        try:
            self.create_table()
        except Exception, e:
            if re.match(r'table .* already exists', e.message):
                print "table already exists"
            else:
                raise e
        else:
            print "create table WeatherBoulder successfully"
        # requests
        self.s = requests.Session()
        self.fileds = ['RunID', 'Temperature', 'TemperatureH', 'TemperatureL',
                       'Description', 'Wind', 'Humidity', 'Time']
        self.mail = Mail.weatherMail()

    def create_table(self):
        cu = self.con.cursor()
        cu.execute('''CREATE TABLE [WeatherBoulder] (
              [RunID] integer NOT NULL ON CONFLICT REPLACE PRIMARY KEY,
              [Temperature] integer,
              [TemperatureH] integer,
              [TemperatureL] integer,
              [Description] varchar(40),
              [Wind] integer,
              [Humidity] integer,
              [Time] varchar(40));
        ''')
        cu.execute('CREATE INDEX [RunID] ON [WeatherBoulder] ([RunID] ASC);')
        cu.close()

    def fetch_html(self, url):
        while True:
            success = True
            print("[{0}] fetch ok ".format(time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime())))
            try:
                resp = self.s.get(url, timeout=5)
            except Exception, e:
                print e
                success = False
                time.sleep(5)
            else:
                print("[{0}] status code: {1}".format(time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()), resp.status_code))
                if resp.status_code != 200:
                    success = False
                    time.sleep(5)
            if success:
                break
        return resp

    def cacl(self, ftemp):
        return int(round((float(ftemp) - 32.0) / 1.8))

    def fetch(self):
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid=2367231"
        yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"

        resp = self.fetch_html(yql_url)
        # result = urllib2.urlopen(yql_url).read()
        data = json.loads(resp.content)
        # data = data.encode('utf-8')
        line = {
            'RunID': self.getRunID(),
            'Temperature': self.cacl(data['query']['results']['channel']['item']['condition']['temp']),
            'TemperatureH': self.cacl(data['query']['results']['channel']['item']['forecast'][0]['high']),
            'TemperatureL': self.cacl(data['query']['results']['channel']['item']['forecast'][0]['low']),
            'Description': data['query']['results']['channel']['item']['forecast'][0]['text'].encode('utf-8'),
            'Wind': int(data['query']['results']['channel']['wind']['speed']),
            'Humidity': int(data['query']['results']['channel']['atmosphere']['humidity']),
            'Time': data['query']['results']['channel']['item']['condition']['date'].encode('utf-8'),
        }

        print('[{2}] RunID = {0}. Got {1} fields.'.format(line['RunID'], len(line), time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())))
        self.insert(line)
        return line

    def getRunID(self):
        RunID = 1
        cu = self.con.cursor()
        cu.execute("SELECT RunID from WeatherBoulder ORDER by RunID DESC LIMIT 1")
        bk = cu.fetchone()
        if bk is None or len(bk) == 0:
            RunID = 1
        else:
            RunID = bk[0] + 1
        return RunID

    def insert(self, status):
        cu = self.con.cursor()
        status_array = []
        s = []
        for key in self.fileds:
            s.append(status[key])
        status_array.append(s)
        cu.executemany(
            'INSERT OR REPLACE INTO WeatherBoulder Values(?,?,?,?,?,?,?,?)', status_array)
        self.con.commit()

    def print_ts(self, message):
        print "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message)

    def run(self, interval):
        self.print_ts("-" * 100)
        self.print_ts("Starting every %s seconds." % interval)
        self.print_ts("-" * 100)
        while True:
            try:
                # sleep for the remaining seconds of interval
                time_remaining = interval - time.time() % interval
                self.print_ts("Sleeping until %s (%s seconds)..." % (
                    (time.ctime(time.time() + time_remaining)), time_remaining))
                time.sleep(time_remaining)
                self.print_ts("Starting command.")
                # execute the command
                self.fetch()
                # 发送邮件
                self.mail.main()
                self.print_ts("-" * 100)
            except Exception, e:
                print e


if __name__ == '__main__':
    filename = "weather.db"
    fetcher = weatherFetcher(filename=filename)
    interval = 20
    fetcher.run(interval)
