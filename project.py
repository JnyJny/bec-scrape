'''
'''

from lxml import html
from collections import OrderedDict
import requests
import json

#Project name
#Category
#Address
#Size
#Construction Cost
#Description
#Owner
#Architect
#Architect Website
#Photo urls if possible

class Project(object):

    _projectKeys = [ 'project', 'url', 'category', 'address',
                     'size', 'cost', 'description', 'owner',
                     'architect', 'architectWebsite', 'images']
    
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return json.dumps(self.orderedDict, indent=2)

    @property
    def category(self):
        try:
            return self._category
        except AttributeError:
            pass
        self._category = self.url.split('/')[-2]
        return self._category

    @property
    def completed(self):
        try:
            return self._completed
        except AttributeError:
            pass
        self._completed = True if self.url.split('/')[-3] == 'completed' else False
        return self._completed

    @property
    def project(self):
        try:
            return self._project
        except AttributeError:
            pass
        self._project = self.tree.xpath('//h1')[0].text_content()
        return self._project

    @property
    def address(self):
        try:
            return self._address
        except AttributeError:
            pass
        try:
            self._address = self.listItems['address']
        except KeyError:
            self._address = 'NotAvailable'
        return self._address

    @property
    def size(self):
        try:
            return self._size
        except AttributeError:
            pass
        try:
            self._size = self.listItems['size']
        except KeyError:
            self._size = 'NotAvailable'
        return self._size

    @property
    def cost(self):
        try:
            return self._cost
        except AttributeError:
            pass
        try:
            self._cost = self.listItems['construction cost']
        except KeyError:
            self._cost = 'NotAvailable'
        return self._cost

    @property
    def description(self):
        try:
            return self._description
        except AttributeError:
            pass
        try:
            self._description = self.listItems['description']
        except KeyError:
            self._description = 'NotAvailable'
        return self._description

    @property
    def owner(self):
        try:
            return self._owner
        except AttributeError:
            pass
        try:
            self._owner = self.listItems['owner']
        except KeyError:
            self._owner = 'NotAvailable'
        return self._owner

    @property
    def architect(self):
        try:
            return self._architect
        except AttributeError:
            pass
        try:
            self._architect = self.listItems['architect']
        except KeyError:
            self._architect = 'NotAvailable'
        return self._architect

    @property
    def architectWebsite(self):
        try:
            return self._architectWebsite
        except AttributeError:
            pass
        try:
            self._architectWebsite = self.listItems['architect website']
        except KeyError:
            self._architectWebsite = 'NotAvailable'
        return self._architectWebsite

    @property
    def response(self):
        try:
            return self._response
        except AttributeError:
            pass
        self._response = requests.get(self.url)
        return self._response

    @property
    def tree(self):
        try:
            return self._tree
        except AttributeError:
            pass
        self._tree = html.fromstring(self.response.content)
        return self._tree
    
    @property
    def listItems(self):
        try:
            return self._listItems
        except AttributeError:
            pass

        self._listItems = {}

        for line in [li.text_content() for li in self.tree.xpath('//li')]:
            line = ' '.join(line.split()).strip() # de-dup spaces
            k,_,v = map(str.strip,line.partition(':'))
            if len(k):
                self._listItems.setdefault(k.lower(),v)
        return self._listItems

    @property
    def images(self):
        try:
            return self._images
        except AttributeError:
            pass
        self._images = [img.get('src') for img in self.tree.xpath('//img')]
        return self._images


    @property
    def orderedDict(self):
        try:
            return self._orderedDict
        except AttributeError:
            pass

        self._orderedDict = OrderedDict()

        for k in self._projectKeys:
            self._orderedDict[k] = getattr(self, k)
        return self._orderedDict
        
        
