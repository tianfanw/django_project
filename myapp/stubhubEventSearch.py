
#upARnU34eyNp4axvFHn5AsmSn5ca
#MrAWjIzDkf1EEZhtLDojeUfmf6Ia
#E7DF153021286899D6
import csv
import json
import requests
import time
#import sys

"""
LISTING_HEADER is used to populate the first row of the comma 
seperated values sheet. Be sure to edit this if changing anything
"""

LISTING_HEADER = ['deliveryFee',
					'seatNumbers',
					# 'currentPrice',
					'amount',
					'deliveryTypeList',
					'totalCost',
					'listingId',
					'serviceFee',
					'splitVector',
					'zoneId',
					'row',
					'sectionId',
					'listingAttributeList',
					'sellerOwnInd',
					'ticketClass',
					'splitOption',
					'listingAttributeCategoryList',
					'zoneName',
					'sectionName',
					'dirtyTicketInd',
					'faceValue',
					'sellerSectionName',
					'quantity',
					]

def login():
	"""
	This is the login method that connects to stubhub's API
	Uses the username and password, as well as authorization token as retrieved
	from the Stubhub developers page
	"""

	url = 'https://api.stubhub.com/login'

	headers = {
		'Content-Type'  : 'application/x-www-form-urlencoded',
		'Authorization' : 'Basic dXBBUm5VMzRleU5wNGF4dkZIbjVBc21TbjVjYTpNckFXakl6RGtmMUVFWmh0TERvamVVZm1mNklh'
	}

	request_body = {
		'grant_type' : 'password',
		'username' : '******',
		'password' : '*****',
		'scope' : 'PRODUCTION'
	}
	
	req =requests.post(url, params=request_body, headers=headers)
	
	return req

def get_userID():
	"""
	This method retrieves the users login information
	"""

	info = login()
	user_guid = info.headers['x-stubhub-user-guid']
	#user_id = user_guid[0:7] + user_guid[-11:]
	return user_guid

def api_call(call,params):
	"""
	This makes the final api call and returns the JSON object/information 
	"""

	json_obj = login().json()
	conn = json_obj
	print conn['access_token']
	base = 'https://api.stubhub.com'
	# base = 'https://api.stubhub.com{0}{1}' % (call, param)

	headers = {
		'Accept-Encoding'  : 'application/json',
		'Authorization' : 'Bearer '+ conn['access_token']
	}
	
	req = requests.get(base+call+params, headers=headers)
	
	return req.json()

def myprint(d):
	"""
	myprint takes a dictionary (or json) object as it's argument
	was simply exploratory and isn't used right now.
	run it to see what happens
	"""

	for k, v in d.iteritems():
		if isinstance(v,dict):
			myprint(v)
		else:
			print "{0} : {1}".format(k,v)


def updatefile(tix_dict):
	"""
	updatefile method was first attempt to write rows into the csv file
	takes a dictionary/json object as its argument
	writes the key value pair in a row
	"""

	#http://stackoverflow.com/questions/4893689/save-a-dictionary-to-a-file-alternative-to-pickle-in-python
	w = csv.writer(open("postings.csv", "w"))
	for key, val in tix_dict.items():
		w.writerow([key,val])

def jsondump(json_results):
	"""
	jsondump takes a dictionary/json object
	not used
	"""

	json.dumps(json_results)
	

def testcalls():
	"""
	testcalls is where the action is to understand what is going on 
	resource and params are the particular URL endpoint you are interested
	in looking at. 

	testcalls then calls the api_call method and stores it in the variable named result

	the rest is playing around with printing 
	"""

	resource = '/search/inventory/v1'
	params = '?eventid=4378924' #str(get_userID())
	
	result = api_call(resource,params)
	#updatefile(result)
	#jsondump(result)

	for k in result.keys():
		print str(k) + ' : ' + str(result[k])
	
	print "below are lisings"
	print result['listing']

	for i in range(1, len(result['listing'])):
		print "This is listing " + str(i)
		print result['listing'][i]

def listingtorow(listingDict):
	"""
	converts listing json dictionary to comma seperated row
	"""

	oneRow = [listingDict['deliveryFee'],
				listingDict['seatNumbers'],
				listingDict['currentPrice']['amount'],
				listingDict['deliveryTypeList'],
				listingDict['totalCost'],
				listingDict['listingId'],
				listingDict['serviceFee'],
				str(listingDict['splitVector']),
				listingDict['zoneId'],
				listingDict['row'],
				listingDict['sectionId'],
				listingDict['listingAttributeList'],
				listingDict['sellerOwnInd'],
				listingDict['ticketClass'],
				listingDict['splitOption'],
				listingDict['listingAttributeCategoryList'],
				listingDict['zoneName'],
				listingDict['sectionName'],
				listingDict['dirtyTicketInd'],
				listingDict['faceValue'],
				listingDict['sellerSectionName'],
				listingDict['quantity']
			]
	return oneRow

def WriteEventInformation(eventid, csvwriter):
	"""
	as opposed to testcalls, this is actually where all the work is being done right now
	allows eventid to be passed in and the name of file 

	checks to see if file exists
	writes the LISTING_HEADER on the first row 
	then fills in with listings 

	eventid must be an UPCOMING event. 
	"""

	eventid = chooseEvent() #overwriting the input for now
	resource = '/search/inventory/v1'
	params = '?eventid={number}&rows={rows}'.format(**{'number': eventid, 'rows': 1000000})
	
	result = api_call(resource,params)

	print "Success"

	if csvwriter is None:
		csvwriter = open(str(eventid)+'_inventory.csv', 'wb')
		writer = csv.writer(csvwriter)
		writer.writerow(LISTING_HEADER)

	for listing in result['listing']:
		# csvwriter.writerow(['a','b'])
		print listingtorow(listing)
		csvwriter.writerow(listingtorow(listing))

def getEventID(grouping, city, team, venue, year, month, day):
	"""
	getEventID allows user to search for an event and retrieve the eventId for use
	in the other functions

	grouping is organizations and descriptors that can be associated, i.e. MLB,
	Pre-Season, etc
	city is the city location
	team is the performer

	TO DO: implement a date range search, and allow a user to pick one of the events
	try/except some for no results found.
	"""
	#yyyy-mm-ddThh:mm
	currentDate = (time.strftime("%Y-%m-%d"))
	dateRange = str(year)+'-'+str(month)+'-'+str(day)
	date= currentDate+'T00:00TO'+dateRange+'T00:00' 
	resource = '/search/catalog/events/v2'
	params = '?groupingName{grouping}&city={city}&performerName={performer}&rows={rows}&venue={venue}&date={date}'.format(**{'grouping': grouping, 'city': "city", 'performer':team, 'rows': 1000, 'venue':venue, 'date': date })
	#note that 'city':"city" has an extra set of quotes because stubhub accepts quotes to search for specifics
	#seems to change rusults

	result = api_call(resource, params)
	print result

	eventlist = {}

	for event in result['events']:
		#print event['id'], event['title']
		eventlist[event['id']] = event['title']

	#print eventlist
	#print result['events'][1]['id']
		

	#for event in result['events']:
	#	print event['venue']

	return eventlist

def chooseEvent():
	"""
	chooseEvent() calls getEventId to create a list for the user to select an UPCOMING event from
	note that Sublime does not allow user input without SublimeREPL so the first bit has been 
	commented out
	""" 

	"""grouping = raw_input("Please enter grouping: ")
	city = raw_input("Please enter a city: ")
	venue = raw_input("Please enter a venue: ")
	print "Next enter a date to search until..."
	year = raw_input("Please enter a year: ")
	month = raw_input("Please enter a month: ")
	day = raw_input("Please enter a day: ")
	"""	
	eventlist = getEventID('NFL', 'New York', 'Giants', 'Metlife Stadium', 2014, 12, 10)


	print "Please pick from one of the following events"

	count = 1
	for key,value in eventlist.iteritems():
		print str(count) + ": " + value
		count+=1
	
	#Apparently Sublime doesn't allow raw_input...
	#selection = raw_input("Please type the corresponding number: ") 
	selection = 2
	select_key = eventlist.keys()[selection]

	return select_key 


#testcalls()

csvwriter = open('tmp.csv', 'wb')
writer = csv.writer(csvwriter)
writer.writerow(LISTING_HEADER)
WriteEventInformation(4378924, writer) #NOTE this event needs to be upcoming unless you will get an error!

#just noticed a possible error here, it seems that I tried to make a file name eventId_inventory.csv but infact only writes to tmp.csv 
#getEventID('NFL', 'New York', 'Giants', 'Metlife Stadium', 2014, 12, 10)


