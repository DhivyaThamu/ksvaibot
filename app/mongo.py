import pymongo
import json

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# mydb = myclient["bankdb"]#Create Database or open existing database
# mycol = mydb["customerData"]#Create collection or open collection

# custNum = "1234567890"
def connect ():
  try:
    myclient = pymongo.MongoClient("mongodb+srv://ksvuser01:ksvatlas123@cluster0.pmda5.mongodb.net/")
  except pymongo.errors.ConnectionFailure as e:
    return "Server Error"

  mydb = myclient["bankdb"]#Create Database or open existing database
  mycol = mydb["customerData"]#Create collection or open collection
  return mycol
  
def check_cust_status (custNum): 
  print (f"CustNum : {custNum}")
  try:
    myclient = pymongo.MongoClient("mongodb+srv://ksvuser01:ksvatlas123@cluster0.pmda5.mongodb.net/")
  except pymongo.errors.ConnectionFailure as e:
    return "Server Error"

  mydb = myclient["bankdb"]#Create Database or open existing database
  mycol = mydb["customerData"]#Create collection or open collection

  myquery = {"customerNumber" : custNum}
  print(f"My query: {myquery}")
  mydoc = mycol.find(myquery)
  print(f"mydoc is {mydoc}")
  if mydoc.count () == 0:
    return "Not Enrolled"
  return "Enrolled"
  # return "Invalid Customer Data"


def get_balance (custNum):
  try:
    myclient = pymongo.MongoClient("mongodb+srv://ksvuser01:ksvatlas123@cluster0.pmda5.mongodb.net/")
  except pymongo.errors.ConnectionFailure as e:
    return "Server Error"

  mydb = myclient["bankdb"]#Create Database or open existing database
  mycol = mydb["customerData"]#Create collection or open collection

  myquery = {"Customer Number" : custNum}
  mydoc = mycol.find(myquery)
  for x in mydoc:
    # if x is None:
    #   return "Invalid Customer Data"
    accountBalance = x['accountBalance']
    print (f"x:  {x} \n Bal : {accountBalance}")
    return accountBalance
    

def Update_enrollment_status (CustNum):
  myclient = pymongo.MongoClient("mongodb+srv://ksvuser01:ksvatlas123@cluster0.pmda5.mongodb.net/")
  mydb = myclient["bankdb"]#Create Database or open existing database
  mycol = mydb["customerData"]#Create collection or open collection
  mydict = { "SNo": "X", "customerName": "test", "customerNumber" : CustNum, "enrollmentStatus": "YES" }

  x = mycol.insert_one(mydict)
  return
# Result = getBiometricID ("9876543210")
# print(f"Result: {Result}")
    


