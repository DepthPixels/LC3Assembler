.ORIG x3000
; yo im a full comment
    YO .FILL x2003
    NOT R0, R2  ; Hi im a comment
    LEA R3, #254
    AND R0, R0, R1
    ADD R0, R0, R1
    LD R1 YES
    LD R0 YO
    BRnz #-2
    HALT
    JSR #255
    RET
    YES .FILL 0x2002
    .STRINGZ "YO"

.END