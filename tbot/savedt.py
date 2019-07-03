import warnings
warnings.filterwarnings("ignore")

from bs4 import BeautifulSoup
import re
import urllib3
import datetime
from models import Calendar

for k in range(200):
    dd = datetime.datetime.today() + datetime.timedelta(days=k)

    datas = str(dd.year) + '-' + str(dd.month) + '-' + str(dd.day)

    # get the contents
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://postypashki.ru/ecwd_calendar/calendar/?date={}&t=full'.format(datas))
    d = r.data

    parsed_html = BeautifulSoup(d)

    p = parsed_html.body.find('td', attrs={'data-date': datas})
    p2 = p.find_all('a')

    texts = []
    urls = []
    for i in range(0, len(p2), 2):
        texts.append(str(p2[i].text))
        match = re.search(r'http://.*/"', str(p2[i]))
        urls.append(match.group())
        # print( p2[i].text)

    for i in range(0, len(texts)):
        event = Calendar(name=texts[i],url=urls[i] ,date=dd,typeles=0)
        event.save()
        print('|' + texts[i] + '|' + urls[i])
    print(dd)