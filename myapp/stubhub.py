import time
import requests
import json
from config import CONFIG

def api_call(call,params):
  """
  This makes the final api call and returns the JSON object/information 
  """

  # json_obj = login().json()
  # conn = json_obj
  # print conn['access_token']
  # base = 'https://api.stubhub.com'
  base = 'https://api.stubhubsandbox.com'
  # base = 'https://api.stubhub.com{0}{1}' % (call, param)

  headers = {
    'Accept-Encoding'  : 'application/json',
    'Authorization' : 'Bearer '+ CONFIG['stubhub']['application_token']
  }
  
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
        eventlist[event['id']] = event['title']
      return {'eventlist': eventlist}  
  # return {'error': 'test'}

def getTickets(eventid):
  resource = '/search/inventory/v1'
  params = '?eventid={number}&rows={rows}'.format(**{'number': eventid, 'rows': 1000000})
  
  result = api_call(resource,params)
  if result.get('error'):
    return result
  else:
    if result.get('listing'):
      return result['listing']
    else:
      return {'error': 'unknown error'}