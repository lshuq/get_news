from imp import reload

import MySQLdb
import datetime

conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='dede',
)
conn.set_character_set('utf8')
cur = conn.cursor()
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')


def upload(content, title):
    d = datetime.datetime.now()
    t = int(d.timestamp())
    id = 110
    while 1:
        try:
            sqli1 = "insert into dede_addonarticle values(%s,%s,%s,%s,%s,%s)"
            cur.execute(sqli1, (id, 12, content, u'', u'', u"0.0.0.0"))
            sqli = "insert into dede_archives values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sqli, (
                id, 12, '0', t, '', 1, 1, 0, 0, 0, title, '', '', 'admin', '??', '', t, t, 1, '??,test,', 0,
                0, 0, 0, 0, 0, 'test', '', 0, 0, 0, 0))
            print("success")
            break
        except:
            id += 1
    return id
