class UserData:
	def __init__(self):
		self.name = 'None'
		self.gender = 'None'
		self.dob = 'None'

	def extractData(self):
		with open('userData/userData.dat', 'r') as file:
			self.name = file.readline().strip()
			self.gender = file.readline().strip()
			self.dob = file.readline().strip()

	def getName(self):
		return self.name

	def getGender(self):
		return self.gender

	def getDOB(self):
		return self.dob

	def updateData(self, name, gender, dob='None'):
		with open('userData/userData.dat', 'w') as file:
			file.write(str(name)+'\n')
			file.write(str(gender)+'\n')
			file.write(str(dob)+'\n')
