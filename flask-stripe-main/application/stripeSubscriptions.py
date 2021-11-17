from flask.helpers import url_for
import stripe
from flask import  jsonify, render_template, request, session, flash
from werkzeug.utils import redirect
from application import app, csrf, dbSQL, migrate
import json, os
from datetime import datetime



@app.route('/webhooks', methods=['POST','GET'])
@csrf.exempt
def webhook_received():
    if request.method == 'POST':
        print ('received POST')
    webhook_secret = app.config['WEBHOOKS_SECRET']
    request_data = json.loads(request.data)
    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
            print(event)
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
    # Payment is successful and the subscription is created.
    # You should provision the subscription and save the customer ID to your database.
      print(data)
    elif event_type == 'invoice.paid':
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
      print(data)
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
      print(data)
    else:
      print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})




@app.route("/subscribe", methods=["POST","GET"])
@csrf.exempt
def subscribe():
    context = {}
    context['plans'] = Plans.query.all()
    if request.method == "GET":
        return render_template("Stripe-Plans.html",**context)
    else:
        PlanID = request.form.get('sub-id')
        #replace following line as it's hard coded for now
        PlanID = 'price_1JIZeVG6509MXKUYT7G8V6UL' #'prod_JwSZwGgM4dDlNK'
        PlanName = request.form.get('plan-name')
        #it is necessary for testing purposes
        #then should be removed as it will be retrieved with login information
        email = request.form.get('email') or None
        if not email:
            flash("Email missing!")
            return redirect(url_for('subscribe'))
        print(PlanName)
        standard = []
        if PlanName == "Standard":
            print("standard plan")
            standard = [{
                'price': PlanID,
                'quantity': 1
            }]
        else:
            print("Graduated plan")
            standard = [{
                'price': PlanID,
                'quantity': 1
            }]

        standard = [{
            'price': PlanID,
            'quantity': 1
        }]

        session = stripe.checkout.Session.create(
            success_url = app.config['STRIPE_URL'] + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = app.config['STRIPE_URL'] + 'cancel',
            payment_method_types = ['card'],
            mode = 'subscription',
            line_items = standard,
        )
        print(session)
        return redirect(session.url, code=303)

@app.route("/cancel", methods=["POST","GET"])
@csrf.exempt
def cancel_subscription():
    return render_template("Stripe-Cancelled.html")

@app.route("/success", methods=["POST","GET"])
@csrf.exempt
def subscription_success():
    return render_template("Stripe-Success.html")



def create_database(app):
    if not os.path.exists(app.config['DB_NAME']):
        dbSQL.create_all(app=app)
        print("Created Database!")

create_database(app)

