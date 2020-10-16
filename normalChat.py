import datetime

class HelpChat:
	def help(self):
		print()
	def whatCanIdo(self):
		with open("#normal chat","r") as file:
			for line in file:
				line=line.strip()
				print(line)

class DateTime:
	def currentTime(self):
		time = datetime.datetime.now()
		x = " A.M."
		if time.hour>12: x = " P.M."
		time = str(time)
		time = time[11:16] + x
		return time

	def currentDate(self):
		date = str(datetime.datetime.now())
		return date[:10]
	
def wishMe():
	now = datetime.datetime.now()
	hr = now.hour
	if hr<12:
		wish="Good Morning"
	elif hr>=12 and hr<16:
		wish="Good Afternoon"
	else:
		wish="Good Evening"
	return wish


def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def chat(text):
	dt = DateTime()
	result = ""
	if isContain(text, ['good']):
		result = wishMe()		
	elif isContain(text, ['time']):
		result = "Current Time is: " + dt.currentTime()
	elif isContain(text, ['date','today','day','month']):
		result = "Today is: " + dt.currentDate()

	return result

from difflib import get_close_matches
import json
from random import choice

data = json.load(open('extrafiles/NormalChat.json', encoding='utf-8'))

def reply(query):
	if query in data:
		response =  data[query]
	else:
		query = get_close_matches(query, data.keys(), n=2, cutoff=0.5)
		if len(query)==0: return "None"
		return choice(data[query[0]])

	return choice(response)


from googletrans import Translator, LANGUAGES

def lang_translate(text,language):
	if language in LANGUAGES.values():
		translator = Translator()
		result = translator.translate(text, src='en', dest=language)
		return result
	else:
		return "None"
