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
prev_data = {"links": [], "current_page": "", "pages": []}
ex_st = False

args = decoded["args"]
if (args[1].isdigit() == False):
    arr1 = args[1:]
    arr2 = []
    arr2.append(args[0])
    arr2.append("0")
    arr2 += arr1
    args = arr2

# query = args[0]
pd = json.loads(decoded["prev_data"])

# [query, page]
if len(args) == 2:
    search_page = args[1]
    subscription_key = os.environ['MKEY']
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search?q=%-s&textDecorations=%-s&count=5&offset=%-s"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}

    num_current_page = int(search_page)
    with urllib.request.urlopen(urllib.request.Request(url = search_url % (args[0], "True", str(num_current_page * 5)), headers = headers)) as response:
        ret = json.loads(response.read())
        ret["webPages"]
        for idx, item in enumerate(ret["webPages"]["value"]):
            res.append(("[%-s] " % idx) + item['url'] + ":\n")
            res.append(item['snippet'] + "\n")
            res.append("page %-d shown" % (num_current_page))
            prev_data["links"].append(item['url'])
# [query, page, select, link_n] -> use prev_data[links]
# [query, page, select, link_n, page_n] -> use prev_data[pages]
# select = args[2]
# link_n = args[3]
# page_n = args[4]
elif len(args) > 2:
    links = pd["links"]
    link_n = args[3]
    url = links[int(link_n) - 1]

    parser = MyHTMLParser()

    with urllib.request.urlopen(url) as response:
        parser.feed(str(response.read()))

    page_n = "0"
    if len(args) == 5:
        page_n = args[4]
    pages = split_arrays(parser.res, 140)
    prev_data = {"links": links, "current_page": pages[int(page_n)], "pages": pages}
    res = pages[int(page_n)]
    res += "page %-d of %-d pages" % (int(page_n), len(pages))
    ex_st = False

prev_data = json.dumps(prev_data)
ret = json.dumps({"new_data": prev_data, "to_display": ''.join(res), "exit": ex_st})

print(ret)
