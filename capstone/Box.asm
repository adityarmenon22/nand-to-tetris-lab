(LOOP)
@24576
D=M
@WHITE
D;JEQ
@color
M=-1
@DRAW
0;JMP

(WHITE)
@color
M=0

(DRAW)
@16576
D=A
@addr
M=D
@20
D=A
@rows
M=D

(ROWLOOP)
@rows
D=M
@LOOP
D;JEQ

@color
D=M
@addr
A=M
M=D

@color
D=M
@addr
A=M+1
M=D

@color
D=M
@addr
A=M+1
A=A+1
M=D

@32
D=A
@addr
M=D+M

@rows
M=M-1
@ROWLOOP
0;JMP