#########################
# GLOBAL VARIABLES USED #
#########################
rec_email = ""
emailEntry = None
chatBgColor = 'red'
background = 'black'
textColor = 'white'
ai_name = 'jarvis'.lower()
WAKE_COMMANDS = ['hello','hi','hey',ai_name,'hai','activate','google']
EXIT_COMMANDS = ['bye','exit','quit','shutdown']
WelcomeSpeech = "Hello, I'm your Personal Assistant. You can ask me any thing, and I will perform the task for you."
voice_id = 0 #male
ass_volume = 1
ass_voiceRate = 200

'''User Created Modules'''
try:
	import normalChat
	import appControl
	import webScrapping
	import game
	import math_function
	from userHandler import UserData
	import timer
	from FACE_UNLOCKER import clickPhoto, viewPhoto
except Exception as e:
	raise e

##############################################
try:
	user = UserData()
	user.extractData()
	ownerName = user.getName().split()[0]
except Exception as e:
	print("You're not Registered Yet !\nRun SECURITY.py file to register your face.")
	raise SystemExit
###############################################

'''System Modules'''
try:
	import os
	import speech_recognition as sr
	import pyttsx3
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from time import sleep
	from threading import Thread
except Exception as e:
	print(e)


########################################################################################################
def ChangeSettings(write=False):
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate
	if write:
		with open('userData/settings.dat', 'w') as file:
			file.write(str(background)+'\n')
			file.write(str(textColor)+'\n')
			file.write(str(chatBgColor)+'\n')
			file.write(str(voice_id)+'\n')
			file.write(str(ass_volume)+'\n')
			file.write(str(ass_voiceRate)+'\n')
		return
	try:
		with open('userData/settings.dat', 'r') as file:
			background = file.readline().strip()
			textColor = file.readline().strip()
			chatBgColor = file.readline().strip()
			voice_id = int(file.readline().strip())
			ass_volume = float(file.readline().strip())
			ass_voiceRate = int(file.readline().strip())
	except Exception as e:
		pass

if os.path.exists('userData/settings.dat')==False:
	ChangeSettings(True)


def changeTheme():
	global background, textColor
	if themeValue.get()==1:
		background, textColor = "black", "white"
	else:
		background, textColor = "white", "black"

	root['bg'], root2['bg'] = background, background
	settingsFrame['bg'] = background
	settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl['fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
	settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl['bg'], chooseChatLbl['bg'] = background, background, background, background, background, background, background, background
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
	ChangeSettings(True)

def changeVoice(e):
	global voice_id
	voice_id=0
	if assVoiceOption.get()=='Male': voice_id=1
	engine.setProperty('voice', voices[voice_id].id)
	ChangeSettings(True)

def changeVolume(e):
	global ass_volume
	ass_volume = volumeBar.get() / 100
	engine.setProperty('volume', ass_volume)
	ChangeSettings(True)

def changeVoiceRate(e):
	global ass_voiceRate
	temp = voiceOption.get()
	if temp=='Very Low': ass_voiceRate = 100
	elif temp=='Low': ass_voiceRate = 150
	elif temp=='Fast': ass_voiceRate = 250
	elif temp=='Very Fast': ass_voiceRate = 300
	else: ass_voiceRate = 200
	print(ass_voiceRate)
	engine.setProperty('rate', ass_voiceRate)
	ChangeSettings(True)

ChangeSettings()

######################################################################################################

try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[voice_id].id) #male
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)

##################################################################################################
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg='#EAEAEA', fg='#494949', justify=LEFT, wraplength=250, font=('Arial Bold',12))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg='#23AE79', fg='white', justify=RIGHT, wraplength=250, font=('Arial Bold',12))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def isHaving(text,list):
	for word in list:
		if word in text:
			return True
	return False

def raise_frame(frame):
	frame.tkraise()

############################################################################################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	engine.say(text)
	engine.runAndWait()

def record(clearChat=True):
	print('\nListening...')
	AITaskStatusLbl['text'] = 'Listening...'
	r = sr.Recognizer()
	r.dynamic_energy_threshold = False
	r.energy_threshold = 4000
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
		said = ""
		try:
			AITaskStatusLbl['text'] = 'Processing...'
			said = r.recognize_google(audio)
			print(f"\nUser said: {said}")
			if clearChat:
				clearChatScreen()
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Your System is Offline...", True, True)
			return 'None'
	return said.lower()

def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):

		if 'click' in text and 'photo' in text:
			speak('Sure Sir...', True, True)
			clickPhoto()
			speak('Do you want to view your clicked photo?', True)
			query = record(False)
			if isContain(query, ['yes', 'sure', 'yeah', 'show me']):
				Thread(target=viewPhoto).start()
			else:
				speak('No Problem Sir', True, True)
			return

		if 'volume' in text:
			appControl.volumeControl(text)
			Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)		
			attachTOframe('Volume Settings Changed', True)
			return
			
		if isContain(text, ['timer', 'countdown']):
			Thread(target=timer.startTimer, args=(text,)).start()
			speak('Ok, Timer Started!', True, True)
			return
	
		if 'whatsapp' in text:
			return
			# webScrapping.sendWhatsapp

		if 'email' in text:
			speak('Whom do you want to send the email?', True, True)
			Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			emailPOPUP()
			attachTOframe(rec_email)
			speak('What is the Subject?', True, True)
			subject = record(False)
			speak('What message you want to send ?', True, True)
			message = record(False)
			Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
			speak('Email has been Sended', True, True)
			return

		if isContain(text, ['covid','virus']):
			result = webScrapping.covid(text)
			if 'str' in str(type(result)):
				speak(result, True, True)
				return
			speak(result[0], True, True)
			result = '\n'.join(result[1])
			attachTOframe(result, True)
			return

		if isContain(text, ['youtube','video']):
			speak('Ok Sir, here a video for you...', True, True)
			try:
				speak(webScrapping.youtube(text), True)
			except Exception as e:
				speak("Desired Result Not Found", True)
			return

		if isContain(text, ['search', 'image', 'show the']):
			speak(webScrapping.googleSearch(text), True, True)
			return
			
		if isContain(text, ['map']):
			webScrapping.maps(text)
			speak('Here you go...', True, True)
			return

		if isContain(text, ['math', '+', '-', 'binary']):
			try:
				speak(('Result is: ' + math_function.perform(text)), True, True)
			except Exception as e:
				return
			return

		if "joke" in text:
			speak('Here is a joke...', True, True)
			speak(webScrapping.jokes(), True)
			return

		if isContain(text, ['news']):
			speak('Getting the latest news...', True, True)
			headlines,headlineLinks = webScrapping.latestNews(2)
			for head in headlines: speak(head, True)
			speak('Do you want to read the full news?', True)
			text = record(False)
			if isContain(text, ["no","don't"]):
				speak('No Problem Sir')
			else:
				speak('Ok Sir, Opening browser...', True, True)
				webScrapping.openWebsite('https://indianexpress.com/latest-news/')
				speak("You can now read the full news from this website.")
			return

		if isContain(text, ['weather']):
			speak(webScrapping.weather(), True, True)
			return

		if isContain(text, ['screenshot']):
			Thread(target=appControl.Win_Opt, args=('screenshot',)).start()
			speak("Screen Shot Taken", True, True)
			return

		if isContain(text, ['window','close that']):
			appControl.Win_Opt(text)
			return

		if isContain(text, ['tab']):
			appControl.Tab_Opt(text)
			return

		if isContain(text, ['setting']):
			raise_frame(root2)
			clearChatScreen()
			return

		if isContain(text, ['open','type','save','delete','select','enter']):
			appControl.System_Opt(text)
			return

		if isContain(text, ['wiki', 'who is']):
			speak('Searching Wikipedia...', True, True)
			speak(webScrapping.wikiResult(text), True)
			return

		
		if isContain(text, ['voice']):
			global voice_id
			try:
				if 'female' in text: voice_id = 0
				elif 'male' in text: voice_id = 1
				else:
					if voice_id==0: voice_id=1
					else: voice_id=0
				engine.setProperty('voice', voices[voice_id].id)
				ChangeSettings(True)
				speak("Hello Sir, I have changed my voice. How may I help you?", True, True)
				assVoiceOption.current(voice_id)
			except Exception as e:
				print(e)
			return
		
		if isContain(text, ['hello','good','how are you','hai','morning','evening','noon']):
			if isContain(text, ["good"]):
				speak(normalChat.chat("good"), True, True)
				return
			speak('Hello Sir, How are you ?', True, True)
			return
		
		if isContain(text, ['game']):
			speak("Which game do you want to play?", True, True)
			attachTOframe(game.showGames(), True)
			text = record(False)
			if text=="None":
				speak("Didn't understand what you say?", True, True)
				return
			if 'online' in text:
				speak("Ok Sir, Let's play some online games", True, True)
				webScrapping.openWebsite('https://www.agame.com/games/mini-games/')
				return
			if isContain(text, ["don't", "no", "cancel", "back", "never"]):
				speak("No Problem Sir, We'll play next time.", True, True)
			else:
				speak("Ok Sir, Let's Play " + text, True, True)
				os.system(f"python -c \"import game; game.play('{text}')\"")
			return

		if isContain(text, ['coin','dice','toss','roll','die']):
			speak("Ok Sir", True, True)
			speak(game.play(text), True)
			return
		
		if isContain(text, ['time','date','day','today','month']):
			speak(normalChat.chat(text), True, True)
			return

		if 'my name' in text:
			speak('Your name is, ' + ownerName, True, True)
			return

		speak('Result Not Found', True, True)


def voiceMedium():
	while True:
		query = record()
		if isContain(query, EXIT_COMMANDS):
			speak('Shutting down the System. Good Bye Sir!', True, True)
			break
		if query == 'None': continue
		else: main(query.lower())
	appControl.Win_Opt('close')

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

'''
def enter(event):
	text = userField.get()
	userField.delete(0, END)
	if text!="":
		attachTOframe(text)
		if 'clear' in text:
			clearChatScreen()
		else: main(text)
'''
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Are you sure you want to delete your Face Data ?')
	if result=='no': return
	messagebox.showinfo('Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
	import shutil
	shutil.rmtree('userData')

						#####################
						####### GUI #########
						#####################

def sendEmail1():
	global rec_email
	rec_email = emailEntry.get()
	emailEntry.delete(0, END)
	appControl.Win_Opt('close')

def sendEmail2(e):
	sendEmail1()

def emailPOPUP():
	global emailEntry
	emailroot = Tk()
	emailroot.title('Email Service')
	emailroot.attributes('-toolwindow', True)
	emailroot.configure(bg='white')
	w_width, w_height = 410, 200
	s_width, s_height = emailroot.winfo_screenwidth(), emailroot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	emailroot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(emailroot, text='Reciever Email Address', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	emailEntry = Entry(emailroot, bd=10, relief=FLAT, font=('Arial', 12), bg='#DCDCDC', width=30)
	emailEntry.pack()
	emailEntry.focus()

	SendBtn = Button(emailroot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendEmail1)
	SendBtn.pack(pady=20, ipadx=10)
	emailroot.bind('<Return>', sendEmail2)
	emailroot.mainloop()

def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

if __name__ == '__main__':
	# ChangeSettings()

	root = Tk()
	root.title('ASSISTANT')
	w_width, w_height = 400, 650
	s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	root.configure(bg=background)
	# root.resizable(width=False, height=False)
	root.pack_propagate(0)

	root1 = Frame(root, bg=chatBgColor)
	root2 = Frame(root, bg=background)

	for f in (root1, root2):
		f.grid(row=0, column=0, sticky='news')	
	
	################################
	########  CHAT SCREEN  #########
	################################

	#Chat Frame
	chat_frame = Frame(root1, width=380,height=550,bg=chatBgColor)
	chat_frame.pack(padx=10)
	chat_frame.pack_propagate(0)

	# userField = Entry(root1, bd=10, font=('Arial',15),fg=boxFG,width=35,relief=FLAT, bg=boxBG,insertbackground="black")
	# userField.focus_set()
	# userField.pack(side=BOTTOM)
	# root.bind('<Return>', enter)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)

	cbl = PhotoImage(file='extrafiles/centralButton.png')
	Label(bottomFrame1, fg='white', image=cbl, bg='#dfdfdf').pack(pady=17)
	AITaskStatusLbl = Label(bottomFrame1, text='    Offline', fg='white', bg='#14A769', font=('Arial', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sph = PhotoImage(file = "extrafiles/setting3.png")
	sph = sph.subsample(2,2)
	settingBtn = Button(bottomFrame1,image=sph,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbph = PhotoImage(file = "extrafiles/keyboard.png")
	kbph = kbph.subsample(2,2)
	kbBtn = Button(bottomFrame1,image=kbph,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",)
	kbBtn.place(x=25, y=30)

	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/owner.png")
	userIcon = userIcon.subsample(2,2)
	botIcon = PhotoImage(file="extrafiles/assistant.png")
	botIcon = botIcon.subsample(3,3)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	img = PhotoImage(file = "extrafiles/user.png")
	img = img.subsample(2,2)
	userPhoto = Label(root2, image=img, bg=background)
	userPhoto.pack(pady=(20, 5))

	#Username
	userName = Label(root2, text=ownerName, font=('Arial', 12), fg=textColor, bg=background)
	userName.pack()

	#Settings Frame
	settingsFrame = Frame(root2, width=300, height=300, bg=background)
	settingsFrame.pack(pady=20)

	assLbl = Label(settingsFrame, text='Assistant Voice', font=('Arial', 13), fg=textColor, bg=background)
	assLbl.place(x=0, y=20)
	n = StringVar()
	assVoiceOption = ttk.Combobox(settingsFrame, values=('Female', 'Male'), font=('Arial', 13), width=13, textvariable=n)
	assVoiceOption.current(voice_id)
	assVoiceOption.place(x=150, y=20)
	assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

	voiceRateLbl = Label(settingsFrame, text='Voice Rate', font=('Arial', 13), fg=textColor, bg=background)
	voiceRateLbl.place(x=0, y=60)
	n2 = StringVar()
	voiceOption = ttk.Combobox(settingsFrame, font=('Arial', 13), width=13, textvariable=n2)
	voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
	voiceOption.current(ass_voiceRate//50-2) #100 150 200 250 300
	voiceOption.place(x=150, y=60)
	voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)
	
	volumeLbl = Label(settingsFrame, text='Volume', font=('Arial', 13), fg=textColor, bg=background)
	volumeLbl.place(x=0, y=105)
	volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16, highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
	volumeBar.set(int(ass_volume*100))
	volumeBar.place(x=150, y=85)



	themeLbl = Label(settingsFrame, text='Theme', font=('Arial', 13), fg=textColor, bg=background)
	themeLbl.place(x=0,y=143)
	themeValue = IntVar()
	s = ttk.Style()
	s.configure('Wild.TRadiobutton', background=background, foreground=textColor)
	darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme)
	darkBtn.place(x=150,y=145)
	lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue, style='Wild.TRadiobutton', command=changeTheme)
	lightBtn.place(x=230,y=145)

	chooseChatLbl = Label(settingsFrame, text='Chat Background', font=('Arial', 13), fg=textColor, bg=background)
	chooseChatLbl.place(x=0,y=180)
	cimg = PhotoImage(file = "extrafiles/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Back   ', font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Clear Facial Data   ', font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)

	raise_frame(root1)

	try:
		# pass
		Thread(target=voiceMedium).start()
	except:
		pass
	try:
		# pass
		Thread(target=webScrapping.dataUpdate).start()
	except Exception as e:
		print('System is Offline...')
	root.mainloop()