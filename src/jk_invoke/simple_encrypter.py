



import os
import base64
from Crypto.Cipher import AES



def encryptPwd(pwd:str) -> str:
	assert isinstance(pwd, str)

	secretKey = "GalliaEstOmnisDi".encode("ascii")
	iv = os.urandom(16)
	assert isinstance(iv, (bytes, bytearray))

	cipher = AES.new(secretKey, AES.MODE_CFB, iv=iv)
	binEncoded = cipher.encrypt(pwd.encode("utf-8"))
	assert isinstance(binEncoded, (bytes, bytearray))
	base64Encoded = base64.b64encode(binEncoded)

	partMagic = "SiPaEn"
	partVersion = "1"
	partIV = base64.b64encode(iv).decode("utf-8")
	partData = base64.b64encode(binEncoded).decode("utf-8")

	return "$".join([ partMagic, partVersion, partIV, partData ])
#

def decryptPwd(data:str) -> str:
	assert isinstance(data, str)

	secretKey = "GalliaEstOmnisDi".encode("ascii")

	parts = data.split("$")
	assert len(parts) == 4
	partMagic, partVersion, partIV, partData = parts
	assert partMagic == "SiPaEn"
	assert partVersion == "1"

	iv = base64.b64decode(partIV.encode("utf-8"))
	assert isinstance(iv, (bytes, bytearray))

	cipher = AES.new(secretKey, AES.MODE_CFB, iv=iv)
	binEncoded = base64.b64decode(partData.encode("utf-8"))
	assert isinstance(iv, (bytes, bytearray))

	return cipher.decrypt(binEncoded).decode("utf-8")
#

def isPwdEncrypted(data:str) -> str:
	assert isinstance(data, str)

	parts = data.split("$")
	if len(parts) != 4:
		return False
	partMagic, partVersion, partIV, partData = parts
	if partMagic != "SiPaEn":
		return False
	if partVersion != "1":
		return False

	return True
#







