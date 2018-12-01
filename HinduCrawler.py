#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 08:45:27 2018

@author: sidharthdugar
"""

"""
Creating crawler for The Hindu newspaper.
"""

#Importing Libraries
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, News
import re

#Connecting to database to store info
engine = create_engine('sqlite:///newsSummarizer.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Defining the categories
category = ["","tp-international/","tp-business/","tp-national/","tp-sports/"]

#Defining other variables
startUrl = "https://www.thehindu.com/todays-paper/"

def crawl(url):
    unvisitedLinks=[]
    lis=[]
    try:
        global data
        data = urllib.request.urlopen(url).read()
    except Exception as e:
        print("Error:"+str(e))
    soup = BeautifulSoup(data,"html.parser")
    ul = soup.find_all('ul', attrs={'class':"archive-list"})
    for li in ul:
        lis.extend(li.find_all('a'))
    for i in lis:
        unvisitedLinks.append(i.attrs["href"])
    return extract(unvisitedLinks)

def extract(links):
    linksDict={}
    for i in range(2):
        div=[]
        p=[]
        data = urllib.request.urlopen(links[i]).read()
        soup = BeautifulSoup(data,"html.parser")
        content=""
        ids=[]
        for tag in soup.find_all('div'):
            ids.append(tag.get('id'))
        for j in ids:
            if re.search("content-body-",str(j)):
                ID = j
        div = soup.find_all('div', attrs={'id':ID})
        for k in div:
            p.extend(k.find_all('p'))
        for l in p:
            try:
                content += l.string.strip()
            except:
                continue
        category=soup.find('a', attrs={'class':"section-name"}).string.strip("\n")
        article = soup.find('h1', attrs={'class':'title'}).string.strip("\n")
        linksDict[links[i]] = [article,content,category]
    return store(linksDict)

def store(dictionary):
    for keys, values in dictionary.items():
        storing = News(link=keys,article=dictionary[keys][0],content=dictionary[keys][1],
                       category=dictionary[keys][2])
        session.add(storing)
        session.commit()
   
def main():
    for i in category:
        url = startUrl+i
        crawl(url)
        
main()