


import time
import os

import fabric

from jk_testing import Assert
from jk_utils import ChModValue

from .AbstractInvoker import AbstractInvoker
from .CommandResult import CommandResult
from .SSHConnectionProvider import SSHConnectionProvider




class RemoteSudoInvoker(AbstractInvoker):

	def __init__(self, cprov:SSHConnectionProvider):
		assert isinstance(cprov, SSHConnectionProvider)

		self.__cprov = cprov
	#

	def isSudo(self) -> bool:
		return False
	#

	def __filterSSHStdErr(self, stdErr:str) -> str:
		if stdErr.startswith("[sudo] "):
			lines = stdErr.split("\n")
			return "\n".join(lines[1:])
		else:
			return stdErr
	#

	def runCmd(self, cmd:str, *cmdArgs) -> CommandResult:
		c = self.__cprov.connect()

		t = time.time()
		r = c.sudo(
			self._encodeSSHCmdLine(cmd, *cmdArgs),
			hide=True)
		stdErr = self.__filterSSHStdErr(r.stderr)
		duration = time.time() - t

		return CommandResult(cmd, cmdArgs, r.stdout, stdErr, r.exited, duration)
	#

	def readTextFile(self, absFilePath:str) -> str:
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)

		c = self.__cprov.connect()

		t = time.time()
		r = c.sudo(
			self._encodeSSHCmdLine("/bin/cat", absFilePath),
			hide=True)
		stdErr = self.__filterSSHStdErr(r.stderr)
		duration = time.time() - t

		assert r.exited == 0
		assert not stdErr

		return r.stdout
	#

	def writeTextFile(self, absFilePath:str, textContent:str, chModValue:ChModValue = None):
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)
		assert isinstance(textContent, str)

		if chModValue is None:
			chModValue = ChModValue(userR=True, userW=True)
		else:
			chModValue = ChModValue.create(chModValue)

		c = self.__cprov.connect()

		localTmpFilePath = self._generateLocalPrivateTempFile(textContent)

		remoteTmpDirPath = "/tmp/" + self._createRandomFileName()
		remoteTmpFilePath = remoteTmpDirPath + "/" + self._createRandomFileName()

		try:
			t = time.time()

			# step 1: make target directory
			r = c.run(
				self._encodeSSHCmdLine("/bin/mkdir", remoteTmpDirPath, "-m", "0700"),
				hide=True)
			assert r.exited == 0

			# step 2: store file in target directory
			c.put(
				localTmpFilePath,
				remoteTmpFilePath,
				True)

			# step 3: chmod file
			r = c.run(
				self._encodeSSHCmdLine("/bin/chmod", chModValue.toStrChMod(), remoteTmpFilePath),
				hide=True)
			assert r.exited == 0

			# step 4: change ownership to root:root
			r = c.sudo(
				self._encodeSSHCmdLine("/bin/chown", "root:root", remoteTmpFilePath),
				hide=True)
			assert r.exited == 0

			# step 5: move file to final target
			r = c.sudo(
				self._encodeSSHCmdLine("/bin/mv", remoteTmpFilePath, absFilePath),
				hide=True)
			assert r.exited == 0

			# step 6: remove target directory
			r = c.run(
				self._encodeSSHCmdLine("/bin/rmdir", remoteTmpDirPath),
				hide=True)
			assert r.exited == 0

			duration = time.time() - t

		finally:
			if localTmpFilePath and os.path.exists(localTmpFilePath):
				os.unlink(localTmpFilePath)
	#

#








