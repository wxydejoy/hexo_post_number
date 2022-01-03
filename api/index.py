

import bs4
import requests
import re
from http.server import BaseHTTPRequestHandler
import json


def getLinks(url):
    url.replace('https', 'http')
    if url[-1] == "/":
        url = url[:-1]
    url = url + '/archives'


    links = []

    try:
        requests.DEFAULT_RETRIES = 5
        requests.keep_alive = False
        res = requests.get(url)
        if res.status_code != 200:
            return links
        # print(res.text)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        for link in soup.findAll('a', attrs={'href': re.compile("/")}):
            links.append(link.get('href'))
            # print(link)
    except requests.exceptions.ConnectionError:

        print('ConnectionError -- please connect wxy')
    except requests.exceptions.ChunkedEncodingError:
        print('ChunkedEncodingError -- please connect wxy')
    except:
        print('Unfortunitely -- An Unknow Error Happened, -- please connect wxy')

    return links


def getdata(url):



    list_links = []
    list_links += getLinks(url)
    for i in range(2,100):

        if getLinks(url + "/page/" + str(i) + "/") != []:
            list_links += getLinks(url + "/page/" + str(i) + "/")
        else:
            break
    news_ids = []
    for id in list_links:
        if id not in news_ids:
            news_ids.append(id)


    list_links = news_ids
    newss_ids = []
    ex = ["https","http",'/tags', '/categories', '/archives', '/friends','/shuoshuo', '/bangumi', '/movie', '/about', '/rss2.xml', '/atom.xml','/talk', '/page/','/search/', '/toys/','/fcircle/', '/link/', '/comments/', '/gallery/', '/random/','/null','/daodaoplus/','/music/', '/messageboard/', '/friendcircle/','/bber/',]
    for i in list_links:
        time = 0
        for j in ex:
            if j in i:
                time += 1
        if time == 0:
            newss_ids.append(i)

    return len(newss_ids)-1


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = getdata(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return


