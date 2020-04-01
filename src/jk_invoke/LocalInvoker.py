


import time
import os
import pwd
import grp
import subprocess

import fabric

from jk_testing import Assert
from jk_utils import ChModValue

from .AbstractInvoker import AbstractInvoker
from .CommandResult import CommandResult
from .CachedPasswordProvider import CachedPasswordProvider
from .SSHConnectionProvider import SSHConnectionProvider
from .RemoteSudoInvoker import RemoteSudoInvoker




class LocalInvoker(AbstractInvoker):

	def __init__(self, passwordProvider = None, localSSHPort:int = None):
		if passwordProvider is not None:
			assert callable(passwordProvider)
			if localSSHPort is None:
				localSSHPort = self.__retrieveLocalSSHPortFromSSHCfg()
			else:
				assert isinstance(localSSHPort, int)

			self.__userID = os.getuid()
			self.__userName = pwd.getpwuid(self.__userID).pw_name
			self.__groupID = os.getgid()
			self.__groupName = grp.getgrgid(self.__groupID).gr_name

			self.__cprov = SSHConnectionProvider("localhost", localSSHPort, self.__userName, passwordProvider)

		else:
			self.__cprov = None

		self.__sudoInoker = None
	#

	def __retrieveLocalSSHPortFromSSHCfg(self):
		with open("/etc/ssh/sshd_config", "r") as f:
			for line in f.readlines():
				if line.startswith("Port "):
					return int(line[5:].strip())
	#

	def runCmd(self, cmd:str, cmdArgs:list = None) -> CommandResult:
		dataToPipeAsStdIn = None

		s = [ cmd ]
		if cmdArgs:
			s.extend(cmdArgs)
		elif cmdArgs is None:
			cmdArgs = []

		t = time.time()
		if dataToPipeAsStdIn:
			p = subprocess.Popen(s, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			p.stdin.write(dataToPipeAsStdIn)
		else:
			p = subprocess.Popen(s, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=None)
		(stdout, stderr) = p.communicate()
		duration = time.time() - t

		sStdOutData = stdout.decode("utf-8")
		sStdErrData = stderr.decode("utf-8")

		return CommandResult(cmd, cmdArgs, sStdOutData, sStdErrData, p.returncode, duration)
	#

	def readTextFile(self, absFilePath:str) -> str:
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)

		with open(absFilePath, "r") as f:
			return f.read()
	#

	def writeTextFile(self, absFilePath:str, textContent:str):
		assert isinstance(absFilePath, str)
		assert os.path.isabs(absFilePath)
		assert isinstance(textContent, str)

		with open(absFilePath, "w") as f:
			return f.write(textContent)
	#

	def sudo(self) -> AbstractInvoker:
		if self.__sudoInoker is None:
			if self.__cprov is None:
				raise Exception("This invoker has no password provider and therefore does not support sudo!")
			self.__sudoInoker = RemoteSudoInvoker(self.__cprov)
		return self.__sudoInoker
	#

#








