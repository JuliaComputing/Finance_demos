from ibapi import wrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper #just for decorator
from ibapi.common import *
from ibapi.contract import *
from ibapi.ticktype import *
from io import StringIO
import sys

class TestApp(wrapper.EWrapper, EClient):
    def __init__(self):
        wrapper.EWrapper.__init__(self)
        EClient.__init__(self, wrapper=self)
        self.count = 0
        self.array = []

    @iswrapper
    def nextValidId(self, orderId:int):
        print("nextValidOrderId:", orderId)
        self.nextValidOrderId = orderId

        #here is where you start using api
        contract = Contract()
        contract.symbol = "GOOG"
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.lastTradeDateOrContractMonth = "20200605"
        #contract.strike = 1050
        contract.right = "C"
        contract.multiplier = "100"
        self.reqMarketDataType(3)
        for i in [900,950,1000,1050,1100]:
            self.nextValidOrderId = i
            contract.strike = i
            self.reqMktData(i, contract, "", False, False,[])
    @iswrapper
    def historicalData(self,reqId, bar):
        self.array.append(bar.close)

    @iswrapper
    def error(self, reqId:TickerId, errorCode:int, errorString:str):
        pass
        #print("Error. Id: " , reqId, " Code: " , errorCode , " Msg: " , errorString)

    @iswrapper
    def tickPrice(self, reqId: TickerId , tickType: TickType, price: float,
                  attrib:TickAttrib):
        print("Tick Price. Ticker Id:", reqId,
              "tickType:", TickTypeEnum.to_str(tickType),
              "Price:", price)
        self.count += 1
        if self.count > 10 : 
            #self.done = True
            self.disconnect()

#app = TestApp()
#app.connect("127.0.0.1", 4002, clientId=1)
#print("serverVersion:%s connectionTime:%s", app.serverVersion(),app.twsConnectionTime())
#app.run()

def main():
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    try:
        app = TestApp()
        app.connect("127.0.0.1", 4002, clientId=0)
        print("serverVersion:%s connectionTime:%s" % (app.serverVersion(),app.twsConnectionTime()))
        app.run()
    except:
        pass
    sys.stdout = old_stdout
    output = mystdout.getvalue()
    print(output)
    text_file = open("output.txt", "w")
    text_file.write(output)
    text_file.close()
    d = {}
    #output = "".join(output)
    #output = output.split()
    with open("output.txt") as f:
        lines = f.readlines()
        for line in lines:
            print(line)
            if "DELAYED_CLOSE" in line:
                elements = line.split()
                d[int(float(elements[4]))] = float(elements[-1])
    print("dict ", d)
    return d
if __name__ == "__main__":
    main()
