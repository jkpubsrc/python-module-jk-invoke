



import jk_pwdinput




class CachedPasswordProvider(object):

	def __init__(self, nested):
		assert callable(nested)

		self.__nested = nested
		self.__cachedPwd = None
		self.__machineName = None
		self.__loginName = None
	#

	def __call__(self, machineName:str, loginName:str) -> str:
		if (self.__cachedPwd is None) or (self.__machineName != machineName) or (self.__loginName != loginName):
			self.__cachedPwd = self.__nested(machineName, loginName)
			self.__machineName = machineName
			self.__loginName = loginName
		return self.__cachedPwd
	#

#

