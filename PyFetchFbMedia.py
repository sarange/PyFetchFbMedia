#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
File: /home/sarange/Documents/PyFetchFbMedia/pyfacebook.py
Project: /home/sarange/Documents/PyFetchFbMedia
Created Date: Thursday, September 26th 2019, 12:11:06 am
Author: sarange
-----
Last Modified: Fri Sep 27 2019
Modified By: sarange
-----
Copyright (c) 2019 sarange

Talk is cheap. Show me the code.
'''

from selenium.webdriver import FirefoxProfile
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os.path import realpath, exists, dirname
from os import makedirs
from pathlib import Path
from re import findall
from time import sleep, strftime, time
from subprocess import call
from shutil import move
from pickle import dump, load
from threading import Event

class Account():

	def __init__(self, signal, lock, name, people, headless=True, debug=False):
		# Variables
		self.start = time()
		self.convLists = ['Conversation List', 'Λίστα συζητήσεων']   # Add your language here
		self.name = name
		self.people = people
		self.lock = lock
		self.signal = signal
		self.path = dirname(realpath(__file__))
		self.cookies = f'{self.path}/cookies/{self.name}_cookies.pkl'
		self.mediapath = f'{self.path}/media/{self.name}'
		self.logpath = f'{self.path}/media/{self.name}/last.log'
		self.debug = debug
		self.logFile = f'{self.path}/logs/{self.name}_{strftime("%d-%m-%y-%H.%M.%S")}.log'
		self.url_messages = 'https://www.facebook.com/messages/t/'
		self.url_home = 'https://facebook.com'
		self.timeout = 1
		self.iter_L = 60
		self.iter = self.iter_L
		self.maxBack = 30
		self.faults = 0
		self.faultThreashold = 3

		# Initialize Gecko driver
		agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'
		profile = FirefoxProfile()
		profile.set_preference('general.useragent.override', agent)
		options = Options()
		options.headless = headless
		self.driver = Firefox(profile, options=options)
		
		# Make folders 
		self.makeFolder(f'{self.path}/logs')
		self.makeFolder(self.mediapath)
		for person in self.people:
			self.makeFolder(f'{self.mediapath}/{person}')

	def getToMessages(self):
	# Points driver to url_messages
		if self.url_messages != self.driver.current_url:
			self.driver.get(self.url_messages)
			self.waitU('_1enh')

	def getToHome(self):
	# Points driver to url_home
		self.driver.get(self.url_home)
		self.waitU('facebook')

	def waitU(self, element_id):
	# Waits until the element element_id is available
		try:
			element_present = EC.presence_of_element_located((By.ID, element_id))
			WebDriverWait(self.driver, self.timeout).until(element_present)
		except TimeoutException:
			pass

	def getConversations(self, people):
	# Locates element of conversation
		self.logIt(f'Get to conversation with list {people}')
		for convList in self.convLists:
			if convList in self.driver.page_source:
				conversations = self.driver.find_elements_by_xpath(f'//ul[@aria-label="{convList}"]//li[@tabindex="-1"]')
		conv = []
		for i in conversations:
			person = findall('data-href="https://www.facebook.com/messages/t/(.*?)"', i.get_attribute('innerHTML'))[0]
			if person in people:
				conv.append(i)
		return conv

	def getToThread(self, num):
	# Wrapper to download media
		self.logIt(f'Getting to thread, media {num}')
		self.waitU('_3m31')
		threads = self.driver.find_elements_by_xpath('//a[@class="_3m31"]')
		thread = threads[num]
		if self.existsMedia(thread.get_attribute('innerHTML')):
			return
		thread.click()
		self.waitU('_4-od')
		self.getMedia()
		thread.send_keys(Keys.ESCAPE)
		return len(threads)
		
	def login(self, username, password):
	# Logs in to account, USE WITH CAUTION
		self.logIt('Trying to login, USE WITH CAUSION!! (sleeping for 10 secs)')
		sleep(10)
		driver = self.driver
		self.getToHome()
		elem = driver.find_element_by_id('email')
		elem.send_keys(username)
		elem = driver.find_element_by_id('pass')
		elem.send_keys(password)
		elem.send_keys(Keys.RETURN)
		self.waitU('userNav')
		self.saveCookies()

	def saveCookies(self):
	# Saves the cookies
		self.logIt(f'Saving cookies')
		self.makeFolder(f'{self.path}/cookies/')
		if Path(self.cookies).is_file():
			move(self.cookies, f'{self.cookies}.bak')
		with open(self.cookies,'wb') as filehandler:
			dump(self.driver.get_cookies(), filehandler)
	
	def loadCookies(self):
	# Loads the cookies
		if exists(self.cookies):
			self.getToHome()
			self.logIt(f'Loading cookies')
			with open(self.cookies, 'rb') as cookiesfile:
				cookies = load(cookiesfile)
				for cookie in cookies:
					self.driver.add_cookie(cookie)
		else:
			raise ValueError('Cookies file not found!')

	def isRead(self, person, elem):
	# Checks if the conversation is read
		if '_1ht3' in elem.get_attribute('outerHTML'):
			self.logIt(f'Conversation with {person} is not read')
			self.iter = 2
			return False
		else:
			self.logIt(f'Conversation with {person} is read')
			return True

	def getPerson(self, person, override):
	# Checks if the conversation is read and if so it gets in
		self.person = person
		try:
			elem = self.getConversations(person)[0]
			if self.isRead(person, elem) or override:
				elem.click()
				self.faults = 0
				return True
		except Exception as e:
			self.logIt(f'{person} not rechable ({e})')
			if self.pressEscape():
				self.logIt('Pressed escape!')
			else:
				self.faults += 1
		return False

	def downloadMedia(self, link):
	# Downloads the media
		self.logIt(f'Downloading media with person {self.person}')
		file = findall('/(\d+_\d+_\d+_\w\.\w{3,4})\?', link)[0]
		if not Path(f'{self.mediapath}{file}').is_file():
			call(['curl', '-s', link,'-o', f'{self.mediapath}/{self.person}/{file}'])
			return False
		else:
			self.iter = self.iter_L
			return True

	def getMedia(self):
	# Finds the media inside the conversation
		self.logIt(f'Trying to get media')
		photo = self.driver.find_element_by_class_name('_4-od')
		image = findall('src="(.*?)"',photo.get_attribute('innerHTML'))[0]
		return self.downloadMedia(image.replace('amp;', ''))

	def existsMedia(self, media):
	# Checks if the media exists
		medianame = findall('/(\d+_\d+_\d+_\w\.\w{3,4})\?', media)[0]
		if not Path(self.logpath).is_file():
			with open(self.logpath, 'w') as f:
				f.write('---\n')
		with open(self.logpath, 'r+') as f:
			if medianame not in f.read():
				f.write(f'{medianame}\n')
				self.logIt('Media does not exist, fetching it')
				return False
			else:
				self.logIt('Media exists')
				return True

	def manageThread(self, person, override):
	# Wrapper
		lenght = 0
		now = 0
		while self.getPerson(person, override):
			try:
				lenght = self.getToThread(now)
				now += 1
				if now == lenght or now > self.maxBack:
					return
			except:
				return
		return

	def manageThreads(self, override):
	# Main wrapper function
		for person in self.people:
			self.logIt(f'Now on person {person}')
			self.manageThread(person, override)
		self.logIt(f'Sleeping for {self.iter} secs')
		sleep(self.iter)
		return True if self.faults < self.faultThreashold else False
	
	def pressEscape(self):
	# Presses escape
		elements = ['_4-od','_3m31', '_1enh']
		for element in elements:
			try:
				elem = self.driver.find_element_by_class_name(element)
				elem.send_keys(Keys.ESCAPE)
				return True
			except:
				pass
		return False

	def makeFolder(self, path):
	# Makes folder if it doesn't exist
		if not exists(path):
			makedirs(path)
			self.logIt(f'Making a new forlder in {path}')

	def logIt(self, message):
	# Logs events and prints on screen debugging information
		self.signal.set()
		with open(self.logFile, 'a') as log:
			log.write(f'[{self.name}]: {message}, t+{round(time()-self.start)}s\n')
		if self.debug:
			with self.lock:
				print(f'[{self.name}]: {message}, t+{round(time()-self.start)}s')