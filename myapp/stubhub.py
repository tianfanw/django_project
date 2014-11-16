import time
import requests
import json
from config import CONFIG
import logging
from models import Event, Ticket, SoldTicket

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
        e = Event.objects.filter(id=event['id'])
        logging.info(event)
        if not e:
          e = Event(id=event['id'])
          e.title = event.get('title')
          if event.get('venue'):
            e.venue = event['venue'].get('name')
          if event.get('groupings'):
            e.grouping = event['groupings'][0].get('name')
          if event.get('attributes'):
            e.primary_performer = event['attributes'][0].get('value')
            if len(event['attributes']) > 1:
              e.secondary_performer = event['attributes'][1].get('value')
          e.save()

        eventlist[event['id']] = event['title']
      return {'eventlist': eventlist}  
  # return {'error': 'test'}

def getTickets(eventId):
  resource = '/search/inventory/v1'
  params = '?eventId={number}&rows={rows}'.format(**{'number': eventId, 'rows': 1000000})
  
  result = api_call(resource,params)
  if result.get('error'):
    return result
  else:
    logging.info(result['totalListings'])
    logging.info(result['rows'])
    logging.info(result['totalTickets'])
    if result.get('listing'):
      e = Event.objects.get(id=eventId)
      tickets = e.ticket_set.all()
      ticketIds = tuple(t.id for t in tickets)
      listingIds = tuple(t['listingId'] for t in result['listing'])
      # soldTickets = e.soldticket_set.all()
      for ticket in tickets:
        if ticket.id not in listingIds:
          logging.info("found missing entry!")
          logging.info(ticket.id)
          Ticket.objects.filter(id=ticket.id).delete()
          t = SoldTicket(id=ticket.id, event=ticket.event, quantity=ticket.quantity,
                    zoneId=ticket.zoneId, zoneName=ticket.zoneName, sectionId=ticket.sectionId, sectionName=ticket.sectionName,
                    row=ticket.row, seatNumbers=ticket.seatNumbers, currentPrice=ticket.currentPrice)
          t.save()

      for ticket in result['listing']:
        if ticket['listingId'] not in ticketIds:
          t = Ticket(id=ticket['listingId'], event=e, quantity=ticket['quantity'],
                    zoneId=ticket['zoneId'], zoneName=ticket['zoneName'], sectionId=ticket['sectionId'], sectionName=ticket['sectionName'],
                    row=ticket['row'], seatNumbers=ticket['seatNumbers'], currentPrice=ticket['currentPrice']['amount'])
          t.save()
        # else:
        #   check if quantity changes
      # logging.info(result['listing'])
      return result['listing']
    else:
      return {'error': 'unknown error'}