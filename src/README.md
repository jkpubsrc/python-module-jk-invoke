jk_invoke
==========

Introduction
------------

This python module provides a high level interface to provide a clean API for executing commands and reading and writing files transparently: It doesn't matter if you operate locally or remotely or as a regular user or as root via sudo.

Information about this module can be found here:

* [github.org](https://github.com/jkpubsrc/python-module-jk-invoke)
* [pypi.python.org](https://pypi.python.org/pypi/jk_invoke)

Why this module?
----------------

If you need to automate system administration tasks it is convenient if you do not need to distinguish between local or remote operation. This library wraps around `fabric` (which in turn wraps around `paramiko` and `invoke`) in order to streamline system administration tasks.

Limitations of this module
--------------------------

This module provides capabilities for:
* executing commands and process the data returned
* read individual files
* store individual files

Nothing more. So it's use is quite limited. Nevertheless this exactly fits requirements for system administration.

How to use this module
----------------------

### Import this module

Please include this module into your application using the following code:

```python
import jk_invoke
```

### Instantiate a password provider

You require a password provider. This object provides a password whenever it is required.

The following password providers are implemented:

* `InteractivePasswordProvider`
* `OneSlotPasswordProvider`

It is extremely easy to implemnt your own password provider. (For details see section "Extending jk_invoke" below.)

### Instantiate an invoker

There are two invokers available for use:
* `LocalInvoker` - This class should be used of you want to work with the local system.
* `RemoteInvoker` - This class should be used of you want to work with a remote system.

An instance of `LocalInvoker` will require these arguments:
* `callable passwordProvider` - An object that provides the password; required
* `int localSSHPort` - An integer that tells the system about the local SSH port; optional: if `None` the port will be autodetected via `/etc/ssh/sshd_config`

The SSH port is required if you intend to use `sudo`. (Though technically we could follow different approaches for ease of implementation an SSH connection to the local machine is initiated on *sudo*.)

Example:

```python
invoker = jk_invoke.LocalInvoker(
	jk_invoke.InteractivePasswordProvider(),
	)
```

An instance of `RemoteInvoker` will require these arguments:
* `str hostName` - The host to connect to; required
* `int port` - The TCP port to use during connect; required
* `str userName` - The user name to use for login; required
* `callable passwordProvider` - An object that provides the password for login; required

Example:

```python
invoker = jk_invoke.RemoteInvoker(
	"localhost",
	22,
	"someuser",
	jk_invoke.InteractivePasswordProvider(),
	)
```

### Execute a command

This is how you can execute a command:

```python
ret = invoker.runCmd("/usr/bin/id")
```

The data returned is of type `CommandResult`. This object provides:
* the STDOUT data
* the STDOUT data splitted into lines
* the STDERR data
* the STDERR data splitted into lines
* the command exit code
* the duration of execution in seconds

### Read a text file

This is how you can read the contents of a text file:

```python
ret = invoker.readTextFile("/etc/hostname")
```

The data returned is of type `str`.

### Write a text file

This is how you can read the contents of a text file:

```python
invoker.writeTextFile("/tmp/someFile", "abcXYZ123")
```

This method returns no data.

### Perform operations as super user

In order to run commands, read or write files as super user, use the `sudo()` method to obtain another invoker. Example:

```python
sudoInvoker = invoker.sudo()
ret = sudoInvoker.readTextFile("/etc/hostname")
```

The methods `runCmd()` and `writeTextFile()` can be used likewise and transparently.

Extending jk_invoke
-------------------

### Implement custom password providers

If you want to write an adapter for using `jk_invoke` in a different context, this is easy by providing a new password provider.

A custom password provider must meet the following requirements:

* It must be a callable object.
* If called two arguments are passed to the `__call__()` method:
	* `str machineName` - The machine to connect to
	* `str loginName` - The login name to use during connect
* On call you must return a string: The password to use on connect.

That's it. If you meet these requirements your password provider will perfectly work.

A prototype to start from could be the following code:

```python
class MyPasswordProvider(object):

	def __init__(self, thePassword:str):
		self.__pwd = thePassword

	def __call__(self, machineName:str, loginName:str) -> str:
		return self.__pwd

```

Contact Information
-------------------

This work is Open Source. This enables you to use this work for free.

Please have in mind this also enables you to contribute. We, the subspecies of software developers, can create great things. But the more collaborate, the more fantastic these things can become. Therefore Feel free to contact the author(s) listed below, either for giving feedback, providing comments, hints, indicate possible collaborations, ideas, improvements. Or maybe for "only" reporting some bugs:

* Jürgen Knauth: jknauth@uni-goettingen.de, pubsrc@binary-overflow.de

License
-------

This software is provided under the following license:

* Apache Software License 2.0



