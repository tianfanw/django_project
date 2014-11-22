import time
import requests
import json
from config import CONFIG
import logging
from models import Event, Listing, SoldTicket
import os

def api_call(call,params):
  """
  This makes the final api call and returns the JSON object/information 
  """

  # json_obj = login().json()
  # conn = json_obj
  # print conn['access_token']
  base = 'https://api.stubhub.com'
  access_token = CONFIG['production']['application_token']
  # base = 'https://api.stubhubsandbox.com'
  # access_token = CONFIG['sandbox']['application_token']
  # base = 'https://api.stubhub.com{0}{1}' % (call, param)
  
  headers = {
    'Accept-Encoding'  : 'application/json',
    'Authorization' : 'Bearer '+ access_token
  }
  logging.info(base+call+params)
  req = requests.get(base+call+params, headers=headers, verify=False)
  if req.status_code == 200:
    return req.json()
  else:
    return {'error': req.status_code}

def storeEvent(event):
  # logging.info(event)
  e = Event(id=event['id'])
  e.title = event.get('title')
  if event.get('venue'):
    e.venue = event['venue'].get('name')
  if event.get('groupings'):
    e.grouping = event['groupings'][0].get('name')
  if event.get('attributes'):
    e.primaryPerformer = event['attributes'][0].get('value')
    if len(event['attributes']) > 1:
      e.secondaryPerformer = event['attributes'][1].get('value')
  e.save()
  return e

def getEvents(query):
  resource = '/search/catalog/events/v2'
  params = '?'
  for key, value in query.iteritems():
    if(key == 'date'):
      currentDate = (time.strftime("%Y-%m-%d"))
      params = params + 'date=' + currentDate+'T00:00TO'+value+'T00:00' + '&'
    else:
      params = params + key + '=' + value + '&'

  params = params + 'rows=1000'
  result = api_call(resource, params)
  if result.get('error'):
    return result
  else:
    if result['numFound'] == 0:
      return {'error': 'No records found.'}
    else:
      eventlist = {}
      for event in result['events']:
        try:
          Event.objects.get(id=event['id'])
        except Event.DoesNotExist:
          storeEvent(event)
        eventlist[event['id']] = event['title']
      return {'eventlist': eventlist}  
  # return {'error': 'test'}

def getEvent(eventId):
  logging.info(eventId)
  resource = '/search/catalog/events/v2'
  params = '?id={number}'.format(**{'number': eventId})
  result = api_call(resource, params)
  if result.get('error'):
    return result
  else:
    if result['numFound'] == 0:
      return {'error': 'No records found.'}
    else:
      event = result['events'][0]
      return event

def updateDBTickets(eventId, listings):
  try:
    e = Event.objects.get(id=eventId)
  except Event.DoesNotExist:
    # User queried an event not in the database, probably search by modifying url
    logging.info('event ' + str(eventId) + ' not in db yet')
    if int(eventId) == 1: # for testing only
      e = Event(id=1)
      e.save()
    else:
      event = getEvent(eventId)
      logging.info(event)
      if not event.get('error'):
        e = storeEvent(event)
      else:
        return {'error': 'event does not exist'}

  oldListings = dict((l.id,l) for l in e.listing_set.all())
  newListings = dict((l['listingId'], l) for l in listings)

  for lid in oldListings:
    oldListing = oldListings[lid]
    if lid not in newListings.keys():
      # if the listing in database is not in the latest listings, then it is sold
      logging.info("All tickets in the listing " + str(lid) + " have been sold out!")
      if(oldListing.quantity > 0):
        # insert all tickets into SoldTicket
        seats = [seat.strip() for seat in oldListing.seatNumbers.split(',')]
        for seat in seats:
          t = SoldTicket(listingId=lid, event=e, zoneId=oldListing.zoneId, zoneName=oldListing.zoneName, 
            sectionId=oldListing.sectionId, sectionName=oldListing.sectionName, row=oldListing.row,
            seatNumber=seat, currentPrice=oldListing.currentPrice)
          t.save()
        remaining = oldListing.quantity - len(seats)
        if remaining > 0: # mainly caused by seatNumbers == "General Admission"
          for i in xrange(0, remaining):
            t = SoldTicket(listingId=lid, event=e, zoneId=oldListing.zoneId, zoneName=oldListing.zoneName, 
            sectionId=oldListing.sectionId, sectionName=oldListing.sectionName, row=oldListing.row,
            seatNumber=None, currentPrice=oldListing.currentPrice)
            t.save()

      # Delete the empty listing
      Listing.objects.filter(id=lid).delete()
    else:
      # the listing is still active, then check its quantity
      curListing = newListings[lid]
      if curListing['quantity'] < oldListing.quantity:
        # Some tickets are sold but not all of them
        # find out which seats were sold, update listing and insert into sold tickets
        oldSeats = [seat.strip() for seat in oldListing.seatNumbers.split(',')]
        newSeats = [seat.strip() for seat in curListing['seatNumbers'].split(',')]
        missingSeats = [seat for seat in oldSeats if seat not in newSeats]
        for seat in missingSeats:
          t = SoldTicket(listingId=lid, event=e, zoneId=oldListing.zoneId, zoneName=oldListing.zoneName, 
            sectionId=oldListing.sectionId, sectionName=oldListing.sectionName, row=oldListing.row,
            seatNumber=seat, currentPrice=oldListing.currentPrice)
          t.save()
        remaining = oldListing.quantity - curListing['quantity'] - len(missingSeats)
        if remaining > 0: # mainly caused by seatNumbers == "General Admission"
          for i in xrange(0, remaining):
            t = SoldTicket(listingId=lid, event=e, zoneId=oldListing.zoneId, zoneName=oldListing.zoneName, 
            sectionId=oldListing.sectionId, sectionName=oldListing.sectionName, row=oldListing.row,
            seatNumber=None, currentPrice=oldListing.currentPrice)
            t.save()

        oldListing.seatNumbers = curListing['seatNumbers']
        oldListing.quantity = curListing['quantity']
        oldListing.save()

  for lid in newListings:
    if lid not in oldListings.keys():
      # Someone has posted a new listing that is not in the database, put it into database
      newListing = newListings[lid]
      l = Listing(id=newListing['listingId'], event=e, quantity=newListing['quantity'],
                zoneId=newListing['zoneId'], zoneName=newListing['zoneName'], sectionId=newListing['sectionId'], 
                sectionName=newListing['sectionName'], row=newListing['row'], seatNumbers=newListing['seatNumbers'],
                currentPrice=newListing['currentPrice']['amount'])
      l.save()

def getTickets(eventId):
  if int(eventId) == 1: # for testing only
    logging.info("testing!")
    f = open('myapp/testdata.json')
    data = json.load(f)
    f.close()
    result = {'listing': data}
  else:
    resource = '/search/inventory/v1'
    params = '?eventId={number}&rows={rows}'.format(**{'number': eventId, 'rows': 1000000})
    
    start = time.time()
    result = api_call(resource,params)
    print "Elapsed time for calling api: %s" % (time.time()-start)
  if result.get('error'):
    return result
  else:
    # logging.info(result['totalListings'])
    # logging.info(result['rows'])
    # logging.info(result['totalTickets'])
    # f = open('myapp/testdata.json', 'w')
    # json.dump(result['listing'][0:4], f, indent=4)
    # f.close()
    if result.get('listing'):
      start = time.time()
      updateDBTickets(eventId, result['listing'])
      print "Elapsed time for db writing: %s" % (time.time()-start)
      return result['listing']
    else:
      return {'error': 'unknown error'}