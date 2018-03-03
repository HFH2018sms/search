import sys
import os
import json
import urllib.request
from html.parser import HTMLParser

# response.raise_for_status()
# search_results = response.json()
# print(search_results)

# decoded = json.loads(sys.argv[1])
# url
# if decoded["cmd"] == "search":
    # url = "https://%-s" % decoded["query"]
# elif decoded["cmd"] == "select":
    # url = decoded["links"][decoded["args"][0] - 1]

class MyHTMLParser(HTMLParser):
    res = ""
    num_of_links = 0
    tags = []
    links = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "a":
            for attr in attrs:
                if attr[0] == 'href':
                    self.links.append(attr[1])

    def handle_endtag(self, tag):
        self.tags.pop()

    def handle_data(self, data):
        data = ' '.join(data.split())
        if len(self.tags) > 0:
            tag = self.tags[-1]
            if tag in ["title","h1","h2","h3","h4","h5","h6","h7"]:
                self.res += data + "\n"
            elif tag in ["p", "b", "strong", "i", "em", "mark", "small", "del", "ins", "sub", "li"]:
                self.res += data
            elif tag in ["a"]:
                self.res += ("[%-s]" % str(self.num_of_links)) + data
                self.num_of_links += 1

    def get_res(self):
        return self.res

parser = MyHTMLParser()

# with urllib.request.urlopen('https://www.googleapis.com/customsearch/v1?key=%-s&q=hello' % gkey) as response:
    # parser.feed(str(response.read()))

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=%-s&textDecorations=%-s"
subscription_key = os.environ['MKEY']
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

with urllib.request.urlopen(urllib.request.Request(url = search_url % ("hello", "True"), headers = headers)) as response:
    res = json.loads(response.read())
    for item in res["webPages"]["value"]:
        print(item['url'])
        print(item['snippet'])

# print(parser.res)
# print(parser.links)
