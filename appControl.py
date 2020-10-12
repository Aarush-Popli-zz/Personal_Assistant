import pyscreenshot as ImageGrab
import time
import os
import subprocess
from pynput.keyboard import Key, Controller
import psutil

class SystemApps:
	def __init__(self):
		self.keyboard = Controller()

	def openApp(self, appName):
		appName = appName.replace('paint', 'mspaint')
		appName = appName.replace('wordpad', 'write')
		appName = appName.replace('word', 'write')
		appName = appName.replace('calculator', 'calc')
		try: subprocess.Popen('C:\\Windows\\System32\\'+appName[5:]+'.exe')
		except: pass

	def write(self, text):
		text = text[5:]
		for char in text:
			self.keyboard.type(char)
			time.sleep(0.02)

	def select(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('a')
		self.keyboard.release('a')
		self.keyboard.release(Key.ctrl)

	def hitEnter(self):
		self.keyboard.press(Key.enter)
		self.keyboard.release(Key.enter)

	def delete(self):
		self.keyboard.press(Key.backspace)
		self.keyboard.release(Key.enter)

	def save(self, text):
		if "don't" in text:
			self.keyboard.press(Key.right)
		else: 
			self.keyboard.press(Key.ctrl)
			self.keyboard.press('s')
			self.keyboard.release('s')
			self.keyboard.release(Key.ctrl)
		self.hitEnter()

class TabOpt:
	def __init__(self):
		self.keyboard = Controller()

	def switchTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press(Key.tab)
		self.keyboard.release(Key.tab)
		self.keyboard.release(Key.ctrl)

	def closeTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('w')
		self.keyboard.release('w')
		self.keyboard.release(Key.ctrl)

	def newTab(self):
		self.keyboard.press(Key.ctrl)
		self.keyboard.press('n')
		self.keyboard.release('n')
		self.keyboard.release(Key.ctrl)


class WindowOpt:
	def __init__(self):
		self.keyboard = Controller()

	def openWindow(self):
		self.maximizeWindow()
	
	def closeWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.f4)
		self.keyboard.release(Key.f4)
		self.keyboard.release(Key.alt_l)
	
	def minimizeWindow(self):
		for i in range(2):
			self.keyboard.press(Key.cmd)
			self.keyboard.press(Key.down)
			self.keyboard.release(Key.down)
			self.keyboard.release(Key.cmd)
			time.sleep(0.05)
	
	def maximizeWindow(self):
		self.keyboard.press(Key.cmd)
		self.keyboard.press(Key.up)
		self.keyboard.release(Key.up)
		self.keyboard.release(Key.cmd)

	def moveWindow(self, operation):
		self.keyboard.press(Key.cmd)

		if "left" in operation:
			self.keyboard.press(Key.left)
			self.keyboard.release(Key.left)
		elif "right" in operation:
			self.keyboard.press(Key.right)
			self.keyboard.release(Key.right)
		elif "down" in operation:
			self.keyboard.press(Key.down)
			self.keyboard.release(Key.down)
		elif "up" in operation:
			self.keyboard.press(Key.up)
			self.keyboard.release(Key.up)
		self.keyboard.release(Key.cmd)

	def switchWindow(self):
		self.keyboard.press(Key.alt_l)
		self.keyboard.press(Key.tab)
		self.keyboard.release(Key.tab)
		self.keyboard.release(Key.alt_l)
		

	def takeScreenShot(self):
		im = ImageGrab.grab()
		im.save('ss.png')

def isContain(text, lst):
	for word in lst:
		if word in text:
			return True
	return False

def Win_Opt(operation):
	w = WindowOpt()
	if isContain(operation, ['open']):
		w.openWindow()
	elif isContain(operation, ['close']):
		w.closeWindow()
	elif isContain(operation, ['mini']):
		w.minimizeWindow()
	elif isContain(operation, ['maxi']):
		w.maximizeWindow()
	elif isContain(operation, ['move', 'slide']):
		w.moveWindow(operation)
	elif isContain(operation, ['switch','which']):
		w.switchWindow()
	elif isContain(operation, ['screenshot','capture','snapshot']):
		w.takeScreenShot()
	return

def Tab_Opt(operation):
	t = TabOpt()
	if isContain(operation, ['new','open','another','create']):
		t.newTab()
	elif isContain(operation, ['switch','move','another','next','previous','which']):
		t.switchTab()
	elif isContain(operation, ['close','delete']):
		t.closeTab()
	else:
		return


def System_Opt(operation):
	s = SystemApps()
	if 'delete' in operation:
		s.delete()
	elif 'save' in operation:
		s.save(operation)
	elif 'type' in operation:
		s.write(operation)
	elif 'select' in operation:
		s.select()
	elif 'enter' in operation:
		s.hitEnter()
	elif isContain(operation, ['notepad','paint','calc','word']):
		s.openApp(operation)
	elif isContain(operation, ['music','video']):
		s.playMusic(operation)
	else:
		return


###############################
###########  VOLUME ###########
###############################

keyboard = Controller()
def mute():
	for i in range(50):
		keyboard.press(Key.media_volume_down)
		keyboard.release(Key.media_volume_down)

def full():
	for i in range(50):
		keyboard.press(Key.media_volume_up)
		keyboard.release(Key.media_volume_up)


def volumeControl(text):
	if 'full' in text or 'max' in text: full()
	elif 'mute' in text or 'min' in text: mute()
	elif 'incre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_up)
			keyboard.release(Key.media_volume_up)
	elif 'decre' in text:
		for i in range(5):
			keyboard.press(Key.media_volume_down)
			keyboard.release(Key.media_volume_down)

def systemInfo():
	import wmi
	c = wmi.WMI()  
	my_system_1 = c.Win32_LogicalDisk()[0]
	my_system_2 = c.Win32_ComputerSystem()[0]
	print("Total Disk Space:", round(int(my_system_1.Size)/(1024**3),2), "GB")
	print("Free Disk Space:", round(int(my_system_1.Freespace)/(1024**3),2), "GB")
	print("Manufacturer:", my_system_2.Manufacturer)
	print("Model:", my_system_2. Model)
	print("Owner:", my_system_2.PrimaryOwnerName)
	print("Number of Processors:", my_system_2.NumberOfProcessors)
	print("System Type:", my_system_2.SystemType)

def batteryInfo():
	usage = str(psutil.cpu_percent(interval=0.1))
	battery = psutil.sensors_battery()
	return usage, battery.percent

def OSHandler(query):
	if isContain(query, ['system', 'info']):
		systemInfo()
	elif isContain(query, ['cpu', 'battery']):
		return batteryInfo()
