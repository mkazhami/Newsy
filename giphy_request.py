import requests
import json

def getGiphyURLFromKeywords(keywords):
    key = 'dc6zaTOxFJmzC'
    query = '+'.join(keywords)
    payload = {
        'api_key': key,
        'limit': 1,
        'q': query
        }
    resp = requests.get('http://api.giphy.com/v1/gifs/search', params=payload)
    return resp.json()['data'][0]['embed_url']
