##
# This Python script is to collect the RSS feed and send the data to firebase
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from firebase import firebase
import urllib.request as urllib2
import json
import uuid
import sys
import datetime
import requests
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
cred = credentials.Certificate("./AccountKey.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()
main_category = sys.argv[2]
today = str(datetime.date.today())
replace_url = sys.argv[1].replace(":", "%3A").replace("/", "%2F").replace("&", "%26").replace("?", "%3F").replace("=", "%3D")
url = 'https://api.rss2json.com/v1/api.json?rss_url=' + replace_url + '&api_key=XXXXXXXXXXXXXXXX&order_by=pubDate&count=30'
response = urllib2.urlopen(url)
data = json.loads(response.read());
if data['status'] == 'ok':
    for item in data['items']:
        newurl = item['link']
        try:
            html = urlopen(newurl)
            bs = BeautifulSoup(html, 'html.parser')
            images = bs.find_all('img', {'src':re.compile('.jpg')})
            for image in images:
                newimages = image['src']
                break
            date = str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
            title = item['title'].replace("$", "dollar")
            filename = title[0:40]
            item["uuid"] = str(uuid.uuid4())
            item.update( {'addedDate' : date} )
            if 'category' in item:
                del item['category']
            if 'categories' in item:
                del item['categories']
            item.update( {'category' : main_category} )
            if 'description' not in item:
                item.update( {'description' : ''} )
            if 'pubDate' in item:
                item['origin_date'] = item.pop('pubDate')
            if 'thumbnail' in item:
                del item['thumbnail']
            if 'enclosure' in item:
                del item['enclosure']
            item.update( {'image' : newimages} )
            item.update( {'reportCount' : 0} )
            batch = store.batch()
            doc_ref = store.collection('feed').document(filename)
            batch.set(doc_ref, item)
            batch.commit()
        except requests.exceptions.ConnectionError:
            print (newurl + " " + 'url not found')