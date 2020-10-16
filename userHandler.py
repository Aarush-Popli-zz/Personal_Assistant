import pickle

class UserData:
	def __init__(self):
		self.name = 'None'
		self.gender = 'None'

	def extractData(self):
		with open('userData/userData.pck', 'rb') as file:
			details = pickle.load(file)
			self.name, self.gender = details['name'], details['gender']

	def updateData(self, name, gender):
		with open('userData/userData.pck', 'wb') as file:
			details = {'name': name, 'gender': gender}
			pickle.dump(details, file)

	def getName(self):
		return self.name

	def getGender(self):
		return self.gender
