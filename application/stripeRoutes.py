# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Wed Aug 12 09:40:28 2020

# @author: fleggio@tibco.com
# """
# from flask import  jsonify, render_template, request, session#, url_for # send_from_directory
# from application import app,  logWebApp, stripePvtKey, stripePubKey, stripePvtEndpoint, stripeDomainUrl, stripeListOfProductsAndPrices#, mail, t,client
# #from .models import User, validate_username, validate_password, check_password, check_profile
# #from .token import generate_confirmation_token, confirm_token
# #from werkzeug.security import check_password_hash, generate_password_hash
# from flask_login import  current_user, login_fresh, logout_user
# #import datetime, 
# #from .authenticationDecorator import authenticationClass
# #from .authorizationDecorator import authorizationClass
# #import os#, uuid#from bson.json_util import dumps
# #from flask_mail import Message
# import stripe



# #@t.include
# @app.route("/publishablekey")
# def get_publishable_key():
#     stripe_config = {"publicKey": stripePubKey}
#     return jsonify(stripe_config)


# #@t.include
# @app.route('/payment', methods = ['GET'])
# def payment():
#     if login_fresh() == False:logout_user()

#     if current_user.is_authenticated == False:
#          return render_template ('pricing.html', name='', profile='')
     
#     productId=request.args.get('payOption')
    
#     if productId == '' or productId is None:
#         return render_template ('pricing.html', name=current_user.username, profile=current_user.profile, stripeListOfProductsAndPrices= stripeListOfProductsAndPrices )
    
#     session['productId']= productId
#     my_item = next((item for item in stripeListOfProductsAndPrices if item['id'] == session['productId']), None)

#     #dataForm= request.form.to_dict()
#     #print (request.form.data)
#     return render_template ('payment.html', name=current_user.username, profile=current_user.profile, payAmount= my_item['price'], currency= my_item['currency'])

# #@t.include
# @app.route("/create-checkout-session")
# def create_checkout_session():
#     print (stripeDomainUrl)
#     #domain_url = stripeDomainUrl # "http://localhost:8000/"
#     if login_fresh() == False:logout_user()

#     if current_user.is_authenticated == False: return render_template ('pricing.html', name='', profile='')

#     stripe.api_key = stripePvtKey
     
#     try:
#         # Create new Checkout Session for the order
#         # Other optional params include:
#         # [billing_address_collection] - to display billing address details on the page
#         # [customer] - if you have an existing Stripe Customer ID
#         # [payment_intent_data] - capture the payment later
#         # [customer_email] - prefill the email input in the form
#         # For full details see https://stripe.com/docs/api/checkout/sessions/create

#         # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
#         my_item = next((item for item in stripeListOfProductsAndPrices if item['id'] == session['productId']), None)
#         checkout_session = stripe.checkout.Session.create(
#             success_url=stripeDomainUrl + "paymentsuccess?session_id={CHECKOUT_SESSION_ID}",
#             cancel_url=stripeDomainUrl + "paymentcancelled",
#             payment_method_types=["card"],
#             mode="payment",
#             line_items=[
#                 {
#                     "name": my_item['name'],
#                     "quantity": 1,
#                     "currency": my_item['currency'],
#                     "amount": int(my_item['price']*100), #10.00 translates into 1000 as amount
#                 }
#             ]
#         )
#         return jsonify({"sessionId": checkout_session["id"]})
#     except Exception as e:
#         return jsonify(error=str(e)), 403
    

# @app.route("/paymentsuccess")
# def success():

#     if current_user.is_authenticated == False:
#         return render_template ('index.html', name='')

#     stripeSessionId=request.args.get('session_id')

#     if stripeSessionId == '' or stripeSessionId is None:
#         return render_template ('index.html', name=current_user.username)

#     stripe.api_key = stripePvtKey
#     try:
#         stripeSessionObj= stripe.checkout.Session.retrieve(stripeSessionId)        
#     except:
#         return render_template ('index.html', name=current_user.username)        

#     if stripeSessionObj['payment_status'] != 'paid':
#         return render_template ('index.html', name=current_user.username)
    
#     my_item = next((item for item in stripeListOfProductsAndPrices if item['id'] == session['productId']), None)
    
#     if my_item is None:
#         logWebApp.error("User " + current_user.email + " paid successfully product " + session['productId'] + ". Anyway wsgi couldn't retrieive it for updating limitsConfiguration collection")
#         msg= 'Something went wrong while updating authorization for your payment. Please contact admin@tepiloradata.com and provide apikey= ' + current_user.apikey + ' and your registration email= ' + current_user.email
#         return render_template("paymentsuccess.html", msg=msg)    
#     try:
#         collectionLimits= client['APIs']['limitsConfiguration']
#         collectionLimits.update_one({'apikey' : current_user.apikey},
#                               {'$set':{
#                                            'limitPerDay' : int(my_item['metadata']['limitPerDay'])
#                                        , 'limitPerMonth': int(my_item['metadata']['limitPerMonth'])
#                                        , 'hardLimit' : True
#                                        , 'email' : current_user.email
#                                        }
#                                   },upsert=True)
#     except:
#         logWebApp.error("Couldn't update limitsConfiguration for " + current_user.email + " and apikey= " + current_user.apikey + " and product=" + session['productId'])
#         msg= 'Something went wrong while updating authorization for your payment. Please contact admin@tepiloradata.com and provide apikey= ' + current_user.apikey + ' and your registration email= ' + current_user.email
#         return render_template("paymentsuccess.html", msg=msg)    


#     try:
#         collectionAccounts= client['APIs']['accounts']
#         collectionAccounts.update_one({'apikey' : current_user.apikey},
#                               {'$set':{
#                                            'role' : my_item['name']
#                                        }
#                                   },upsert=True)
#     except:
#         logWebApp.error("Couldn't update accounts for " + current_user.email + " and apikey= " + current_user.apikey + " and product=" + session['productId'])
#         msg= 'Something went wrong while updating authorization for your payment. Please contact admin@tepiloradata.com and provide apikey= ' + current_user.apikey + ' and your registration email= ' + current_user.email
#         return render_template("paymentsuccess.html", msg=msg)    

    
#     return render_template("paymentsuccess.html", msg='')


# @app.route("/paymentcancelled")
# def cancelled():
#     if current_user.is_authenticated == False:
#         return render_template ('index.html', name='')

#     stripeSessionId=request.args.get('session_id')

#     if stripeSessionId == '' or stripeSessionId is None:
#         return render_template ('index.html', name=current_user.username)

#     stripe.api_key = stripePvtKey
#     try:
#         stripeSessionObj= stripe.checkout.Session.retrieve(stripeSessionId)        
#     except:
#         return render_template ('index.html', name=current_user.username)        

#     if stripeSessionObj['payment_status'] == 'paid':
#         return render_template ('index.html', name=current_user.username)

#     msg= 'Payment authorization has been declined by your Bank. Please try again later. If the error persists try contacting your bank and/or admin@tepiloradata.com and provide apikey= ' + current_user.apikey + ' and your registration email= ' + current_user.email
#     return render_template("paymentcancelled.html", msg)



# @app.route("/webhook", methods=["POST"])
# def stripe_webhook():
#     payload = request.get_data(as_text=True)
#     sig_header = request.headers.get("Stripe-Signature")

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, stripePvtEndpoint
#         )

#     except ValueError as e:
#         # Invalid payload
#         return "Invalid payload", 400
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return "Invalid signature", 400

#     # Handle the checkout.session.completed event
#     if event["type"] == "checkout.session.completed":
#         print("Payment was successful.")
#         # TODO: run some custom code here
#         # Payment is successful and the subscription is created.
#         # You should provision the subscription and save the customer ID to your database

#     if event["type"] == 'invoice.paid':
#         print("invoice.paid")
#         # Continue to provision the subscription as payments continue to be made.
#         # Store the status in your database and check when a user accesses your service.
#         # This approach helps you avoid hitting rate limits.
#     if event["type"] == 'invoice.payment_failed':
#         print('invoice.payment_failed')
#         # The payment failed or the customer does not have a valid payment method.
#         # The subscription becomes past_due. Notify your customer and send them to the
#         # customer portal to update their payment information.

#     return "Success", 200