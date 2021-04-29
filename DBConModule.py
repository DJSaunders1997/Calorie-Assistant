from pymongo import MongoClient
import datetime
import os

# Get password from local enviroment variable not published to GitHub
#os.environ["MONGO_PW"] = #"enter_password_here" # Reminder of how to set enviroment variables in Python
password = os.environ.get('MONGO_PW')

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(f'mongodb+srv://user:{password}@cluster0.ad9pz.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db=client.CaloriesDB


def get_daily_total(person, date):
	'''
	This function will return the total calories from all calories events with todays date for specified person.
	If the event doesn't exist then create it with 0 calories.
	TODO: do the aggregation on Mongos side when I figure out how it all works
	'''
		
	datestr = date.strftime("%Y-%m-%d")

	# Query to return all info for person we want and with calories for today 
	# We could just query on name but wanted to add the other condition for completeness sake
	doc = db.People.find_one( {"$and": [{"calorie_events.timestamp": {"$regex": datestr} }, {"name": person} ]} )

	# If nothing is returned then there is no data logged today
	if doc is None:
		return 0
	else:
		# Go through all timestamps with todays date and sum calories    
		total = 0

		for event in doc['calorie_events']:
			if datestr in event['timestamp']:
				total = total + event['calories']

		return total


def add_calories(person, date, amount):
	'''
	This function is used to add a new calorie event to the Connected MongoDB Database.
	A new item is added to the calorie_events array for the specified person.
	This item is a dict with a timestamp and the amount of calories to add.
	Note to take away calories this function is also used, but with a negative amount.
	Returns True if successful.
	'''

	current_time = datetime.datetime.now() 
	current_timestr = current_time.strftime("%Y-%m-%d %H:%M:%S")# In format like '2021-04-22 11:26:55'

	datestr = datetime.datetime.strftime(date, "%Y-%m-%d")# In format like '2021-04-22'

	if date.date() == current_time.date():
		# If event is being added for today then add with all exact time info
		new_calories_event = {'timestamp': current_timestr, 'calories': int(amount)} # Double check amount is int before pushing

	else:
		# If event is being added for previous / future date then do not add exact time info
		new_calories_event = {'timestamp': datestr, 'calories': int(amount)} # Double check amount is int before pushing

	# This query finds the record/document with the name "Dave" then uses the $push command to append a new calories item to the calories array
	# That item is a dict comprising of a timestamp and a number of calories
	res = db.People.update_one( {'name':person}, {'$push' : {'calorie_events': new_calories_event} } )

	return res.acknowledged