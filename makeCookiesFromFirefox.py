#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
File: /home/sarange/Documents/pyfacebook/makeCookies.py
Project: /home/sarange/Documents/pyfacebook
Created Date: Thursday, July 18th 2019, 3:55:12 pm
Author: sarange
-----
Last Modified: Fri Sep 27 2019
Modified By: sarange
-----
Copyright (c) 2019 sarange

Talk is cheap. Show me the code.
'''
def main():
	import sqlite3
	from pathlib import Path
	from os.path import realpath, dirname, exists
	from os import makedirs


	cookie_name = 'MyProfile1'
	if not Path(f'{dirname(realpath(__file__))}/cookies.sqlite').is_file():
		raise ValueError('Didn\'t find a cookies.sqlite file in executing path')
	
	conn = sqlite3.connect('cookies.sqlite')
	c = conn.cursor()
	names = ['datr', 'sb', 'spin', 'c_user', 'xs', 'fr', 'pnl_data2', 'wd']
	db = lambda value, name: c.execute(f'SELECT {value} FROM moz_cookies WHERE name=="{name}"').fetchone()[0]
	cook = []

	for name in names:
		try:
			if db('isHttpOnly',name)==1:
				httpOnly = True
			else:
				httpOnly = False
			cook.append({'name': name, 'value': db('value', name), 'path': '/', 'domain': '.facebook.com', 'secure': True, 'httpOnly': httpOnly, 'expiry': db('expiry', name)})
		except:
			pass

	conn.close()

	if not exists('cookies'):
		makedirs('cookies')

	with open(f'cookies/{cookie_name}_cookies.pkl','wb') as filehandler:
		__import__("pickle").dump(cook, filehandler)

if __name__ == '__main__':
	main()