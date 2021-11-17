# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:29:09 2019

@author: fleggio
"""

#from werkzeug.wsgi import DispatcherMiddleware
#from werkzeug import DispatcherMiddleware
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from application import app as tepiloradata #flask_app
#from application.reporting import app as appDashReporting

#tepiloradata = DispatcherMiddleware(flask_app, {
#    '/reporting': appDashReporting.server
#})



if __name__ == "__main__":
    #context = ('ServerCertificate.pem', 'ServerKey.pem')
    #78ad516c-e3e5-47d2-89ad-76d4e429c629
    #app.run(host='0.0.0.0', port=8000, debug=False)#, ssl_context=context)
    run_simple('localhost', 8000, tepiloradata) 
         
