from flask.helpers import url_for
import stripe
from flask import  jsonify, render_template, request, session, flash
from werkzeug.utils import redirect
from application import app, csrf, dbSQL, migrate
import json, os,time, uuid
from datetime import datetime
from application.utilityRoutes import currentUserInfo
 
#DB_NAME = "StripeDatabase.db"
#app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

class Customer(dbSQL.Model):
    __tablename__ = 'Customer'
    id = dbSQL.Column(dbSQL.Integer(), primary_key=True)
    email = dbSQL.Column(dbSQL.String(50),unique=True)
    name = dbSQL.Column(dbSQL.String(50))
    stripe_id = dbSQL.Column(dbSQL.String(50))
    tax_type = dbSQL.Column(dbSQL.String(50),nullable=True)
    tax_value = dbSQL.Column(dbSQL.String(50),nullable=True)

    def __repr__(self):
        return f'Plan: {self.email}'

class Plans(dbSQL.Model):
    __tablename__ = 'Plans'
    id = dbSQL.Column(dbSQL.Integer(), primary_key=True)
    plan_id = dbSQL.Column(dbSQL.String(50))
    name = dbSQL.Column(dbSQL.String(50))
    description = dbSQL.Column(dbSQL.String(1000),nullable=True)
    plans = dbSQL.relationship('Pricing', backref='Plans',lazy='dynamic')

    def __repr__(self):
        return f'Plan: {self.name}'

class Pricing(dbSQL.Model):
    __tablename__ = 'Pricing'
    id = dbSQL.Column(dbSQL.Integer(), primary_key=True)
    price_id = dbSQL.Column(dbSQL.String(100))
    amount = dbSQL.Column(dbSQL.String(50))
    period = dbSQL.Column(dbSQL.String(50))
    currency = dbSQL.Column(dbSQL.String(50))
    metered_billing = dbSQL.Column(dbSQL.Boolean,default=False)
    plan_id = dbSQL.Column(dbSQL.String, dbSQL.ForeignKey('Plans.id'),nullable=False)
    # subscription = dbSQL.relationship('Subscriptions', backref='Pricing',lazy='dynamic')

    def __repr__(self):
        return f'Price = {self.amount}, Period = {self.period}'

class Subscriptions(dbSQL.Model):
    __tablename__ = 'Subscriptions'
    id = dbSQL.Column(dbSQL.Integer(), primary_key=True)
    is_active = dbSQL.Column(dbSQL.Boolean, default=False)
    plan_id = dbSQL.Column(dbSQL.String(50),nullable=True)
    price_id = dbSQL.Column(dbSQL.String(50),nullable=True)
    created_at = dbSQL.Column(dbSQL.String(50), nullable=True,default=datetime.utcnow)
    end_at = dbSQL.Column(dbSQL.String(50))
    # membership = dbSQL.Column(dbSQL.Integer, dbSQL.ForeignKey('Paypal_plans.id'),nullable=True)
    username = dbSQL.Column(dbSQL.String(50),nullable=True)
    email = dbSQL.Column(dbSQL.String(50),nullable=True)
    stripe_subscription_id = dbSQL.Column(dbSQL.String(50),nullable=True)
    stripe_subscription_item_id = dbSQL.Column(dbSQL.String(50),nullable=True)

    def __repr__(self):
        return f'Email = {self.email}, Active = {self.is_active}'

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys

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
            print('Event start')
            print(event)
            print("Event end")
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
        print('Invoice paid start')
        print(data)
        print('Invoice paid end')
        if data_object['subscription'] and data_object["status"] == "paid":
            UpdateSubscription = Subscriptions.query.filter_by(email=data_object["customer_email"]).first()
            print(data_object['subscription'],data_object['lines']['data'][0]['period']['start'])
            Start_date = datetime.fromtimestamp(data_object['lines']['data'][0]['period']['start'])
            End_date = datetime.fromtimestamp(data_object['lines']['data'][0]['period']['end'])
            UpdateSubscription.price_id = data_object['lines']['data'][0]['price']['id']
            UpdateSubscription.plan_id = data_object['lines']['data'][0]['price']['product']
            UpdateSubscription.stripe_subscription_id = data_object['subscription']
            UpdateSubscription.is_active = True
            UpdateSubscription.created_at = Start_date
            UpdateSubscription.end_at = End_date
            GetItemId = stripe.Subscription.retrieve(
                data_object['subscription'],
            )
            print('Sub retrieve start')
            print(GetItemId)
            print('Sub retrieve end')
            if GetItemId['items']['data'][0]['id']:
                UpdateSubscription.stripe_subscription_item_id = GetItemId['items']['data'][0]['id']
            dbSQL.session.add(UpdateSubscription) 
            dbSQL.session.commit()
            print(UpdateSubscription)
            

        return jsonify({'status': 'success'})
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
      
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
      print(data)
    else:
      print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})


@app.route("/create-plans", methods=["POST","GET"])
def create_plans():
    if request.method == "POST":
        PlanName = request.form.get('plan-name') or None
        Description = request.form.get('description') or None
        if PlanName:
            check = Plans.query.filter_by(name=PlanName).first()
            print(check)
            if check:
                flash("Plan with similar name already existed!")
                return redirect(url_for('create_plans'))
            else:
                response = stripe.Product.create(name=PlanName,description=Description)
                print(response)
                created_plan = Plans(
                    name = response['name'],
                    plan_id = response['id'],
                    description = response['description']
                )
                print(created_plan)
                dbSQL.session.add(created_plan)
                dbSQL.session.commit()
                flash("Plan created successfully!")
        else:
            flash("Enter Product name!")
        return render_template("Stripe-CreatePlans.html")
    else:
        return render_template("Stripe-CreatePlans.html")

@app.route("/declare-prices", methods=["POST","GET"])
def declare_pricing():
    if request.method == "POST":
        context = {}
        context['plans'] = Plans.query.all()
        PlanID = request.form.get('plan-id') or None
        Price = request.form.get('price') or None
        Currency = request.form.get('currency') or None
        Graduated = request.form.get('graduated') or False
        Interval = request.form.get('interval') or None
        print(f"Price:{Price},Graduated:{Graduated}")
        var = False
        if Graduated:
            var = True
        if not PlanID:
            flash("No plan selected!")
            return redirect(url_for('declare_pricing'))
        if var == True:
            print("Graduated")
            response  = stripe.Price.create(
                product= f"{PlanID}",
                currency = f"{Currency}",
                billing_scheme = "tiered",
                tiers = [{
                    'flat_amount' : f'{Price}',
                    'unit_amount' : '100',
                    'up_to' : 'inf'
                }],
                tiers_mode = "graduated",
                recurring =  {
                    'interval': f'{Interval}',
                    'usage_type': 'metered',
                }                
            )
            print(response)
        else:
            print("standard")
            response = stripe.Price.create(
                unit_amount = Price,
                currency = f"{Currency}",
                recurring = {"interval": f"{Interval}"},
                product = f"{PlanID}",
            )
            print(response)
        created_pricing = Pricing(
            amount = Price,
            period = response["recurring"]["interval"],
            metered_billing = var,
            currency = Currency,
            price_id = response["id"]
        )
        get_plan = Plans.query.filter_by(plan_id=PlanID).first()
        get_plan.plans.append(created_pricing)
        dbSQL.session.add(get_plan)
        dbSQL.session.add(created_pricing)
        dbSQL.session.commit()
        print(created_pricing)
        flash("Pricing added to plan successfully!")
        return render_template("Stripe-DeclarePricing.html",**context)
    else:
        context = {}
        context['plans'] = Plans.query.all()
        return render_template("Stripe-DeclarePricing.html",**context)

@app.route("/subscribe", methods=["POST","GET"])
@csrf.exempt
def subscribe():
    context = {}
    context['plans'] = Plans.query.all()
    if request.method == "GET":
        return render_template("Stripe-Plans.html",**context)
    else:
        priceID = request.form.get('sub-id')
        #replace following line as it's hard coded for now
        #PlanID = 'price_1JIZeVG6509MXKUYT7G8V6UL' #'prod_JwSZwGgM4dDlNK'
        planType = request.form.get('plan-name')
        print(planType)
        #it is necessary for testing purposes
        #then should be removed as it will be retrieved with login information
        email = request.form.get('email') or None
        GetCustomer = Customer.query.filter_by(email=email).first()
        if not email:
            flash("Email missing!")
            return redirect(url_for('planoffering'))
        if not GetCustomer:
            flash("No customer with that email exists! Kindly register first.")
            return redirect(url_for('planoffering'))
        else:
            print(GetCustomer)
        standard = []
        #it references billing scheme
        if planType == 'per_unit': #"Standard":
            print("standard plan")
            standard = [{
                'price': priceID,
                'quantity': 1
            }]
        elif planType == 'tiered' : #graduated
            print("Graduated plan")
            standard = [{
                'price': priceID,
            }]
        else:
            return 

        session = stripe.checkout.Session.create(
            customer = GetCustomer.stripe_id,
            success_url = app.config['STRIPE_URL'] + 'success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = app.config['STRIPE_URL'] + 'cancel',
            payment_method_types = ['card'],
            mode = 'subscription',
            line_items = standard,
            tax_id_collection = {
                'enabled': True,
            },
            customer_update = {
                'name': 'auto',
                'address': 'auto',
            },
        )
        print(session)
        AddSubscription = Subscriptions(
            email = email,
            plan_id = priceID
        )
        print(AddSubscription)
        dbSQL.session.add(AddSubscription)
        dbSQL.session.commit()
        return redirect(session.url, code=303)

@app.route("/cancel", methods=["POST","GET"])
@csrf.exempt
def cancelled():
    return render_template("Stripe-Cancelled.html")

@app.route("/success", methods=["POST","GET"])
@csrf.exempt
def subscription_success():
    return render_template("Stripe-Success.html")

@app.route("/delete-pricings", methods=["POST","GET"])
@csrf.exempt
def delete_pricings():
    Pricing.query.delete()
    dbSQL.session.commit()
    flash("Pricings deleted!")
    return redirect(url_for('declare_pricing'))

@app.route("/create-customer", methods=["POST","GET"])
def create_customer():
    if request.method == "POST":
        CustomerName = request.form.get('customer-name') or None
        email = request.form.get('customer-email') or None
        TaxType = request.form.get('tax-type') or None
        TaxValue = request.form.get('tax-value') or None
        if email:
            check = Customer.query.filter_by(email=email).first()
            if check:
                flash("Customer with that email already exists!")
                return redirect(url_for('create_customer'))
            else:
                response = stripe.Customer.create(
                    email = email,
                    name = CustomerName
                )
                TaxResponse = None
                if TaxType and TaxValue:
                    TaxResponse = stripe.Customer.create_tax_id(
                        response['id'],
                        type = TaxType,
                        value = TaxValue
                    )
                if TaxResponse:
                    New_customer = Customer(
                        name = response['name'],
                        email = response['email'],
                        stripe_id = response['id'],
                        tax_type = TaxResponse['id'],
                        tax_value = TaxResponse['type']
                    )
                else:
                    New_customer = Customer(
                        name = response['name'],
                        email = response['email'],
                        stripe_id = response['id']
                    )
                print(response)
                dbSQL.session.add(New_customer)
                dbSQL.session.commit()
                flash("Customer added successfully!")
        else:
            flash("Enter customer email!")
        return render_template("Stripe-Customer.html")
    else:
        return render_template("Stripe-Customer.html")

@app.route("/user-dashboard", methods=["POST","GET"])
def user_dashboard():
    if request.method == "POST":
        email = request.form.get('email') or None
        print(email)
        if email:
            context = {}
            session['email'] = email
            GetSubscription = Subscriptions.query.filter_by(email=email).first()
            context['subscription'] = GetSubscription
            currentUserData= currentUserInfo
            Userdynamicinfo = {}
            current_usage = 0
            if GetSubscription.stripe_subscription_item_id:
                response = stripe.SubscriptionItem.list_usage_record_summaries(
                    f"{GetSubscription.stripe_subscription_item_id}"
                )
                current_usage = response['data'][0]['total_usage']
            if GetSubscription.price_id:
                Pricedata = stripe.Price.retrieve(
                    f"{GetSubscription.price_id}",
                    )
                print("Price data")
                print(Pricedata)
                interval = Pricedata['recurring']['interval']
            if GetSubscription.plan_id:
                data = stripe.Product.retrieve(
                    f"{GetSubscription.plan_id}",
                    )
                print("Plan data")
                print(data)
                if data:
                    stat = True
                limitperday = data['metadata']['LimitPerDay'] or None
                LimitPerMonth = data['metadata']['LimitPerMonth'] or None
                des1 = data['metadata']['des1'] or None
                des2 = data['metadata']['des2'] or None
                des3 = data['metadata']['des3'] or None  
            #pass to Stripe-Dashboard.html also currentUserData and display as meaningful info like:
            # your apikey is ...
            # your current plan is limited to:
            #     daily calls = 
            #     montly calls = 
            # your current usage is :
            # ...
            return render_template("Stripe-Dashboard.html",**context, usage = current_usage,statistics=stat,limitperday=limitperday,LimitPerMonth=LimitPerMonth,des1=des1,des2=des2,des3=des3,interval=interval)
        else:
            flash('No email found!')
            return redirect(url_for('user_dashboard'))
    else:
        return render_template("Stripe-Dashboard.html")

@app.route("/update-subscription", methods=["POST","GET"])
def update_subscription():
    if 'email' in session:
        print(session['email'])
        email = session['email']
        GetSubscription = Subscriptions.query.filter_by(email=email).first()
        if GetSubscription.is_active:
            subscription = stripe.Subscription.retrieve(GetSubscription.stripe_subscription_id)
            response = stripe.Subscription.modify(
                subscription.id,
                cancel_at_period_end=False,
                proration_behavior='always_invoice', #Use this to get payment at the end 'create_prorations'
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': 'price_1JuQJqB4k1y3jDV8dgWgFE3A', #hard-coded price id for now
                }]
            )
            print(response)
            flash('Subscription updated')
            return redirect(url_for('user_dashboard'))
        else:
            flash('No active subscription!')
            return redirect(url_for('user_dashboard'))
    else:
        flash('No email found!')
        return redirect(url_for('user_dashboard'))


@app.route("/cancel-subscription", methods=["POST","GET"])
def cancel_subscription():
    if 'email' in session:
        print(session['email'])
        response = Subscriptions.query.filter_by(email=session['email']).first()
        if response.is_active:
            stripe.Subscription.delete(
                response.stripe_subscription_id,
            )
            print(response)
            response.is_active = False
            dbSQL.session.add(response)
            dbSQL.session.commit()
            flash("Subscription canceled!")
            return redirect(url_for('user_dashboard'))
        else:
            flash("No active subscription!")
            return redirect(url_for('user_dashboard'))
    else:
        flash("No email found!")
        return redirect(url_for('user_dashboard'))



@app.route("/report-usage", methods=["POST","GET"])
def report_usage():
    if request.method == "POST":
        # This code can be run on an interval (e.g., every 24 hours) for each active
        # metered subscription.

        # You need to write some of your own business logic before creating the
        # usage record. Pull a record of a customer from your database
        # and extract the customer's Stripe Subscription Item ID and usage
        # for the day. If you aren't storing subscription item IDs,
        # you can retrieve the subscription and check for subscription items
        # https://stripe.com/docs/api/subscriptions/object#subscription_object-items.

        email = request.form.get('email') or None
        units  = int(request.form.get('units')) or None

        if not email and units:
            flash('No email and units found!')
            return redirect(url_for('report_usage'))
        
        response = Subscriptions.query.filter_by(email=email).first()

        if not response.is_active:
            flash('No active subscription!')
            return redirect(url_for('report_usage'))

        subscription_item_id = response.stripe_subscription_item_id

        # The usage number you've been keeping track of in your database for
        # the last 24 hours.
        usage_quantity = units

        timestamp = int(time.time())

        # The idempotency key allows you to retry this usage record call if it fails.
        idempotency_key = str(uuid.uuid4())
        print(idempotency_key)

        try:
            response = stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=usage_quantity,
                timestamp=timestamp,
                action='set',
                idempotency_key=idempotency_key
            )
            print(response)
            pass
        except stripe.error.StripeError as e:
            print('Usage report failed for item ID %s with idempotency key %s: %s' %
            (subscription_item_id, idempotency_key, e.error.message))
            pass
        
        flash("Units reported")
        return redirect(url_for('report_usage'))
    else:
        return render_template('Stripe-Report-Usage.html')

def create_database(app):
    if not os.path.exists(app.config['DB_NAME']):
        dbSQL.create_all(app=app)
        print("Created Database!")

create_database(app)

if __name__ == '__main__':
    app.run(debug=True)