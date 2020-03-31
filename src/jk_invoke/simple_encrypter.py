



import os
import base64
from Crypto.Cipher import AES



def encryptPwd(pwd:str) -> str:
	assert isinstance(pwd, str)

	secretKey = "GalliaEstOmnisDi".encode("ascii")
	iv = os.urandom(16)

	cipher = AES.new(secretKey, AES.MODE_CFB, iv=iv)
	binEncoded = cipher.encrypt(pwd.encode("utf-8"))
	base64Encoded = base64.b64encode(binEncoded)

	return "1$" + base64.b64encode(iv) + "$" + base64Encoded
#

def decryptPwd(data:str) -> str:
	assert isinstance(data, str)

	secretKey = "GalliaEstOmnisDi".encode("ascii")

	parts = data.split("$")
	assert len(parts) == 3
	assert parts[0] == "1"

	iv = base64.b64decode(parts[2])

	cipher = AES.new(secretKey, AES.MODE_CFB, iv=iv)
	binEncoded = base64.b64decode(parts[2])
	return cipher.decrypt(binEncoded)
#







