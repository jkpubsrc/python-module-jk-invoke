


import typing
import os
import json




#
# Objects of this class represent the processing result of a command.
#
class CommandResult(object):

	def __init__(self, cmd:str, cmdArgs:typing.Union[tuple,list], stdOut:str, stdErr:str, returnCode:int, duration:float):
		assert isinstance(cmd, str)
		assert isinstance(cmdArgs, (tuple, list))
		assert isinstance(stdOut, str)
		assert isinstance(stdErr, str)
		assert isinstance(returnCode, int)
		assert isinstance(duration, float)

		self.__cmd = cmd
		self.__cmdArgs = cmdArgs
		self.__stdOut = stdOut
		self.__stdErr = stdErr
		self.__stdOutLines = None
		self.__stdErrLines = None
		self.__duration = duration
		self.__returnCode = returnCode
	#


	@property
	def duration(self) -> float:
		return self.__duration
	#



	#
	# Returns the path used for invokation of the command.
	# @return		string			The file path.
	#
	@property
	def commandPath(self) -> str:
		return self.__cmd
	#



	#
	# Returns the arguments used for invokation of the command.
	# @return		string[]		The list of arguments (possibly an empty list or <c>None</c>).
	#
	@property
	def commandArguments(self) -> list:
		return self.__cmdArgs
	#



	#
	# The return code of the command after completion.
	# @return		int			The return code.
	#
	@property
	def returnCode(self) -> int:
		return self.__returnCode
	#



	@property
	def stdOut(self) -> str:
		return self.__stdOut
	#



	#
	# The STDOUT output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdOutLines(self) -> list:
		if self.__stdOutLines is None:
			self.__stdOutLines = self.__stdOut.split("\n")
			if not self.__stdOutLines[-1]:
				del self.__stdOutLines[-1]
		return self.__stdOutLines
	#


	#
	# Return the text data as a regular JSON object.
	#
	def getStdOutAsJSON(self):
		return json.loads(self.__stdOut)
	#



	@property
	def stdErr(self) -> str:
		return self.__stdErr
	#



	#
	# The STDERR output of the command.
	# @return		string[]		The output split into seperate lines. This property always returns a list, never <c>None</c>.
	#
	@property
	def stdErrLines(self) -> list:
		if self.__stdErrLines is None:
			self.__stdErrLines = self.__stdErr.split("\n")
			if not self.__stdErrLines[-1]:
				del self.__stdErrLines[-1]
		return self.__stdErrLines
	#



	#
	# Return the text data as a regular JSON object.
	#
	def getStdErrAsJSON(self):
		return json.loads(self.__stdErr)
	#



	#
	# Returns <c>True</c> iff the return code is not zero or <c>STDERR</c> contains data
	#
	@property
	def isError(self) -> bool:
		return (self.__returnCode != 0) or self.__stdErr
	#



	#
	# If the return code is not zero or <c>STDERR</c> contains data
	# an exception is thrown using the specified exception message.
	#
	# @param		string exceptionMessage			The message for the exception raised.
	# @return		CommandOutput					If no exception is raised the object itself is returned.
	#
	def raiseExceptionOnError(self, exceptionMessage, bDumpStatusOnError = False):
		if self.isError:
			if bDumpStatusOnError:
				self.dump()
			raise Exception(exceptionMessage)
		else:
			return self
	#



	#
	# Write all data contained in this object to STDOUT. This method is provided for debugging purposes.
	#
	def dump(self, prefix = None, writeFunction = None):
		if writeFunction is None:
			writeFunction = print
		if prefix is None:
			prefix = ""
		writeFunction(prefix + "COMMAND: " + self.__cmd)
		writeFunction(prefix + "DURATION: " + str(self.__duration))
		writeFunction(prefix + "ARGUMENTS: " + str(self.__cmdArgs))
		for line in self.stdOutLines:
			writeFunction(prefix + "STDOUT: " + repr(line))
		for line in self.stdErrLines:
			writeFunction(prefix + "STDERR: " + repr(line))
		writeFunction(prefix + "RETURNCODE: " + str(self.__returnCode))
	#



	#
	# Returns a dictionary containing all data.
	# @return		dict			Returns a dictionary with data registered at the following keys:
	#								"cmd", "cmdArgs", "stdOut", "stdErr", "retCode", "duration"
	#
	def toJSON(self):
		return {
			"duration": self.__duration,
			"cmd": self.__cmd,
			"cmdArgs" : self.__cmdArgs,
			"stdOut" : self.stdOutLines,
			"stdErr" : self.stdErrLines,
			"retCode" : self.__returnCode,
		}
	#



#














