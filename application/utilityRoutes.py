#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 09:40:28 2020

@author: fleggio@tibco.com
"""
from flask import redirect, render_template, request, url_for, send_from_directory
from application import app, logWebApp, stripeListOfProductsAndPrices# ,mail, t
#from .models import User, validate_username, validate_password, check_password, check_profile
#from .token import generate_confirmation_token, confirm_token
#from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import  current_user, login_fresh, logout_user
#import datetime, 
#from .authenticationDecorator import authenticationClass
#from .authorizationDecorator import authorizationClass
import os#, uuid#from bson.json_util import dumps
from flask_mail import Message




#@t.include
@app.route('/currentUserInfo', methods=['GET'])
def currentUserInfo():
    #if login_fresh() == False:logout_user()
    if request.method == 'GET':
        #if current_user.is_authenticated == True:
        #    return render_template ('contactus.html', name=current_user.username, email=current_user.email)
        #else:
        currentUserData={}
        currentUserData['apikey']= '78ad517c-e4e6-57d3-89ae-76d4e429c629'
        currentUserData['counterDay']= 13
        currentUserData['counterMonth']= 1000
        currentUserData['limitPerDay']= 100
        currentUserData['limitPerMonth']= 1500
        
        return currentUserData

