import sys
import os
import json
import urllib.request
from html.parser import HTMLParser

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
                self.res += data
            elif tag in ["p", "b", "strong", "i", "em", "mark", "small", "del", "ins", "sub", "li", "a"]:
                self.res += data
            # elif tag in ["a"]:
                # self.res += ("[%-s]" % str(self.num_of_links)) + data
                # self.num_of_links += 1

decoded = json.loads(sys.argv[1])

def split_arrays(arr, num):
    if len(arr) > num:
        return ["".join(arr[:num])] + (split_arrays(arr[num:], num))
    else:
        return ["".join(arr)]

res = []
prev_data = []
if decoded["command"] == "search":
    if len(decoded["args"]) == 2:
        subscription_key = os.environ['MKEY']
        search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=%-s&textDecorations=%-s&count=5&offset=%-s"
        headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

        if len(decoded["args"]) == 1:
            decoded["args"].append("0")
        with urllib.request.urlopen(urllib.request.Request(url = search_url % (decoded["args"][0], "True", str(int(decoded["args"][1]) * 5 + 1)), headers = headers)) as response:
            ret = json.loads(response.read())
            ret["webPages"]
            for idx, item in enumerate(ret["webPages"]["value"]):
                res.append(("[%-s] " % idx) + item['url'] + ":\n")
                res.append(item['snippet'] + "\n")
                prev_data.append(item['url'])
    elif len(decoded["args"]) == 4:
        url = decoded["prev_data"][int(decoded["args"][3]) - 1]
        parser = MyHTMLParser()

        with urllib.request.urlopen(url) as response:
            parser.feed(str(response.read()))
        res = parser.res

ret = json.dumps({"new_data": prev_data, "to_display": ''.join(res)})

print(ret)
