# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia
# @Email: alwaysxiaop@gmail.com
# @Date:   2016-08-30 10:06:19
# @Last Modified time: 2016-09-03 16:23:34
# @FileName: web.py
import tornado.ioloop
import tornado.web
import sqlite3
import time


def getText(filename):
    con = sqlite3.connect(filename)
    cu = con.cursor()
    cu.execute("SELECT * from WeatherBoulder ORDER by RunID DESC LIMIT 10")
    res = cu.fetchall()
    # print bk,type(bk)
    items = []
    for i in range(len(res)):
        bk = res[i]
        # tornado.escape.xhtml_escape('\'')
        Text = '''
                The weather is updated at {0}. Now the temperature is about {1}°C.
                Today‘s temperature around {2}/{3}°C. And weather will be {4}.
                Also the wind is {5}mph and the humidity is {6}%.
            '''.format(bk[7], bk[1], bk[2], bk[3], bk[4], bk[5], bk[6])
        # tornado.escape.xhtml_escape(Text)
        items.append(Text)
        # print('[{0}] The text is:\n{1}'.format(time.strftime(
        #     "%Y-%m-%d %H:%M:%S", time.localtime()), Text))
    return items


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        items = getText('weather.db')
        # items = ["Item 1", "Item 2", "Item 3"]
        self.render("template.html", title="Boulder Weather Report", items=items)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
