#!/usr/bin/env python3

import requests
from urls import urls

for url in urls:
    print('url: '+url)
    fname = url.split('/')[-1]
    with open('data/'+fname,'wb') as f:
        page = requests.get(url)
        f.write(bytes(url+'\n','utf-8'))
        f.write(page.content)
    

