# PyFetchFbMedia (Alpha v0.2)
![alt text](https://img.shields.io/badge/python-%3E%3D3.6-brightgreen "Python >=3.6")
![alt text](https://img.shields.io/badge/licence-GPL3-blue "licence GPL 3")

PyFetchFbMedia is a small project that gets pictures and videos that is sent on Facebook messager with python without leveraging the Facebook API, but with Firefox's geckodriver. It can fetch media from given threads without opening upread ones, waiting util they are read.

## Usage

* If you are using firefox copy the cookies sqlite db to the project folder (In Linux they are under ~/.mozilla/firefox/{profile}/cookies.sqlite) and edit `makeCookiesFromFirefox.py` value `cookie_name` to whatever you want to
#### OR
* Copy the cookies 'value' and 'expiry' values from your browser to manualMakeCookies.py and run ```python3 manualMakeCookies.py``` and the value `cookie_name` to whatever you want to
#### OR
* Use the login(username, password) function of the Class. ***Not recommended***, if you are using a different ip from last login Facebook will ask for more information.
* Edit ```settings.py``` like 
```python
a = {
	'name' : 'MyProfile1',
	'people' : ['conversationToWatch1', 'conversationToWatch2', 'conversationToWatch3'],
	'headless' : True,
	'debug' : False,
	'override' : False
	}
# For multiple profiles
b = {
	'name' : 'MyProfile2',
	'people' : ['conversationToWatch4', 'conversationToWatch5', 'conversationToWatch6'],
	'headless' : True,
	'debug' : False,
	'override' : False
	}
name = [a,b]
```

* ```python3 example.py```
* If you run it on a server it is best to be run through a tmux session

## Requierements

* Python 3.6 and above
* Geckodriver

## Instalation

* ```git clone``` the project
* ```pip3 install -r requirements.txt```
* Done

## Comments

* If you don't care about opening unread threads set override to true.
* If your profile is in an olther language than English or Greek, add the equivalent of 'Conversation List' in your language to PyFetchFbMedia.py in the variable `self.convLists` at line 40.