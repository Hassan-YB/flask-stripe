# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:26:41 2019

@author: fleggio
"""

#import os
import logging, datetime
import socket

class Config:
##############################################################################
#          TEPILORA PROPERTY --- DO NOT MODIFY                               #
##############################################################################
    production_webserverhost='www.tepiloradata.com'
    dev_webserverhost='localhost:8000'
    TESTING = False
    DEBUG = True
    MAX_CONTENT_LENGTH= 1024 * 1024 * 10
    UPLOAD_EXTENSIONS= ['.txt', '.csv', '.json', '.xml']
    BOOTSTRAP_SERVE_LOCAL = True
    LOG_LEVEL=logging.INFO
    LOG_FILE="logs/logWebApp.log"
    STRIPE_DEV_KEYS = {
        'secret_key': 'sk_test_51Imbr8G6509MXKUYuhm0Wpskmfv8DC8tXoy9prQLKYe64QRIo5BHtaZFcT2MFG5gf5ggz0rV2Hxcm9mszn0s6eLd00ZkZd7v0X',
        'publishable_key': 'pk_test_51Imbr8G6509MXKUYlXwtF5xCxS1CusKmmxKhppWnNa3wcEu9mN721p8M8Lss9CUfeS4m0otJeJkY50meEfnnpQ4n002dFLRzo1',
        'endpoint_secret': 'whsec_Uu8s6Ggu03TxYwONUfFmC3O37y4j1eZR'
    }
##############################################################################
#         TO CHANGE VALUES                                                   #
##############################################################################

    SECRET_KEY= 'SECRET KEY'
    SECURITY_PASSWORD_SALT= 'SECURITY_PASSWORD_SALT'
##############################################################################
#         END TEPILORA PROPERTY --- DO NOT MODIFY                            #
##############################################################################

##############################################################################
#         ANY ADDITIONAL CONFIGURATION PROPERTY UNDER THIS LINE              #
##############################################################################
    dev_webserverhost='localhost:8000'
    STRIPE_URL= 'http://' + dev_webserverhost + '/'