



import os

import jk_json

from .simple_encrypter import encryptPwd, decryptPwd, isPwdEncrypted





class OneSlotPasswordProvider(object):

	def __init__(self, thePassword:str):
		self.__pwd = ""

		self.setPassword(thePassword)
	#

	def __call__(self, machineName:str, loginName:str) -> str:
		return self.__pwd
	#

	def storePwd(self, filePath:str):
		with open(filePath, "w") as f:
			f.write(encryptPwd(self.__pwd))
	#

	def loadPwd(self, filePath:str):
		with open(filePath, "r") as f:
			self.__pwd = decryptPwd(f.read())
	#

	def setPassword(self, thePassword:str):
		assert isinstance(thePassword, str)
		assert thePassword

		if isPwdEncrypted(thePassword):
			thePassword = decryptPwd(thePassword)

		self.__pwd = thePassword
	#

	def getEncryptedPassword(self):
		return encryptPwd(self.__pwd)
	#

#

