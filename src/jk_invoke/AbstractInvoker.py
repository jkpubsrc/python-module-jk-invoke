


import os
import time
import random

from jk_testing import Assert
from jk_utils import ChModValue

from .CommandResult import CommandResult





class AbstractInvoker(object):

	def __init__(self):
		pass
	#

	def isSudo(self) -> bool:
		return False
	#

	def runCmd(self, cmd:str, cmdArgs:list = None) -> CommandResult:
		raise Exception()
	#

	def readTextFile(self, absFilePath:str) -> str:
		raise Exception()
	#

	def writeTextFile(self, absFilePath:str, textContent:str):
		raise Exception()
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

	def _createRandomFileName(self) -> str:
		t = int(time.time()*1000000000)
		return "x_" + str(t) + "-" + str(random.randint(0, 1000000000)) + ".tmp"
	#

	def _createLocalPrivateTempDir(self) -> str:
		chmodValue = ChModValue(userW=True, userR=True, userX=True)

		t = int(time.time()*1000000000)
		while True:
			dirPath = "/tmp/dir_" + str(t) + "-" + str(random.randint(0, 1000000000)) + ".tmp"
			if not os.path.exists(dirPath):
				os.makedirs(dirPath, int(chmodValue), exist_ok=False)
				return dirPath
			t += 1
	#

	def _generateLocalPrivateTempFile(self, textContent:str = None, chmodValue:ChModValue = None) -> str:
		if chmodValue is None:
			chmodValue = ChModValue(userW=True, userR=True)

		t = int(time.time()*1000000000)
		while True:
			filePath = "/tmp/tmp_" + str(t) + "-" + str(random.randint(0, 1000000000)) + ".tmp"
			if not os.path.exists(filePath):
				with open(filePath, "w") as f:
					pass
				os.chmod(filePath, int(chmodValue))
				if textContent is not None:
					with open(filePath, "a") as f:
						f.write(textContent)
				return filePath
			t += 1
	#

#








