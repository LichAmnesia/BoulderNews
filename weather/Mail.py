# -*- coding: utf-8 -*-
# @Author: Lich_Amnesia
# @Email: alwaysxiaop@gmail.com
# @Date:   2016-04-19 22:20:19
# @Last Modified time: 2016-04-21 13:51:02
# @FileName: Mail.py

# -*- coding: utf-8 -*-
'''
发送html文本邮件
'''

import smtplib
from email.mime.text import MIMEText
import sqlite3
import yaml


class weatherMail(object):
    """docstring for weatherMail"""

    def __init__(self, arg=None, filename=None):
        super
        (weatherMail, self).__init__()

        self.stream = file('Mail.yaml', 'r')
        self.dic = yaml.load(self.stream)
        if filename == None:
            self.mailto_list = ["alwaysxiaop@gmail.com", "chen3221@126.com"]
        else:
            # 修改为可配置的文件
            self.mailto_list = [""]

        self.mail_host = self.dic['mail_host']  # 设置服务器
        self.mail_user = self.dic['mail_user']  # 用户名
        self.mail_pass = self.dic['mail_pass']  # 口令
        self.mail_postfix = self.dic['mail_postfix']  # 发件箱的后缀
        self.mail_file = "weather.db"

        self.arg = arg

    def sendMail(self, to_list, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
        me = "Lich_Amnesia" + "<" + self.mail_user + "@" + \
            self.mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
        # 创建一个实例，这里设置为html格式邮件
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        msg['Subject'] = sub  # 设置主题
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP()
            s.connect(self.mail_host)  # 连接smtp服务器
            s.login(self.mail_user, self.mail_pass)  # 登陆服务器
            s.sendmail(me, to_list, msg.as_string())  # 发送邮件
            s.close()
            return True
        except Exception, e:
            print str(e)  # print error log
            return False

    def getText(self, filename):
        con = sqlite3.connect(filename)
        cu = con.cursor()
        cu.execute("SELECT * from WeatherBoulder ORDER by RunID DESC LIMIT 1")
        bk = cu.fetchone()
        # print bk,type(bk)
        Text = '''       
            Today is {0}. Today's temperature is 10°C. And weather is {1}. Also the wind is {2}mph and the humidity is {3}%.
        '''.format(bk[5], bk[2], bk[3], bk[4])
        print Text
        return Text

    def main(self):
        # stream = file('Mail.yaml', 'r')
        # dic =  yaml.load(stream)
        # mailto_list=["alwaysxiaop@gmail.com","chen3221@126.com"]
        # mail_host=dic['mail_host'] #设置服务器
        # mail_user=dic['mail_user']   #用户名
        # mail_pass=dic['mail_pass']  #口令
        # mail_postfix=dic['mail_postfix']  #发件箱的后缀

        # mail_file = "weather.db"

        mail_text = self.getText(self.mail_file)
        # exit()
        if self.sendMail(self.mailto_list, "BoulderNews", mail_text):
            print "发送成功"
        else:
            print "发送失败"

if __name__ == '__main__':
    mail = weatherMail()
    mail.main()