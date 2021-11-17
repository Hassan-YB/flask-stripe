#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 07:17:22 2019

@author: fleggio@tibco.com
"""

from flask import render_template, request #, redirect, make_response, #, cache
from application import app, limiter#, mail, t #,client
#from .rateLimit import CountCalls, isProfileFree, isProfileBronze, isProfileSilver, isProfileGold
#from bson.json_util import dumps
from flask_login import current_user
from datetime import datetime
from flask_mail import Message

#@t.include
@app.errorhandler(404)
#@limiter.limit(app.config['RATE_LIMIT_PER_USER'], key_func = lambda : current_user.username)
def not_found_error(error):
    #print(type(error))
    #print(request.)
    emailMsg = Message("Error 404 occurred",
                       sender="admin@tepiloradata.com")
    emailMsg.add_recipient(app.config['MAIL_ADMIN'])
    #print (" current_user  ==>>>> ", current_user)
    try:
        emailMsg.body = "Current user: " + current_user.username + " generated a 404 error at " + str(datetime.now()) + " \r\n Requested url was " + request.url + " \r\n Requester IP: " + request.remote_addr
    except:
        emailMsg.body = "Unknown user:  generated a 404 error at " + str(datetime.now())  + " \r\n Requested url was " + request.url + " \r\n Requester IP: " + request.remote_addr
    try:
        print(emailMsg.body)
        #mail.send(emailMsg)    
    except:pass
    return render_template('404.html', title=''), 404
#@t.include
@app.errorhandler(500)
#@limiter.limit(app.config['RATE_LIMIT_PER_USER'], key_func = lambda : current_user.username)
def internal_error(error):
    #db.session.rollback()
    emailMsg = Message("Error 500 occurred",
                       sender="admin@tepiloradata.com")
    emailMsg.add_recipient(app.config['MAIL_ADMIN'])
    try:
        emailMsg.body = "Current user: " + current_user.username + " generated a 500 error at " + str(datetime.now())   + " \r\n Requested url was " + request.url + " \r\n Requester IP: " + request.remote_addr
    except:
        emailMsg.body = "Unknown user:  generated a 500 error at " + str(datetime.now())  + " \r\n Requested url was " + request.url + " \r\n Requester IP: " + request.remote_addr

    try:
        print(emailMsg.body)
        #mail.send(emailMsg)    
    except:pass
    return render_template('500.html', title=''), 500


#@app.errorhandler(302)
#def other_error(error):
#    db.session.rollback()
#    return render_template('302.html'), 302