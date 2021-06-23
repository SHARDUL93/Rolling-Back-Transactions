import sqlite3
import datetime
import pytz
import pickle


db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS accounts(name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL, account TEXT NOT NULL, amount INTEGER NOT NULL, zone INTEGER NOT NULL, PRIMARY KEY(time, account))")
db.execute("CREATE VIEW IF NOT EXISTS localhistory AS SELECT strftime('%Y-%m-%d %H:%M:%f',history.time,'localtime') AS locatime,"
                      "history.account, history.amount FROM history ORDER BY history.time")


class Account(object):

    @staticmethod
    def _cur_time():
        # return pytz.utc.localize(datetime.datetime.utcnow())
        # local_time = pytz.utc.localize(datetime.datetime.utcnow())
        # return local_time.astimezone()

        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone()
        zone = local_time.tzinfo
        return utc_time, zone


    def __init__(self, name: str, op_bal: int = 0.0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE(name = ?)",(name,))
        row = cursor.fetchone()

        if row:
            self.name, self._bal = row
            print("Retrieved record for {}".format(self.name),end='')
        else:
            self.name = name
            self._bal = op_bal
            cursor.execute("INSERT INTO accounts VALUES(?,?)",(name, op_bal))
            cursor.connection.commit()
            print("Account created for {}".format(self.name),end='')
        self.show_bal()


    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_bal = self._bal+amount
            # dep_time = Account._cur_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)",(new_bal, self.name))
            # db.execute("INSERT INTO history VALUES(?,?,?)",(dep_time, self.name, amount))
            # db.commit()
            # self._bal = new_bal
            self._save_up(amount)
            print("{:.2f} deposited".format(amount/100))
        return self._bal/100


    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._bal:
            # new_bal = self._bal-amount
            # with_time = Account._cur_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)",(new_bal, self.name))
            # db.execute("INSERT INTO history VALUES(?,?,?)",(with_time, self.name, -amount))
            # db.commit()
            # self._bal = new_bal
            self._save_up(-amount)
            print("{:.2f} withdrawn".format(amount/100))
            return amount/100
        else:
            print("Rejected")
            return 0.0

    def show_bal(self):
        print("\tBalance on account {} is {:.2f} ".format(self.name, self._bal/100))


    def _save_up(self, amount):
        new_bal = self._bal+amount
        dep_time, zone = Account._cur_time()  #<-- unpacking return tuple
        picked_zone = pickle.dumps(zone)
        db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)",(new_bal, self.name))
        db.execute("INSERT INTO history VALUES(?,?,?,?)",(dep_time, self.name, amount,picked_zone))
        db.commit()
        self._bal = new_bal


if __name__ =="__main__":
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_bal()

    terry = Account("TerryJ.")
    graham = Account("Graham",9000)
    eric = Account("Eric",7000)
    michel = Account("Michael")
    terryG = Account("TerryG.")

    db.close()





