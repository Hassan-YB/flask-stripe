# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:26:42 2019

@author: fleggio
"""

from flask import Flask #, g
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from flask_login import LoginManager, current_user, login_fresh, logout_user
from flask_mail import Mail
from flask_limiter import Limiter
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoEngineStorage
import logging,stripe, socket, requests, json
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#################################################



# ********** core app initialization **************
app = Flask(__name__)
#connecting flask to dash

app.config.from_object('config.Config') # loads in the current path from config.py the class Config

#
# logging setup
logWebApp = logging.getLogger("tepiloradataWebApp")
logWebApp.setLevel(app.config['LOG_LEVEL'])
logWebAppHandler= logging.FileHandler(app.config['LOG_FILE'])
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "", "%")
logWebAppHandler.setFormatter(formatter)
logWebApp.addHandler(logWebAppHandler)
logWebApp.info("Starting application")

##############################################################################
#                BEGINE STRIPE CONFIGURATION                                 #
##############################################################################

stripePvtKey=app.config['STRIPE_DEV_KEYS'].get('secret_key')
stripePubKey=app.config['STRIPE_DEV_KEYS'].get('publishable_key')
stripePvtEndpoint=app.config['STRIPE_DEV_KEYS'].get('endpoint_secret')
stripe.api_key = stripePvtKey

stripeDomainUrl=app.config['STRIPE_URL']

stripeListOfProductsAndPrices=[]

jsonListOfProducts= stripe.Product.list(limit=100)        
jsonListOfPrices= stripe.Price.list(limit=100)
# print("products")
# print(stripe.Product.list(limit=100))
# print("Prices")
# print(stripe.Price.list(limit=100))
#######################################################################
# stripe graduated prices, with flat subscription and soft limit      #
# any additional call will be invoiced at the end of the month        #
#######################################################################
for product in jsonListOfProducts['data']:
    for price in jsonListOfPrices['data']:
        if price['product']==product['id'] and price['active']==True and product['active']==True:
            priceFullInfo = stripe.Price.retrieve(
              price['id'], 
              expand = ['tiers']#"price_1JIZeVG6509MXKUYT7G8V6UL",
            )
            print("info")
            print(priceFullInfo)
            try:
                if len(priceFullInfo.tiers) > 0:
                    priceFlat= priceFullInfo.tiers[0]['flat_amount']/100
                    limitCallsPriceFlat= priceFullInfo.tiers[0]['up_to']
                    priceInc= priceFullInfo.tiers[1]['unit_amount']/100
                    stripeListOfProductsAndPrices.append({'id': product['id'], 'name':product['name'], 'priceId': price['id'], 'billingScheme': price['billing_scheme'], 'metadata': product['metadata'].to_dict(), 'price':priceFlat, 'incPrice':priceInc , 'limitCallsPriceFlat':limitCallsPriceFlat, 'currency':price['currency'] })
            except: 
                try:
                    priceFlat= priceFullInfo['unit_amount']/100
                    limitCallsPriceFlat= product['metadata']['limitPerMonth']
                    priceInc= 0
                    stripeListOfProductsAndPrices.append({'id': product['id'], 'name':product['name'], 'priceId': price['id'], 'billingScheme': price['billing_scheme'], 'metadata': product['metadata'].to_dict(), 'price':priceFlat, 'incPrice':priceInc , 'limitCallsPriceFlat':limitCallsPriceFlat, 'currency':price['currency'] })
                except: pass
        

stripeListOfProductsAndPrices= sorted(stripeListOfProductsAndPrices, key=lambda i:i['price'])

csrf = CSRFProtect(app)
dbSQL = SQLAlchemy(app)
migrate = Migrate(app, dbSQL)

##############################################################################
#                END STRIPE CONFIGURATION                                    #
##############################################################################


limiter = Limiter()
logWebApp.info("Initizalized Limiter")





    
##############################################################################
#############################################################################

# loading data into app context
with app.app_context():
    #include routes definition
    from application import webRoutes, stripeSubscriptions, utilityRoutes# ,login stripeRoutes,
    from application import HTTPerrors#, apiRoutes
    
    
    