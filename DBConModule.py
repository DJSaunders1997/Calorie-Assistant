# Custom module created by me to abstract away the details of talking to the database.
# Connects to a MongoDB Atlas cloud based database

from pymongo import MongoClient
from datetime import datetime

# Get password from local file not published to GitHub
f = open("password.txt", "r")
password = f.read()

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(f'mongodb+srv://user:{password}@cluster0.ad9pz.mongodb.net/test')
db=client.CaloriesDB


def get_daily_total(person):
	'''
	This function will return the total calories from all calories events with todays date for specified person.
	If the event doesn't exist then create it with 0 calories.

	TODO: do the aggregation on Mongos side when I figure out how it all works
	'''
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
	'''
	This function is used to add a new calorie event to the Connected MongoDB Database.
	A new item is added to the calorie_events array for the specified person.
	This item is a dict with a timestamp and the amount of calories to add.
	Note to take away calories this function is also used, but with a negative amount.
	Returns True if successful.
	'''

	current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # In format like '2021-04-22 11:26:55'
	new_calories_event = {'timestamp': current_time, 'calories': amount}

	# This query finds the record/document with the name "Dave" then uses the $push command to append a new calories item to the calories array
	# That item is a dict comprising of a timestamp and a number of calories
	res = db.People.update_one( {'name':person}, {'$push' : {'calorie_events': new_calories_event} } )

	return res.acknowledged

add_calories('Meg', 450)