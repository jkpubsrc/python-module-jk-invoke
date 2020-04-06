#!/usr/bin/python3



import jk_pwdinput
import jk_invoke
from jk_testing import Assert




pwd = jk_pwdinput.readpwd("Please enter a password: ")
ciphertext = jk_invoke.encryptPwd(pwd)
print("Enrypted: " + ciphertext)








