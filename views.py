from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

import urllib
import  json


import collections
class TransformedDict(collections.MutableMapping):
    """A dictionary which applies an arbitrary key-altering function before accessing the keys"""

    def id(self):
    	return id(self)

    def __init__(self, *args, **kwargs):
        self.store = dict()
        print args
        self.update(dict(*args, **kwargs)) # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key


class MyTransformedDict(TransformedDict):
  def __keytransform__(self, key):
    return key.replace("_",":")



def start(request):

	post = False
	items = []
	translations = []
	found = False
	words = []

	if request.method=='POST':
		post = True

		query = request.POST.get('query', None)
		url = "http://en.wikipedia.org/w/api.php?action=query&titles=%s&prop=langlinks&format=json&lllimit=500" % query
		data = json.load(urllib.urlopen(url))

		words = [query]
		try:
			langlinks = data['query']['pages'][data['query']['pages'].keys()[0]]['langlinks']
			for l in langlinks:
				translations.append("%s" % l.values()[0]) # - %s" % (l.values()[0], l.values()[1]) )
				word = l.values()[1].lower()
				if word not in words:
					words.append(word)
		except:
			pass	



		#print "WIKI: ", url
		#print "words: ", words
		#print "terans: ", translations

		# http://api.europeana.eu/api/opensearch.json?searchTerms=(sudetenland)+AND+(europeana_type:*IMAGE*)+AND+(europeana_rights:*by-sa*%20OR%20europeana_rights:*public*)&wskey=YOURKEY	
		eu_url = 'http://api.europeana.eu/api/opensearch.json?searchTerms=(%s)+AND+(europeana_type:*IMAGE*)+AND+(europeana_rights:*by-sa* OR europeana_rights:*public*)&wskey=YOURKEY' % ' OR '.join(words)
		eu_url = 'http://api.europeana.eu/api/opensearch.json?'

		eu_params = {
			'searchTerms': '(%s) AND (europeana_type:*IMAGE*) AND (europeana_rights:*by-sa* OR europeana_rights:*public*)' % ' OR '.join(words),
			'wskey': 'YOURKEY'
		}

		url = eu_url + urllib.urlencode(eu_params)
		print "Europeana URL: ", url
		data = json.load(urllib.urlopen(url))
		#print data
		try:
			items = [ MyTransformedDict(d) for d in data['items'] ]
			found = True
		except:
			items = []
			found = False

		
	return render_to_response("eutest.html", locals(), context_instance=RequestContext(request))


