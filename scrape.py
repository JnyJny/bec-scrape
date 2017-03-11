#!/usr/bin/env python3

from project import Project
from urls import urls
import json


def build_image_catalog(projects):
    '''
    '''
    catalog = {}
    for p in projects:
        for image in p.images:
            n = catalog.setdefault(image, 0)
            catalog[image] = n + 1

    return catalog

def deduplicate_project_images(projects, others=None):
    '''

    '''
    
    catalog = build_image_catalog(projects)

    duplicates = set([k for k,v in catalog.items() if v > 1])

    if others:
        duplicates.update(set(others))

    for p in projects:
        p.images = list(set(p.images).difference(duplicates))

if __name__ == '__main__':
    '''
    '''

    junk = ['../../images/head_latestnews.gif']
    
    projects = [Project(url) for url in urls]
    
    deduplicate_project_images(projects, junk)
    
    projectRecords = [p.record for p in projects]
    
    print(json.dumps(projectRecords, indent=2))
                     
