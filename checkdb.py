import  sqlite3
#import pytz

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

# for row in db.execute("SELECT * FROM history"):
#     utcT = row[0]
#     localT = pytz.utc.localize(utcT).astimezone()
#     print("{}\t{}".format(utcT, localT))


# for row in db.execute("SELECT strftime('%Y-%m-%d %H:%M:%f',history.time,'localtime') AS locatime,"
#                       "history.account, history.amount FROM history ORDER BY history.time"):
#     print(row)


for row in db.execute("SELECT * FROM history"):
    print(row)


db.close()
