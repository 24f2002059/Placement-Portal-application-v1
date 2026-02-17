from .model import *
from flask import current_app as app
from flask import Flask 

@app.route('/')
def home():
    return "database done !!!"