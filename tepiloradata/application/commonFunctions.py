#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 08:11:55 2020

@author: fleggio@tibco.com
"""
import json

def returnJsonString(errCode, errKey, errMsg, errMsg2):
    retJsonString= {
                "error": {
                        "code": errCode,
                        "message": errMsg,
                        "context": {
                                "symbols": [
                                    {
                                        "key": errKey,
                                        "message": errMsg2
                                    }
                                ]
                        }
                }
            }
    return json.dumps(retJsonString)
