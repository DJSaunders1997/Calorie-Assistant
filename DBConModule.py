from pymongo import MongoClient
from datetime import datetime

# Get password from local file not published to GitHub
f = open("password.txt", "r")
password = f.read()

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(f'mongodb+srv://user:{password}@cluster0.ad9pz.mongodb.net/test')
db=client.CaloriesDB


def get_daily_total(person):
    # TODO do the aggregation on Mongos side when I figure out how it all works
    # Will query the MongoDB for the specified person and return 0 if no calories have been added, or return the current total

    today = datetime.today().strftime("%Y-%m-%d")

    # Query to return all info for person we want and with calories for today 
    # We could just query on name but wanted to add the other condition for completeness sake
    doc = db.People.find_one( {"$and": [{"calorie_events.timestamp": {"$regex": today} }, {"name": person} ]} )

    events = doc['calorie_events']
    # If nothing is returned then there is no data logged today
    if doc is None:
        return 0
    else:
        # Go through all timestamps with todays date and sum calories    
        total = 0

        for event in events:
            if today in event['timestamp']:
                total = total + event['calories']

        return total


def add_calories(person, amount):
    # Adds a new calorie event to the specified person with the current timestamp and specified amount of calories  
    # Returns true if successful

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # In format like '2021-04-22 11:26:55'
    new_calories_event = {'timestamp': current_time, 'calories': amount}

    # This query finds the record/document with the name "Dave" then uses the $push command to append a new calories item to the calories array
    # That item is a dict comprising of a timestamp and a number of calories
    res = db.People.update_one( {'name':person}, {'$push' : {'calorie_events': new_calories_event} } )

    return res.acknowledged

add_calories('Meg', 450)