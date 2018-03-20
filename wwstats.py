#!/usr/bin/python3
# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import requests
import urllib.request
import urllib.parse
import codecs
from achvlist import *

def check(id):
    url = "http://tgwerewolf.com/stats/PlayerAchievements/?pid=" + str(id)
    stats = {}
    #url = urllib.parse.quote(url)
#    r = requests.get(url)
#    soup = BeautifulSoup(r.content)
#    soup = str(r.content)
#    output = soup.prettify("utf-8")
#    output = soup.encode("utf-8")
#    output = UnicodeDammit(soup)
#    output = codecs.decode(soup, 'unicode_escape').encode('latin1').decode('utf8')
#    print(output)
    r = requests.get(url)

    dump = BeautifulSoup(r.json(), 'html.parser')
    db = dump('td')
    msgs = []
    num = 0
    for i in range(0, len(db), 2):
        stats[num] = db[i].string
        num = num + 1
	
    msgs.append(None)
    msgs[0] = "*دستاوردهایی که گرفتی ({0}/{1}):*\n".format(str(len(stats)), str(len(ACHV)))

    for x in stats:
        if stats[x] in [y['name'] for y in ACHV]:
            msgs[0] += "- `" + stats[x] + "`\n"
    msgs.append(None)
    msgs[1] = "\n*دستاوردهایی که نداریشون ({0}/{1}):*\n".format(str(len(ACHV)-len(stats)), str(len(ACHV)))
    msgs[1] += "*--> اینا رو میشه با بازی کردن به دست اورد:*\n"
    i = 1
    j = 1
    for z in ACHV:
        if z['name'] not in stats.values():
            if "inactive" in z or "not_via_playing" in z:
                continue
            msgs[i] += "- `" + z['name'] + "`\n"
            msgs[i] += ">>> _" + z['desc'] + "_\n"
            j += 1
            if j%15 == 0:
                i += 1
                msgs.append(None)
                msgs[i] = ""
    if msgs[i] != "":
        i += 1
        msgs.append(None)
    j = 1
    msgs[i] = "\n--> *اینا رو نمیشه مستقیما به دست اورد:*\n"
    for z in ACHV:
        if z['name'] not in stats.values():
            if "not_via_playing" in z:
                msgs[i] += "- `" + z['name'] + "`\n"
                msgs[i] += ">>> _" + z['desc'] + "_\n"
                j += 1
                if j%15 == 0:
                    i += 1
                    msgs.append(None)
                    msgs[i] = ""
            else:
                continue
    if msgs[i] != "":
        i += 1
        msgs.append(None)
    j = 1
    msgs[i] = "\n--> *این دستاوردا رو بیخیال فعلا غیرفعالن: *\n"
    for z in ACHV:
        if z['name'] not in stats.values():
            if "inactive" in z:
                msgs[i] += "- `" + z['name'] + "`\n"
                msgs[i] += ">>> _" + z['desc'] + "_\n"
                j += 1
                if j%15 == 0:
                    i += 1
                    msgs.append(None)
                    msgs[i] = ""
            else:
                continue

    return msgs
