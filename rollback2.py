class Account(object):

    def __init__(self, name: str, op_bal: float = 0.0):
        self.name = name
        self._bal = op_bal
        print("Account created for {}".format(self.name),end='')
        self.show_bal()


    def deposit(self, amount: float) -> float:
        if amount > 0.0:
            self._bal += amount
            print("{} deposited".format(amount))
        return self._bal


    def withdraw(self, amount: float) -> float:
        if 0 < amount <= self._bal:
            self._bal -= amount
            print("{} withdrawn".format(amount))
            return amount
        else:
            print("Rejected")
            return 0.0

    def show_bal(self):
        print("Balance on account {} is {} ".format(self.name, self._bal))



if __name__ =="__main__":
    john = Account("John")
    john.deposit(10.10)
    john.deposit(0.10)
    john.deposit(0.10)
    john.withdraw(0.30)
    john.withdraw(0)
    john.show_bal()






