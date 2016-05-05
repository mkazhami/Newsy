import requests
import json
from secret import giphy_key

def getGiphyURLFromKeywords(keywords):
	if len(keywords) == 0:
		return ""
	query = '+'.join(keywords)
	payload = {
		'api_key': giphy_key,
		'limit': 1,
		'q': query
	}
	resp = requests.get('http://api.giphy.com/v1/gifs/search', params=payload)
	return resp.json()['data'][0]['embed_url']
