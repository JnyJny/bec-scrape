#!/usr/bin/env python3

import sys
from lxml import etree

try:
    input_file = sys.argv[1]
except IndexError:
    print("usage: {} input.xml [output.xml]\n".format(sys.argv[0].split('/')[-1]))
    exit(-1)

try:
    output_file = sys.argv[2]
except IndexError:
    output_file = '-'

buf = bytes(open(input_file).read(), 'utf-8')

tree = etree.fromstring(buf)

nsmap = tree.nsmap

thumbnail_path = './wp:postmeta/wp:meta_key[text()="_thumbnail_id"]'

items = tree.xpath('//item')
txt = {}
    
for item in items:
    content = item.xpath('./content:encoded', namespaces=nsmap)[0]

    idtxt = [x for x in content.text.split() if x.startswith('ids=')][0].split('=')[1]

    ids = [int(x) for x in  idtxt.replace('"','').split(',')]

    thumbnail = int(item.xpath(thumbnail_path, namespaces=nsmap)[0].getnext().text)

    if thumbnail in ids:
        continue

    ids.insert(0, thumbnail)
    newtext = '"{}"'.format(','.join([str(x) for x in ids]))
    txt.setdefault(idtxt, newtext)

if len(txt) == 0:
    print("nothing to fix")
    exit()
        
text = open(input_file).read()
        
for k,v in txt.items():
    text = text.replace(k, v, 1)

if output_file == '-':
    sys.stdout.write(text)
else:
    open(output_file,'w').write(text)

    
    
        
        

        

