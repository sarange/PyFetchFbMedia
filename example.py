#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
File: /home/sarange/Documents/PyFetchFbMedia/example.py
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
from threading import Thread, Lock, Event
from PyFetchFbMedia import Account
from time import strftime, time, sleep
from settings import names
from makeCookiesFromFirefox import main as makeCookiesFromFirefox

def job(stop, signal, lock, name, people, headless=True, debug=False, override=False):
	start = time()
	account = Account(signal, lock, name, people, headless=headless, debug=debug)
	account.logIt(f'Starting thread on people {people} (headless={headless}, debug={debug}), t={strftime("%H:%M:%S")}')
	try:
		account.loadCookies()
		account.logIt('Cookies found, loaded')
	except:
		account.logIt('Cookies not found, searching for cookies.sqlite')
		makeCookiesFromFirefox()
		account.loadCookies()
	account.getToMessages()
	account.saveCookies()
	try:
		while not stop.isSet():
			if not account.manageThreads(override):
				stop.set()
	except Exception as e:
		account.logIt(f'Exception {e} catched inside thread, trying to restart it')
		account.logIt(f'Restarting thread {name}')

def waitForJobs(start, signals, watchers, names, timerForNonRespoindingThreads):
	while True:
		try:
			for name in names:
				if signals[name['name']].isSet():
					watchers[name['name']] = time()
					signals[name['name']].clear()
				else:
					if watchers[name['name']] + timerForNonRespoindingThreads < time():
						print(f'A thread is not responding, trying to restart it, t+{round(time() - start)}s')
						return
			sleep(10)
		except:
			print(f'Exception catched in main thread, trying to restart it, t+{round(time() - start)}s')
			return

def main():
	timeWaitingExitingThreads = 30
	timerForNonRespoindingThreads = 3*60
	lock = Lock()
	stop = Event()
	signals = {}
	watchers = {}
	while True:
		threads = []
		start = time()
		for name in names:
			signals[name['name']] = Event()
			watchers[name['name']] = time()
			thread = Thread(target=job, args=(stop, signals[name['name']], lock, name['name'], name['people'], name['headless'], name['debug'], name['override']), daemon=True)
			threads += [thread]
			thread.start()
		waitForJobs(start, signals, watchers, names, timerForNonRespoindingThreads)
		stop.set()
		for thread in threads:
			thread.join()
		print(f'[ALL]: All threads died and joined, t+{round(time() - start)}s, restarting in {timeWaitingExitingThreads}s')
		sleep(timeWaitingExitingThreads)
		stop.clear()

if __name__ == '__main__':
	main()