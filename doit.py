#!/usr/bin/env python3

from project import Project
from urls import urls
import json

if __name__ == '__main__':
    data = [Project(url).orderedDict for url in urls]
    with open('bec.json','wb') as output:
        output.write(bytes(json.dumps(data, indent=2),'utf-8'))
                     
