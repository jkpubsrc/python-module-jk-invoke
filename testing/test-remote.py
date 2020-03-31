#!/usr/bin/python3



import jk_invoke



invoker = jk_invoke.RemoteInvoker(
	"localhost",
	22,
	"woodoo",
	jk_invoke.InteractivePasswordProvider(),
	)





ret = invoker.runCmd("/usr/bin/id")
ret.dump()

print()

ret = invoker.sudo().runCmd("/usr/bin/id")
ret.dump()



print()



ret1 = invoker.readTextFile("/etc/hostname")
print(repr(ret1))

ret2 = invoker.sudo().readTextFile("/etc/hostname")
print(repr(ret2))

assert ret1 == ret2



print()



invoker.writeTextFile("/tmp/asdkjhsldfkjahslkdfjhaslkjdhfsa1", "asdfgh")
invoker.sudo().writeTextFile("/tmp/asdkjhsldfkjahslkdfjhaslkjdhfsa2", "asdfgh")

ret1 = invoker.readTextFile("/tmp/asdkjhsldfkjahslkdfjhaslkjdhfsa1")
ret2 = invoker.sudo().readTextFile("/tmp/asdkjhsldfkjahslkdfjhaslkjdhfsa2")

assert ret1 == ret2





