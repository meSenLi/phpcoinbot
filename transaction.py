import datetime


class Transaction:
    def __init__(self, Id="", Date=datetime.datetime.now(), Height=0, Block="", From="", To="", Type="", Value=0.0, Fee=0.0):
        self.Id = Id
        self.Date = Date
        self.Height = Height
        self.Block = Block
        self.From = From
        self.To = To
        self.Type = Type
        self.Value = Value
        self.Fee = Fee

    def toJion(self):
        dick = {}
        dick["Id"] = self.Id
        dick["Date"] = self.Date.strftime('%Y-%m-%d %H:%M:%S')
        dick["Height"] = str(self.Height)
        dick["Block"] = self.Block
        dick["From"] = self.From
        dick["To"] = self.To
        dick["Type"] = self.Type
        dick["Vale"] = str(self.Value)
        dick["Fee"] = str(self.Fee)
        return dick

    def frmeJion(self, dick):
        tran = Transaction()

        tran.Id = dick["Id"]
        tran.Date = datetime.datetime.strptime(
            dick["Date"], "%Y-%m-%d %H:%M:%S")
        tran.Height = int(dick["Height"])
        tran.Block = dick["Block"]
        tran.From = dick["From"]
        tran.To = dick["To"]
        tran.Type = dick["Type"]
        tran.Value = float(dick["Value"])
        tran.Fee = float(dick["Fee"])
        return tran


class Wallet:

    def __init__(self, address="", public="", private="", transaction=[], balance=0.0, received=0.0, sent=0.0) -> None:
        self.Address = address
        self.Public = public
        self.__Private = private
        self.Transactions = transaction
        self.Balance = balance
        self.Received = received
        self.Sent = sent

    def send(self, address, value, message):
        pass

    def addTransactino(self, transaction=Transaction()):
        if not isinstance(transaction, Transaction):
            return False
        if transaction.From != self.Address and transaction.To != self.Address:
            return False
        for tran in self.Transactions:
            if tran.Id == transaction.Id:
                return True
        self.Transactions.append(transaction)
        return True

    def getTypeTransactions(self, type):
        ret = []
        for tran in self.Transactions:
            if tran.Type == type:
                ret.append(tran)
        return ret

    def getTodayReward(self, type):
        trans = []
        end = datetime.datetime.now()
        now = end + datetime.timedelta(hours=8)
        start = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                         microseconds=now.microsecond) - datetime.timedelta(hours=8)
        income = 0.0
        for tran in self.getTypeTransactions(type):
            if (start <= tran.Date <= end):
                income = income + tran.Value
            else:
                break
        return income

    def getTypeAverageTime(self, type, numb):
        if numb < 1:
            return datetime.timedelta()
        trans = self.getTypeTransactions(type)
        if len(trans) < 2:
            return datetime.timedelta()
        time = datetime.timedelta()
        last = trans[0]
        for item in trans[1:numb + 1]:
            time = time + last.Date - item.Date
            last = item
        size = min(numb, len(trans) - 1)
        return datetime.timedelta(seconds=time.total_seconds/size)

    def getTypeAverageBlock(self, type, numb=None):
        trans = self.getTypeTransactions(type)
        if not numb:
            numb = len(trans)
        if len(trans) < 2 or numb < 1:
            return 0.0
        time = 0.0
        last = trans[0]
        for item in trans[1:numb + 1]:
            time = time + last.Height - item.Height
            last = item
        size = min(numb, len(trans) - 1)
        return time/size

    def toJion(self):
        dick = {}
        dick["Address"] = self.Address
        dick["Public"] = self.Public
        dick["Received"] = str(self.Received)
        dick["Sent"] = str(self.Sent)
        dick["Balance"] = str(self.Balance)
        return dick

    def frmeJion(self, dick):
        wallet = Wallet()
        wallet.Address = dick["Address"]
        wallet.Public = dick["Public"]
        wallet.Received = float(dick["Received"])
        wallet.Sent = float(dick["Sent"])
        wallet.Balance = float(dick["Balance"])
        return wallet
