import threading
import time    
import datetime    
from colorama import Fore

class Bank(threading.Thread):
    def __init__(self,balance,bank_id):
        threading.Thread.__init__(self)
        self.balance=balance # dictionary
        self.semaphore=threading.Semaphore(1)
        self.WorkingHour=False
        self.id=bank_id
    def load(self,Em1,Em2,Em3,boss):
        self.Register_Employee=Em1
        self.Deposit_Employee =Em2
        self.Withdraw_Employee=Em3
        self.boss=boss
    def run(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.GREEN+f"   {self.id}:Bank is Open!")
        while self.WorkingHour:
            pass
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.GREEN+f"   {self.id}:The Bank is Closed!")

class Customer(threading.Thread):
    def __init__(self,bank,task,customer_id):
        threading.Thread.__init__(self)
        self.bank=bank
        self.task=task # dictionary
        self.id=customer_id
        self.alive=True
    def run(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTRED_EX+f"   customer {self.id} Entered!")
        time.sleep(0.1)
        if self.task['task']=="deposit":
            self.bank.Deposit_Employee.add(self)
        if self.task['task']=="withdraw":
            self.bank.Withdraw_Employee.add(self)
        if self.task['task']=="register":
            self.bank.Register_Employee.add(self)
        self.wait()
    def wait(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTRED_EX+f"   customer {self.id}: I'm waiting in Queue!")
        while self.alive:
            pass
    def stop(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTRED_EX+f"   customer {self.id}: I'm leaving the Bank. Have a good day!")
        self.alive=False

class Employee(threading.Thread):
    def __init__(self,bank,employee_id,role):
        threading.Thread.__init__(self)
        self.bank=bank
        self.Queue=[]
        self.id=employee_id
        self.role=role
    
    def run(self):
        if self.role=="deposit":
            self.Deposit()
        if self.role=="withdraw":
            self.Withdraw()
        if self.role=="register":
            self.Register()

    def Register(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTMAGENTA_EX+f"   Employee {self.id}: I'm waiting for Customer...")
        while len(self.Queue)==0 and self.bank.WorkingHour:
            pass
        if not self.bank.WorkingHour:
            self.clear()
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTMAGENTA_EX+f"   Employee {self.id}: I’m outta here!")
            exit(0)
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTMAGENTA_EX+f"   Employee {self.id}: it seems i have one")
        customer_id = self.Queue[0].id
        self.bank.semaphore.acquire()
        if self.bank.balance.get(customer_id):
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}"+Fore.LIGHTMAGENTA_EX+f"   Employee {self.id}:You already have account!")
        else:
            self.bank.balance[customer_id]=0
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id}:Register customer {customer_id} is Done!  ")
        
        self.bank.semaphore.release()
        self.Queue[0].stop()
        del self.Queue[0]
        self.Register()
    
    def Deposit(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}: I'm waiting for Customer...")
        while len(self.Queue)==0 and self.bank.WorkingHour:
            pass
        if not self.bank.WorkingHour:
            self.clear()
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}: I’m outta here!")
            exit(0)
        customer_id = self.Queue[0].id
        task = self.Queue[0].task
        value = task['value']
        to = task['to']
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id}: it seems i have one")
        self.bank.semaphore.acquire()
        if value <= 0:
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}: Are you kiding me? negative value for deposit!!!")
        elif self.bank.balance.get(to):
            self.bank.balance[to] += value
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id}: Deposited Successfully {value}$ to account {to}  by customer {customer_id}")
        else:
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}: Invalid destination! deposit failed!")
        self.bank.semaphore.release()
        
        self.Queue[0].stop()
        del self.Queue[0]
        self.Deposit()
    
    def Withdraw(self):
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}: I'm waiting for Customer...")
        while len(self.Queue)==0 and self.bank.WorkingHour:
            pass
        if not self.bank.WorkingHour:
            self.clear()
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second}  "+Fore.LIGHTMAGENTA_EX+f" Employee {self.id}:I’m outta here!")
            exit(0)
        now = datetime.datetime.now()
        print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id}: it seems i have one")
        customer_id = self.Queue[0].id
        task = self.Queue[0].task
        value = task['value']
        self.bank.semaphore.acquire()
        if value <= 0:
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id} Are you  kiding me? negative value for witdraw!!!")
        elif value<=self.bank.balance[customer_id]:
            self.bank.balance[customer_id] -= value
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id} Withdraw Successfully {value}$ from account {customer_id}")
        else:
            now = datetime.datetime.now()
            print(Fore.LIGHTWHITE_EX+f"{now.hour}:{now.minute}:{now.second} "+Fore.LIGHTMAGENTA_EX+f"  Employee {self.id} balance issue! witdraw failed!")
        self.bank.semaphore.release()
        self.Queue[0].stop()
        del self.Queue[0]
        self.Withdraw()
    
    def clear(self):
        for customer in self.Queue:
            customer.alive=False

    def add(self,customer):
        self.Queue.append(customer)

class Boss(threading.Thread):

    def __init__(self,bank,time):
        threading.Thread.__init__(self)
        self.bank=bank
        self.time=time
    def End_of_working_hour(self):
        self.bank.WorkingHour=False
    def Start_of_working_hour(self):
        self.bank.WorkingHour=True
    def run(self):
        self.Start_of_working_hour()
        time.sleep(self.time)
        self.End_of_working_hour()

#-------------------------------bank 1-------------------------------------------------
bank1 = Bank({11111:100},1)
boss1 = Boss(bank1,5)
em1 = Employee(bank1,100,'register')
em2 = Employee(bank1,101,'deposit')
em3 = Employee(bank1,102,'withdraw')
bank1.load(em1,em2,em3,boss1)

cst1 = Customer(bank1,{'task':'withdraw','value':30},11111)
cst2 = Customer(bank1,{'task':'deposit','value': 20,'to':11111},22222)
cst3 = Customer(bank1,{'task':'register'},33333)

boss1.start()
bank1.start()
em1.start()
em2.start()
em3.start()
cst1.start()
cst2.start()
cst3.start()

#-------------------------------bank 2-------------------------------------------------
bank2 = Bank({2222:100},2)
boss2 = Boss(bank2,10)
em4 = Employee(bank2,104,'register')
em5 = Employee(bank2,105,'deposit')
em6 = Employee(bank2,106,'withdraw')
bank2.load(em4,em5,em6,boss2)

cst4 = Customer(bank2,{'task':'deposit','value': 120,'to':2222},44444)
cst5 = Customer(bank2,{'task':'deposit','value': 200,'to':2222},55555)
cst6 = Customer(bank2,{'task':'deposit','value': 220,'to':2222},66666)


boss2.start()
bank2.start()
em4.start()
em5.start()
em6.start()
cst4.start()
cst5.start()
cst6.start()
# #-------------------------------bank 3-------------------------------------------------
bank3 = Bank({333:100},3)
boss3 = Boss(bank3,15)
em7 = Employee(bank3,107,'register')
em8 = Employee(bank3,108,'deposit')
em9 = Employee(bank3,109,'withdraw')
bank3.load(em7,em8,em9,boss3)

cst7 = Customer(bank3,{'task':'deposit','value': -1020,'to':333},7777)
cst8 = Customer(bank3,{'task':'deposit','value': 2000,'to':333},8888)
cst9 = Customer(bank3,{'task':'deposit','value': 2020,'to':333},9999)


boss3.start()
bank3.start()
em7.start()
em8.start()
em9.start()
cst7.start()
cst8.start()
cst9.start()

# #-------------------------------bank 4-------------------------------------------------
bank4 = Bank({1000:100,1100:20,1200:5},4)
boss4 = Boss(bank4,15)
em10 = Employee(bank4,110,'register')
em11 = Employee(bank4,111,'deposit')
em12 = Employee(bank4,112,'withdraw')
bank4.load(em10,em11,em12,boss4)

cst10 = Customer(bank4,{'task':'withdraw','value': 10}, 1000)
cst11 = Customer(bank4,{'task':'withdraw','value': 20}, 1100)
cst12 = Customer(bank4,{'task':'withdraw','value': 100},1200)

boss4.start()
bank4.start()
em10.start()
em11.start()
em12.start()
cst10.start()
cst11.start()
cst12.start()

