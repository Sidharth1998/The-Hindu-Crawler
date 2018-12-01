#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 20:45:32 2018

@author: sidharthdugar
"""

""" Main project file where webiste will be routed,
data will be fetched."""

#Importing Libraries
from flask import Flask, render_template, request, redirect, jsonify
from flask import url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, News
import random
import string
import httplib2
import json
from flask import make_response
import requests
import datetime

#Flask object
app = Flask(__name__)

#Connecting to database and creating database session
engine = create_engine('sqlite:///newsSummarizer.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/news/JSON')
def newsJson():
    data = session.query(News).all()
    return jsonify(data=[i.serialize for i in data])

@app.route('/', methods=["GET","POST"])
@app.route('/news', methods=["GET","POST"])
def showNews():
    news = session.query(News).all()
    query = session.query(News.date.distinct().label("date")).all()
    dates = [row.date for row in query]
    date = dates[-1]
    queryCategory = session.query(News.category.distinct().label("category")).all()
    return render_template("index.html", news=news,date=date,categories=queryCategory)

@app.route('/news/<string:category1>/')
def showCatNews(category1):
    query = session.query(News).filter_by(category=category1).all()
    queryCategory = session.query(News.category.distinct().label("category")).all()
    return render_template("category.html",categories=query,category=queryCategory)

#Running the website
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=8000)