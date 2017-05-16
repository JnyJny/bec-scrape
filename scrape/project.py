'''
'''

from lxml import html
from collections import OrderedDict
import requests
import json


class Project(object):
    '''
    Project records specific information from the source URL.

    Properties are found by building a HTML parse tree with the source
    URL and building a list of all the <li> nodes found on the page.
    We know that each <li> node is a key,value pair separated with a
    colon and lots of embedded white space.
    
    Project also records the <img> tags found in the source URL in the
    images property which is a list of src attributes for <img> nodes.

    The record property is an collections.OrderedDict that summarizes
    the contents of the Project object as determined by parsing the
    content of the source URL.
    '''

    _projectKeys = [ 'project', 'url', 'category', 'address',
                     'size', 'cost', 'description', 'owner',
                     'architect', 'architectWebsite', 'images']
    
    def __init__(self, url, missingDataMarker='NotAvailable'):
        '''
        :param: url is a valid URL string
        :param: missingdataMaker is an optional string 
        '''
        self.url = url
        self.missingDataMarker = missingDataMarker

    def __str__(self):
        return json.dumps(self.record, indent=2)

    @property
    def category(self):
        '''
        Project category string.
        '''
        try:
            return self._category
        except AttributeError:
            pass
        self._category = self.url.split('/')[-2]
        return self._category

    @property
    def completed(self):
        '''
        Boolean value, has the Project been completed?
        '''
        try:
            return self._completed
        except AttributeError:
            pass
        self._completed = self.url.split('/')[-3] == 'completed'
        return self._completed

    @property
    def project(self):
        '''
        Project name string.
        '''
        try:
            return self._project
        except AttributeError:
            pass
        self._project = self.tree.xpath('//h1')[0].text_content()
        return self._project

    @property
    def address(self):
        '''
        Project street address string.
        '''
        try:
            return self._address
        except AttributeError:
            pass
        self._address = self.listItems['address']
        return self._address

    @property
    def size(self):
        '''
        Project size string.
        '''
        try:
            return self._size
        except AttributeError:
            pass
        self._size = self.listItems['size']
        return self._size

    @property
    def cost(self):
        '''
        Project cost string.
        '''
        try:
            return self._cost
        except AttributeError:
            pass
        self._cost = self.listItems['construction cost']
        return self._cost

    @property
    def description(self):
        '''
        Project description string.
        '''
        try:
            return self._description
        except AttributeError:
            pass
        self._description = self.listItems['description']
        return self._description

    @property
    def owner(self):
        '''
        Project owner string.
        '''
        try:
            return self._owner
        except AttributeError:
            pass
        self._owner = self.listItems['owner']
        return self._owner

    @property
    def architect(self):
        '''
        Project architect string.
        '''
        try:
            return self._architect
        except AttributeError:
            pass
        self._architect = self.listItems['architect']
        return self._architect

    @property
    def architectWebsite(self):
        '''
        Project architect URL string.
        '''        
        try:
            return self._architectWebsite
        except AttributeError:
            pass
        self._architectWebsite = self.listItems['architect website']
        return self._architectWebsite

    @property
    def response(self):
        '''
        requests.Response object initialized with data from the source URL.
        '''
        try:
            return self._response
        except AttributeError:
            pass
        self._response = requests.get(self.url)
        return self._response

    @property
    def tree(self):
        '''
        HTML parse tree initialized with source URL data
        '''
        try:
            return self._tree
        except AttributeError:
            pass
        self._tree = html.fromstring(self.response.content)
        return self._tree
    
    @property
    def listItems(self):
        '''
        Dictionary of <li> content strings parsed into key,value pairs.
        '''
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
        '''
        List of src attributes of all the <img> nodes in the source URL data.
        '''
        try:
            return self._images
        except AttributeError:
            pass
        self._images = [img.get('src') for img in self.tree.xpath('//img')]
        return self._images

    @images.setter
    def images(self, newImages):
        '''
        '''
        self._images = newImages

    @property
    def record(self):
        '''
        An OrderedDict populated with all the Project's properties.
        The content and order of record is dictated by the contents
        of Project._projectKeys.  Keys with no data are given the
        value of Project.missingDataMarker.
        '''
        try:
            return self._record
        except AttributeError:
            pass

        self._record = OrderedDict.fromkeys(self._projectKeys,
                                            self.missingDataMarker)

        for k in self._projectKeys:
            try:
                self._record[k] = getattr(self, k)
            except KeyError:
                pass
            
        return self._record
        
        
