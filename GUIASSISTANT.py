#########################
# GLOBAL VARIABLES USED # web development
#########################
rec_email, rec_phoneno = "", ""
WAEMEntry = None
ai_name = 'jarvis'.lower()
WAKE_COMMANDS = ['hello','hi','hey',ai_name,'hai','activate','google']
EXIT_COMMANDS = ['bye','exit','quit','shutdown']
WelcomeSpeech = "Hello, I'm your Personal Assistant. You can ask me any thing, and I will perform the task for you."

chatBgColor = '#12232e'
background = 'white'
textColor = 'black'
AITaskStatusLblBG = '#14A769'
KCS_IMG = 0 #light, 1 for dark
voice_id = 0 #female
ass_volume = 1 #max volume
ass_voiceRate = 200 #normal voice rate

####################################### IMPORTING MODULES ###########################################
""" User Created Modules """
try:
	import normalChat
	import math_function
	import appControl
	import webScrapping
	import game
	from userHandler import UserData
	import timer
	from FACE_UNLOCKER import clickPhoto, viewPhoto
	import dictionary
	import ToDo
	import fileHandler
except Exception as e:
	raise e

""" System Modules """
try:
	import os
	import speech_recognition as sr
	import pyttsx3
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	from tkinter import colorchooser
	from PIL import Image, ImageTk
	from time import sleep
	from threading import Thread
except Exception as e:
	print(e)

########################################## LOGIN CHECK ##############################################
try:
	user = UserData()
	user.extractData()
	ownerName = user.getName().split()[0]
except Exception as e:
	print("You're not Registered Yet !\nRun SECURITY.py file to register your face.")
	raise SystemExit


########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
	import pickle
	global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG
	setting = {'background': background,
				'textColor': textColor,
				'chatBgColor': chatBgColor,
				'AITaskStatusLblBG': AITaskStatusLblBG,
				'KCS_IMG': KCS_IMG,
				'voice_id': voice_id,
				'ass_volume': ass_volume,
				'ass_voiceRate': ass_voiceRate
			}
	if write:
		with open('userData/settings.pck', 'wb') as file:
			pickle.dump(setting, file)
		return
	try:
		with open('userData/settings.pck', 'rb') as file:
			loadSettings = pickle.load(file)
			background = loadSettings['background']
			textColor = loadSettings['textColor']
			chatBgColor = loadSettings['chatBgColor']
			AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
			KCS_IMG = loadSettings['KCS_IMG']
			voice_id = loadSettings['voice_id']
			ass_volume = loadSettings['ass_volume']
			ass_voiceRate = loadSettings['ass_voiceRate']
	except Exception as e:
		pass

if os.path.exists('userData/settings.pck')==False:
	ChangeSettings(True)

def changeTheme():
	global background, textColor, AITaskStatusLblBG, KCS_IMG
	if themeValue.get()==1:
		background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647",1
		cbl['image'] = cblDarkImg
		kbBtn['image'] = kbphDark
		settingBtn['image'] = sphDark
		AITaskStatusLbl['bg'] = AITaskStatusLblBG
	else:
		background, textColor, AITaskStatusLblBG, KCS_IMG= "white", "black", "#14A769", 0
		cbl['image'] = cblLightImg
		kbBtn['image'] = kbphLight
		settingBtn['image'] = sphLight
		AITaskStatusLbl['bg'] = AITaskStatusLblBG

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

############################################ SET UP VOICE ###########################################
try:
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[voice_id].id) #male
	engine.setProperty('volume', ass_volume)
except Exception as e:
	print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
	AITaskStatusLbl['text'] = 'Speaking...'
	if icon: Label(chat_frame, image=botIcon, bg=chatBgColor).pack(anchor='w',pady=0)
	if display: attachTOframe(text, True)
	print('\n'+ai_name.upper()+': '+text)
	engine.say(text)
	engine.runAndWait()

####################################### SET UP SPEECH TO TEXT #######################################
def record(clearChat=True, iconDisplay=True):
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
			if iconDisplay: Label(chat_frame, image=userIcon, bg=chatBgColor).pack(anchor='e',pady=0)
			attachTOframe(said)
		except Exception as e:
			print(e)
			# speak("I didn't get it, Say that again please...")
			if "connection failed" in str(e):
				speak("Your System is Offline...", True, True)
			return 'None'
	return said.lower()

def voiceMedium():
	while True:
		query = record()
		if isContain(query, EXIT_COMMANDS):
			speak('Shutting down the System. Good Bye Sir!', True, True)
			break
		if query == 'None': continue
		else: main(query.lower())
	appControl.Win_Opt('close')

###################################### TASK/COMMAND HANDLER #########################################
def isContain(txt, lst):
	for word in lst:
		if word in txt:
			return True
	return False

def main(text):

		if "project" in text:
			if isContain(text, ['make', 'create']):
				speak("What do you want to give the project name ?", True, True)
				projectName = record(False, False)
				speak(fileHandler.CreateHTMLProject(projectName.capitalize()), True)
				return

		if "create" in text and "file" in text:
			speak(fileHandler.createFile(text), True, True)
			return

		if "translate" in text:
			speak("What do you want to translate?", True, True)
			sentence = record(False, False)
			speak("Which langauage to translate ?", True)
			langauage = record(False, False)
			result = normalChat.lang_translate(sentence, langauage)
			if result=="None": speak("This langauage doesn't exists")
			else:
				speak(f"In {langauage.capitalize()} you would say:", True)
				speak(result.text, True)
			return

		if 'list' in text:
			if isContain(text, ['add', 'create', 'make']):
				speak("What do you want to add?", True, True)
				item = record(False, False)
				ToDo.toDoList(item)
				speak("Alright, I added to your list", True)
				return
			if isContain(text, ['show', 'my list']):
				items = ToDo.showtoDoList()
				attachTOframe('\n'.join(items), True)
				speak(items[0])
				return

		if isContain(text, ['battery', 'battery', 'system info']):
			result = appControl.OSHandler(text)
			if len(result)==2:
				speak(result[0], True, True)
				attachTOframe(result[1], True)
			else:
				speak(result, True, True)
			return
		if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
			result = dictionary.translate(text)
			speak(result[0], True, True)
			if result[1]=='': return
			speak(result[1], True)
			return

		if 'selfie' in text or ('click' in text and 'photo' in text):
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
			speak('Sure Sir...', True, True)
			speak('Whom do you want to send the message?', True)
			WAEMPOPUP("WhatsApp", "Phone Number")
			attachTOframe(rec_phoneno)
			speak('What is the message?', True)
			message = record(False, False)
			Thread(target=webScrapping.sendWhatsapp, args=(rec_phoneno, message,)).start()
			speak("Message is on the way. Do not move away from the screen.")
			return

		if 'email' in text:
			speak('Whom do you want to send the email?', True, True)
			WAEMPOPUP("Email", "E-mail Address")
			attachTOframe(rec_email)
			speak('What is the Subject?', True)
			subject = record(False, False)
			speak('What message you want to send ?', True)
			message = record(False, False)
			Thread(target=webScrapping.email, args=(rec_email,message,subject,) ).start()
			speak('Email has been Sended', True)
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
			if 'image' in text:
				Thread(target=showImages, args=(text,)).start()
				speak('Here are the images...', True, True)
				return
			speak(webScrapping.googleSearch(text), True, True)
			return
			
		if isContain(text, ['map', 'direction']):
			if "direction" in text:
				speak('What is your starting location?', True, True)
				startingPoint = record(False, False)
				speak('Ok Sir, Where you want to go?', True)
				destinationPoint = record(False, False)
				speak('Ok Sir, Getting Directions...', True)
				try:
					distance = webScrapping.giveDirections(startingPoint, destinationPoint)
					speak('You have to cover a distance of '+ distance, True)
				except:
					speak("I think location is not proper, Try Again!")
			else:
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
			text = record(False, False)
			if isContain(text, ["no","don't"]):
				speak('No Problem Sir')
			else:
				speak('Ok Sir, Opening browser...', True)
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
			speak('Searching...', True, True)
			speak(webScrapping.wikiResult(text), True)
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
		
		if isContain(text, ['time','date']):
			speak(normalChat.chat(text), True, True)
			return

		if 'my name' in text:
			speak('Your name is, ' + ownerName, True, True)
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

		if isContain(text, ['morning','evening','noon']) and 'good' in text:
			speak(normalChat.chat("good"), True, True)
			return
		
		result = normalChat.reply(text)
		if result != "None": speak(result, True, True)
		else:
			speak("Here's what I found on the web... ", True, True)
			webScrapping.googleSearch(text)
		

##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
	result = messagebox.askquestion('Alert', 'Are you sure you want to delete your Face Data ?')
	if result=='no': return
	messagebox.showinfo('Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
	import shutil
	shutil.rmtree('userData')

						#####################
						####### GUI #########
						#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def attachTOframe(text,bot=False):
	if bot:
		botchat = Label(chat_frame,text=text, bg='#EAEAEA', fg='#494949', justify=LEFT, wraplength=250, font=('Montserrat',12, 'bold'))
		botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)
	else:
		userchat = Label(chat_frame, text=text, bg='#23AE79', fg='white', justify=RIGHT, wraplength=250, font=('Montserrat',12, 'bold'))
		userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)

def clearChatScreen():
	for wid in chat_frame.winfo_children():
		wid.destroy()

### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
	frame.tkraise()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3 = None, None, None, None
def showImages(query):
	global img0, img1, img2, img3
	webScrapping.downloadImage(query)
	w, h = 150, 110
	#Showing Images
	imageContainer = Frame(chat_frame, bg='#EAEAEA')
	imageContainer.pack(anchor='w')

	#Opening
	img0 = Image.open('Downloads/0.jpg')
	img1 = Image.open('Downloads/1.jpg')
	img2 = Image.open('Downloads/2.jpg')
	img3 = Image.open('Downloads/3.jpg')
	#Resizing
	img0 = img0.resize((w,h), Image.ANTIALIAS)
	img1 = img1.resize((w,h), Image.ANTIALIAS)
	img2 = img2.resize((w,h), Image.ANTIALIAS)
	img3 = img3.resize((w,h), Image.ANTIALIAS)

	img0 = ImageTk.PhotoImage(img0)
	img1 = ImageTk.PhotoImage(img1)
	img2 = ImageTk.PhotoImage(img2)
	img3 = ImageTk.PhotoImage(img3)
	#Displaying
	Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
	Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
	Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
	Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)

############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
	global rec_phoneno, rec_email
	data = WAEMEntry.get()
	rec_email, rec_phoneno = data, data
	WAEMEntry.delete(0, END)
	appControl.Win_Opt('close')
def send(e):
	sendWAEM()

def WAEMPOPUP(Service='None', rec='Reciever'):
	global WAEMEntry
	PopUProot = Tk()
	PopUProot.title(f'{Service} Service')
	PopUProot.attributes('-toolwindow', True)
	PopUProot.configure(bg='white')
	w_width, w_height = 410, 200
	s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
	x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
	PopUProot.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
	Label(PopUProot, text=f'Reciever {rec}', font=('Arial', 16), bg='white').pack(pady=(20, 10))
	WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=('Arial', 12), bg='#DCDCDC', width=30)
	WAEMEntry.pack()
	WAEMEntry.focus()

	SendBtn = Button(PopUProot, text='Send', font=('Arial', 12), relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
	SendBtn.pack(pady=20, ipadx=10)
	PopUProot.bind('<Return>', send)
	PopUProot.mainloop()

######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
	global chatBgColor
	myColor = colorchooser.askcolor()
	if myColor[1] is None: return
	chatBgColor = myColor[1]
	colorbar['bg'] = chatBgColor
	chat_frame['bg'] = chatBgColor
	root1['bg'] = chatBgColor
	ChangeSettings(True)

chatMode = 1
def changeChatMode():
	global chatMode
	if chatMode==1:
		VoiceModeFrame.pack_forget()
		TextModeFrame.pack(fill=BOTH)
		chatMode=0
	else:
		TextModeFrame.pack_forget()
		VoiceModeFrame.pack(fill=BOTH)
		chatMode=1
############################################## MAIN GUI #############################################

if __name__ == '__main__':
	# ChangeSettings()

	root = Tk()
	root.title('F.R.I.D.A.Y')
	rootIcon = PhotoImage(file='extrafiles/images/assistant2.png')
	root.iconphoto(False, rootIcon)
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
	# userField.pack(pady)
	# root.bind('<Return>', enter)

	bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
	bottomFrame1.pack(fill=X, side=BOTTOM)
	VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	VoiceModeFrame.pack(fill=BOTH)
	TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
	TextModeFrame.pack(fill=BOTH)

	# VoiceModeFrame.pack_forget()
	# TextModeFrame.pack_forget()

	cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
	cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
	if KCS_IMG==1: cblimage=cblDarkImg
	else: cblimage=cblLightImg
	cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
	cbl.pack(pady=17)
	AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline', fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
	AITaskStatusLbl.place(x=140,y=32)
	
	#Settings Button
	sphLight = PhotoImage(file = "extrafiles/images/setting.png")
	sphLight = sphLight.subsample(2,2)
	sphDark = PhotoImage(file = "extrafiles/images/setting1.png")
	sphDark = sphDark.subsample(2,2)
	if KCS_IMG==1: sphimage=sphDark
	else: sphimage=sphLight
	settingBtn = Button(VoiceModeFrame,image=sphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf",command=lambda: raise_frame(root2))
	settingBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	
	#Keyboard Button
	kbphLight = PhotoImage(file = "extrafiles/images/keyboard.png")
	kbphLight = kbphLight.subsample(2,2)
	kbphDark = PhotoImage(file = "extrafiles/images/keyboard1.png")
	kbphDark = kbphDark.subsample(2,2)
	if KCS_IMG==1: kbphimage=kbphDark
	else: kbphimage=kbphLight
	kbBtn = Button(VoiceModeFrame,image=kbphimage,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	kbBtn.place(x=25, y=30)

	#Mic
	micImg = PhotoImage(file = "extrafiles/images/mic.png")
	micImg = micImg.subsample(2,2)
	micBtn = Button(TextModeFrame,image=micImg,height=30,width=30, bg='#dfdfdf',borderwidth=0,activebackground="#dfdfdf", command=changeChatMode)
	micBtn.place(relx=1.0, y=30,x=-20, anchor="ne")	
	#Text Field
	TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
	UserFieldLBL = Label(TextModeFrame, fg='white', image=TextFieldImg, bg='#dfdfdf')
	UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
	UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=('Montserrat', 16), bd=6, width=22, relief=FLAT)
	UserField.place(x=20, y=30)
	UserField.focus()
	UserField.insert(0, "Ask me anything...")
	
	#User and Bot Icon
	userIcon = PhotoImage(file="extrafiles/images/owner.png")
	userIcon = userIcon.subsample(2,2)
	botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
	botIcon = botIcon.subsample(2,2)
	

	###########################
	########  SETTINGS  #######
	###########################

	settingsLbl = Label(root2, text='Settings', font=('Arial Bold', 15), bg=background, fg=textColor)
	settingsLbl.pack(pady=10)
	separator = ttk.Separator(root2, orient='horizontal')
	separator.pack(fill=X)
	#User Photo
	img = PhotoImage(file = "extrafiles/images/user2.png")
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
	cimg = PhotoImage(file = "extrafiles/images/colorchooser.png")
	cimg = cimg.subsample(3,3)
	colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
	colorbar.place(x=150, y=180)
	Button(settingsFrame, image=cimg, relief=FLAT, command=getChatColor).place(x=261, y=180)

	backBtn = Button(settingsFrame, text='   Back   ', font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda:raise_frame(root1))
	clearFaceBtn = Button(settingsFrame, text='   Clear Facial Data   ', font=('Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
	backBtn.place(x=5, y=250)
	clearFaceBtn.place(x=120, y=250)


	try:
		# pass
		Thread(target=voiceMedium).start()
	except:
		pass
	try:
		pass
		# Thread(target=webScrapping.dataUpdate).start()
	except Exception as e:
		print('System is Offline...')
	
	raise_frame(root1)
	root.mainloop()
