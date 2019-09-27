#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
File: /home/sarange/Documents/pyfacebook/makeCookies.py
Project: /home/sarange/Documents/pyfacebook
Created Date: Thursday, July 18th 2019, 3:55:12 pm
Author: sarange
-----
Last Modified: Thu Sep 26 2019
Modified By: sarange
-----
Copyright (c) 2019 sarange

Talk is cheap. Show me the code.
'''

cookie_name = 'MyProfile1'

# Put your cookies to the changeMe filed with quotes ('')

a = {'name': 'datr', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
b = {'name': 'sb', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
c = {'name': 'spin', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
d = {'name': 'c_user', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
e = {'name': 'xs', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
f = {'name': 'fr', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
g = {'name': 'pnl_data2', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}
h = {'name': 'wd', 'value': 'changeMe', 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': False, 'expiry': 'changeMe'}

cook = [a,b,c,d,e,f,g,h]

with open(f'cookies/{cookie_name}_cookies.pkl','wb') as filehandler:
	__import__("pickle").dump(cook, filehandler)