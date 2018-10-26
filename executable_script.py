import sys
import helpers
import json
import urllib
import urllib2


def requestMasto(url_ending='timelines/home', toot=None, visibility='direct'):

    host_instance = helpers._config('toots.host_instance')
    if not host_instance: return False

    token = helpers._config('toots.app_secure_token')
    if not token: return False

    headers = {}
    headers['Authorization'] = 'Bearer ' + token

    data = None
    if toot:
        url_ending = 'statuses'
        data = {}
        data['status'] = toot
        data['visibility'] = visibility

        data = urllib.urlencode(data)

    url = host_instance + '/api/v1/' + url_ending

  
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    text = response.read()
    if toot: text = 'Tooted "' + toot + '" to "' + host_instance + '".'
    with open('public/response_text.json', 'w') as fil:
      fil.write(text)
    return text



def tootTheTweet(toot):
    print 'toot is:' + toot
    if toot == 'null': toot = None
    requestMasto(toot=toot)

if __name__ == '__main__':
    tootTheTweet(sys.argv[1])
