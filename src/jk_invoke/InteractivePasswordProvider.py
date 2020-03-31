



import jk_pwdinput




class InteractivePasswordProvider(object):

	def __init__(self, enterPasswordMsg:str = "Please enter password for {0}@{1}: "):
		self.enterPasswordMsg = enterPasswordMsg
	#

	def __call__(self, machineName:str, loginName:str) -> str:
		pwd = jk_pwdinput.readpwd(
			self.enterPasswordMsg.format(
				loginName,
				machineName
			)
		)
		if not pwd:
			raise Exception("No password specified!")
		return pwd
	#

#

