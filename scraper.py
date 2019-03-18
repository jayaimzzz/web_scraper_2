#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a url, scrap the page for links, email addresses, and phone numbers
"""

__author__ = "jayaimzzz"

import re
import argparse
import requests
import urllib2 
from bs4 import BeautifulSoup

links_set = set([])

def scrap(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        return soup
    except:
        print "error scrapping {}".format(url)
    

def print_links(soup):
    links = soup.find_all('a')
    url_regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    links = [str(link.get('href')) for link in links if re.search(url_regex, str(link))]
    print "URLs"
    for link in links:
        print link
    links = soup.find_all('img')
    for link in links:
        print link.get('src')
        

def print_email_addresses(soup):
    links = soup.find_all('a')
    email_regrex = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    links = set([str(link.get('href')) for link in links if re.search(email_regrex, str(link))])
    print "Email addresses"
    for link in links:
        print link.replace("mailto:","")
        
def print_phone_numbers(soup):
    pattern = re.compile(r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?')
    matches = pattern.findall(str(soup))
    phone_numbers = set()
    for match in matches:
        if match not in phone_numbers:
            phone_numbers.add("{}-{}-{}".format(match[0],match[1],match[2]))
    print "Phone numbers"
    for phone_number in phone_numbers:
        print phone_number

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The url to scrap")
    return parser

def main(url):
    soup = scrap(url)
    if soup:
        # print_links(soup)
        print_email_addresses(soup)
        # print_phone_numbers(soup)

if __name__ == "__main__":
    parser = create_parser()
    url = parser.parse_args().url
    main(url)

    # print_email_addresses(soup)
    
