


import time
import os

import fabric

from jk_testing import Assert
from jk_utils import ChModValue

from .AbstractInvoker import AbstractInvoker
from .CommandResult import CommandResult
from .RemoteSudoInvoker import RemoteSudoInvoker
from .SSHConnectionProvider import SSHConnectionProvider





class RemoteInvoker(AbstractInvoker):

	def __init__(self, hostName:str, port:int, userName:str, passwordProvider):
		self.__cprov = SSHConnectionProvider(hostName, port, userName, passwordProvider)

		self.__sudoInoker = None
	#

	def runCmd(self, cmd:str, *cmdArgs) -> CommandResult:
		c = self.__cprov.connect()

		t = time.time()
		r = c.run(
			self._encodeSSHCmdLine(cmd, *cmdArgs),
			hide=True)
		duration = time.time() - t

		return CommandResult(cmd, cmdArgs, r.stdout, r.stderr, r.exited, duration)
	#

	def readTextFile(self, absFilePath:str) -> str:
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)

		c = self.__cprov.connect()

		localTargetDirPath = self._createLocalPrivateTempDir()
		localTargetFilePath = os.path.join(localTargetDirPath, self._createRandomFileName())
		try:
			c.get(
				absFilePath,
				localTargetFilePath
				)

			with open(localTargetFilePath, "r") as f:
				content = f.read()

			return content

		finally:
			if localTargetFilePath and os.path.exists(localTargetFilePath):
				os.unlink(localTargetFilePath)
			if localTargetDirPath and os.path.exists(localTargetDirPath):
				os.rmdir(localTargetDirPath)
	#

	def writeTextFile(self, absFilePath:str, textContent:str, chmodValue:ChModValue = None):
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)
		assert isinstance(textContent, str)

		c = self.__cprov.connect()

		localTmpFilePath = self._generateLocalPrivateTempFile(textContent, chmodValue)
		try:
			t = time.time()
			c.put(
				localTmpFilePath,
				absFilePath,
				True
			)
			duration = time.time() - t

		finally:
			if localTmpFilePath and os.path.exists(localTmpFilePath):
				os.unlink(localTmpFilePath)
	#

	def sudo(self) -> AbstractInvoker:
		if self.__sudoInoker is None:
			self.__sudoInoker = RemoteSudoInvoker(self.__cprov)
		return self.__sudoInoker
	#

#








