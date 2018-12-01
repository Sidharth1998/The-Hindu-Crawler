#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 08:18:41 2018

@author: sidharthdugar
"""

""" 
Creating Database
"""

#importing libraries
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.schema import Sequence
from sqlalchemy import DateTime
import datetime

#Base declaration
Base = declarative_base()

#Creating Table
class News(Base):
    __tablename__ = 'news'
    # news table

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(150), nullable=False)
    article = Column(String(60), nullable=False)
    content = Column(String(1000), nullable=False)
    category = Column(String(30), nullable=False)
    date = Column(DateTime(), default=datetime.datetime.now().date())
    
    @property
    def serialize(self):
        return {
            'Id': self.id,
            'Link' : self.link,
            'Article Name': self.article,
            'Category' : self.category,
            'Content' : self.content,
            'Date' : self.date
        }
        
engine = create_engine('sqlite:///newsSummarizer.db')
Base.metadata.create_all(engine)