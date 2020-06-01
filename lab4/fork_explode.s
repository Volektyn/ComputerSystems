.include "defs.h"

.section .bss
n: .quad 0
pid: .quad 0

.section .data
nforks: .quad 10

.section .text
.global _start

_start:

fork:
    movq $SYS_FORK, %rax
    syscall
    movq %rax, pid

    cmpq $0, pid        /* if (pid !=0) goto parent; */
    jne parent

child:
    movq nforks, %rax
    movq $48, %rsi
    leaq (%rax,%rsi), %rdx
    movq %rdx, n

    /* write number */
    movq $SYS_WRITE, %rax
    movq $STDOUT, %rdi
    movq $n, %rsi
    movq $1, %rdx
    syscall

    decq nforks

    cmpq $0, nforks        /* if (nforks == 0) goto end; */
    je end

    jmp fork

parent:
    movq $SYS_WAIT4, %rax
    movq pid, %rdi
    movq $0, %rsi
    movq $0, %rdx
    movq $0, %r10
    syscall

end:
    movq $SYS_EXIT, %rax
    movq $0, %rdi
    syscall

