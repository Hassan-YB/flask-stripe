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


@app.route('/favicon.ico') 
def favicon():
    #print ("path for favicon ====>>>> " ,os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/apple-touch-icon.png') 
def appletouchicon():
    #print ("path for favicon ====>>>> " ,os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'apple-touch-icon.png', mimetype='image/png')

@app.route('/apple-touch-icon-precomposed.png') 
def appletouchiconprecomposed():
    #print ("path for favicon ====>>>> " ,os.path.join(app.root_path, 'static'))
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'apple-touch-icon-precomposed.png', mimetype='image/png')


#@t.include
@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    #if login_fresh() == False:logout_user()
    if request.method == 'GET':
        #if current_user.is_authenticated == True:
        #    return render_template ('contactus.html', name=current_user.username, email=current_user.email)
        #else:
            return render_template ('contactus.html', name='')
    if request.method == 'POST':
        logWebApp.debug("entered post")
        logWebApp.debug(request.form.to_dict())
        dataForm= request.form.to_dict()
        #print (request.form.data)
        email   = dataForm['materialContactFormEmail']
        textBody= dataForm['materialContactFormMessage']
        materialContactFormCopy= dataForm['materialContactFormCopy']
        logWebApp.debug(email)
        logWebApp.debug(textBody)
        logWebApp.debug(materialContactFormCopy)

        emailMsg = Message("Contact us",
                           sender=email)
        emailMsg.add_recipient("admin@tepiloradata.com")
        #check if a copy is necessary for sender
        if materialContactFormCopy == 'on':
            emailMsg.add_recipient(email)
        emailMsg.body = textBody
        #mail.send(emailMsg)
    return redirect(url_for('home'))            

#@t.include
@app.route('/planoffering', methods = ['GET'])
def planoffering():
    #if login_fresh() == False:logout_user()
    
    #if current_user.is_authenticated == True:
    #    return render_template ('pricing.html', name=current_user.username, profile=current_user.profile, stripeListOfProductsAndPrices= stripeListOfProductsAndPrices )
    #else:
        return render_template ('pricing.html', name='', profile='')

#@t.include
@app.route('/apidoc', methods = ['GET'])
def apidoc():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('apidoc.html', name=current_user.username)
    #else:
        return render_template ('apidoc.html', name='')

#@t.include
@app.route('/apilibraries', methods = ['GET'])
def apilibraries():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('apilibraries.html', name=current_user.username)
    #else:
        return render_template ('apilibraries.html', name='')

#@t.include
@app.route('/newsletter', methods = ['GET'])
def newsletter():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('newsletter.html', name=current_user.username)
    #else:
        return render_template ('newsletter.html', name='')

#@t.include
@app.route('/blog', methods = ['GET'])
def blog():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('blog.html', name=current_user.username)
    #else:
        return render_template ('blog.html', name='')

#@t.include
@app.route('/patents', methods = ['GET'])
def patents():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('patent.html', name=current_user.username)
    #else:
        return render_template ('patent.html', name='')

#@t.include
@app.route('/disclaimer', methods = ['GET'])
def disclaimer():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('disclaimer.html', name=current_user.username)
    #else:
        return render_template ('disclaimer.html', name='')

#@t.include
@app.route('/termsandconditions', methods = ['GET'])
def termsandconditions():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('termsandconditions.html', name=current_user.username)
    #else:
        return render_template ('termsandconditions.html', name='')

#@t.include
@app.route('/idea', methods = ['GET'])
def mission():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('idea.html', name=current_user.username)
    #else:
        return render_template ('idea.html', name='')

#@t.include
@app.route('/project', methods = ['GET'])
def customers():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('project.html', name=current_user.username)
    #else:
        return render_template ('project.html', name='')

#@t.include
@app.route('/aboutus', methods = ['GET'])
def aboutus():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('aboutus.html', name=current_user.username)
    #else:
        return render_template ('aboutus.html', name='')

#@t.include
@app.route('/', methods=['GET'])
def home():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('index.html', name=current_user.username)
    #else:
        return render_template ('index.html', name='')

#@t.include
@app.route('/data', methods=['GET'])
def datahtml():
    #if login_fresh() == False:logout_user()
    #if current_user.is_authenticated == True:
    #    return render_template ('data.html', name=current_user.username)
    #else:
        return render_template ('data.html', name='')

'''
@t.include
@app.route('/upload')
@authenticationClass
@authorizationClass
def upload_file():
    apiKey= request.args.get('apikey')
    return render_template('upload.html', apikey= apiKey)
'''