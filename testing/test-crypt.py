#!/usr/bin/python3



import jk_invoke
from jk_testing import Assert





plaintext = "this is a test"
print("plaintext: " + repr(plaintext))

Assert.isFalse(jk_invoke.isPwdEncrypted(plaintext))

print("Encrypt ...")
ciphertext = jk_invoke.encryptPwd(plaintext)
print("ciphertext: " + repr(ciphertext))

Assert.isTrue(jk_invoke.isPwdEncrypted(ciphertext))

print("Decrypt ...")
plaintext2 = jk_invoke.decryptPwd(ciphertext)
print("plaintext2: " + repr(plaintext2))

Assert.isFalse(jk_invoke.isPwdEncrypted(plaintext2))

assert plaintext == plaintext2








