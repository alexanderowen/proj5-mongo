"""
Nose tests for the memo utils

NOTE:
Assumes the db is empty
"""

import sys
from pymongo import MongoClient
import arrow
import CONFIG
from memo_utils import *

try: 
    dbclient = MongoClient(CONFIG.MONGO_URL)
    db = dbclient.memos
    collection = db.dated 
except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)
    
base = arrow.get(arrow.now().date())
		#Today,    Tomorrow,            Yesterday               next month
tests = [base, base.replace(days=+1), base.replace(days=-1), base.replace(months=+1)]
humanized = ["Today", "Tomorrow", "Yesterday", "in a month"]
ids = []

def test_memo_insert():
	"""
	Test memo insertion
	"""
	
	for test in tests:
		date = test.format('MM/DD/YYYY')
		memo = insert_memo("TEST MEMO", date, collection)
		id = memo.inserted_id
		ids.append(id)
		assert collection.find_one({'_id': id})
		
def test_humanized_date():
	"""
	Test for humanized function
	"""
	
	i = 0
	while i < len(tests):
		date = tests[i].isoformat()
		assert humanize_date(date) == humanized[i]
		i += 1
	
def test_near_midnight_humanized():
	"""
	Make sure that if it's 11:30, the next day is still tomorrow
	"""
	

def test_memo_delete():
	"""
	Test memo deletion
	Remove the memos inserted by test_memo_insert
	"""
	for id in ids:
		assert delete_memo(id, collection)
		
	#Make sure they have been removed
	for test in tests:
		date = test.format('MM/DD/YYYY')
		assert not collection.find_one({'date':date})
	
