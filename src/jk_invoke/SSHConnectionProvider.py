


import time
import os

import fabric

from jk_testing import Assert
from jk_utils import ChModValue

from .AbstractInvoker import AbstractInvoker
from .CommandResult import CommandResult
from .CachedPasswordProvider import CachedPasswordProvider




class SSHConnectionProvider(object):

	def __init__(self, hostName:str, port:int, userName:str, passwordProvider):
		assert isinstance(hostName, str)
		assert isinstance(port, int)
		assert isinstance(userName, str)
		assert callable(passwordProvider)

		self.__hostName = hostName
		self.__port = port
		self.__userName = userName
		self.__passwordProvider = passwordProvider if isinstance(passwordProvider, CachedPasswordProvider) else CachedPasswordProvider(passwordProvider)

		self.__c = None
	#

	def connect(self) -> fabric.Connection:
		if self.__c is None:
			pwd = self.__passwordProvider(self.__hostName, self.__userName)
			config = fabric.Config(overrides={'sudo': {'password': pwd}})
			self.__c = fabric.Connection(self.__hostName, self.__userName, self.__port, config=config, connect_kwargs={"password": pwd})

			r = self.__c.run(
				self._encodeSSHCmdLine("/bin/echo", "foo  \"  \"  bar"),
				hide=True)
			Assert.isTrue(self.__c.is_connected)
			Assert.isEqual(r.exited, 0)
			Assert.isEqual(r.stderr, "")
			Assert.isEqual(r.stdout, "foo  \"  \"  bar\n")

		return self.__c
	#

	def _encodeSSHCmdLineArg(self, cmdArg:str) -> str:
		return "'" + cmdArg.replace("'", "\\'") + "'"
	#

	def _encodeSSHCmdLine(self, *args) -> str:
		if not args:
			raise Exception("No arguments specified!")

		ret = [ args[0] ]
		for arg in args[1:]:
			ret.append(self._encodeSSHCmdLineArg(arg))
		return " ".join(ret)
	#

#





