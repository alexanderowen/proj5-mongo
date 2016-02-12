'''
Utility functions for memos with MongoDB
'''

import arrow

# ObjectId for mongo records
from bson.objectid import ObjectId
	
def insert_memo(txt, date, collection):
	"""
	Creates memo in the collection
	Args:
		txt: string, memo text
		date: string, date of the form 'MM/DD/YYYY'
		collection: pymongo collection object, collection of a mongodb datebase
	Returns:
		InsertOneResult, documentation found here:
		https://api.mongodb.org/python/current/api/pymongo/results.html#pymongo.results.InsertOneResult
	"""
	arrow_date = arrow.get(date, "MM/DD/YYYY")
	
	record = { "type": "dated_memo", "date":  arrow_date.naive, "text": txt }			
	return collection.insert_one(record)


def delete_memo(id, collection):
	"""
	Deletes a memo from the collection
	Args: 
		id: bson.ObjectId, the id of the memo
		collection: pymongo collection object, collection of a mongodb database
	Returns:
		DeleteResult, documentation found here:
		https://api.mongodb.org/python/current/api/pymongo/results.html#pymongo.results.DeleteResult
	"""
	return collection.delete_one({'_id': id})

   
def humanize_date(date):
    """
    'Humanizes' a date using arrow
    Args:
    	date: string, internal UTC ISO format string.
    Returns:
    	human: string, of the format "today", "yesterday", etc.
    """
    try:
        then = arrow.get(date)
        now = arrow.utcnow().to('local')
        now = arrow.get(now.date())
        if then.date() == now.date():
            human = "Today"
        else: 
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
            elif human == "a day ago":
            	human = "Yesterday"
    except: 
        human = date
    return human