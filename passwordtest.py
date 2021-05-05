from pymongo import MongoClient
from datetime import datetime
import os

# Get password from local file not published to GitHub
#os.environ["MONGO_PW"] = #"enter_password_here" # How to set enviroment variables in python
password = os.environ.get('MONGO_PW')
print(password)
# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(f'mongodb+srv://user:{password}@cluster0.ad9pz.mongodb.net/test')
db=client.CaloriesDB

doc = db.People.find_one( )