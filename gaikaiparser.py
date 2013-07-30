#!/usr/bin/env python

"""
Parser for http://www.gaikai.com/careers.
Requires lxml module.

Usage:
>>> parse()
 [{'additional attributes': 'D3 or similar experience',
  'requirements': 'Minimum of 5+ years programming experience',
  'title': 'Data Visualization Architect'},
  ...]
"""

import sys
import urllib
from cStringIO import StringIO

from lxml import etree


URL = "http://www.gaikai.com/careers"


def wget(url):
    f = urllib.urlopen(url)
    return f.read()

def parse():
    ret = []
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(wget(URL)), parser)
    jobs = tree.xpath('//section[@class="openings accordion"]/descendant::article')
    for job in jobs:
        item = {}
        title = job.xpath('./h1/text()')[0]
        item['title'] = title
        desc_section = job.xpath('./section[@class="content"]/h2')
        for detail in desc_section:
            section_name = detail.xpath('./text()')[0].lower()
            # fix bad naming
            if 'skills' in section_name:
                section_name = 'skills'
            # ignore not standard items
            try:
                item[section_name] = detail.xpath('../child::ul/li/text()')
            except KeyError:
                print >> sys.stderr, "Key %s is not valid for job %s" \
                                     % (section_name, item['title'])
                continue
            ret.append(item)
    return ret

if __name__ == '__main__':
    from pprint import pprint as pp
    pp(parse())
