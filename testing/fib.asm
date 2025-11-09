.ORIG x3000

;we're going to calculate the fibonachi numbers, up to 999
	AND R2,R2,#0
	AND R1,R1,#0 	;set R1 and R2 to zero
	ADD R1,R1,#1 	;Nte: nzp is now POSITIVE
LOOP	JSR PRINT
	AND R3,R3,#0
	ADD R3,R1,#0	;store R1 in R3
	ADD R1,R1,R2	;Add R2 to R1
	AND R2,R2,#0
	ADD R2,R3,#0	;Store R3 in R2 
	LD R4, MINUSM
	ADD R3,R1,R4
	BRn LOOP


END	HALT


PRINT	ADD R3,R1,#0	;put the output value in R3
	LD R5,NHUN	;start the hundreds place
	AND R4,R4,#0	;R4=0, running count
	LEA R0,STROUT	;R0=output address
LOOP1	ADD R3,R3,R5	;subtract 100
	BRn WRITEH
	ADD R4,R4,#1	;add one if still greater than
	BRnzp LOOP1
WRITEH	LDR R6,R0,#0
	ADD R6,R6,R4
	STR R6,R0,#0
	LD R4,HUN	;using R4, b/c I'm about to reset it
	ADD R3,R3,R4	;R3's hundres are now zero
	AND R4,R4,#0
	LD R5,NTEN

LOOP2	ADD R3,R3,R5
	BRn WRITET
	ADD R4,R4,#1
	BRnzp LOOP2
WRITET	LDR R6,R0,#1
	ADD R6,R6,R4
	STR R6,R0,#1
	AND R4,R4,#0
	ADD R3,R3,#10
	LD R5,NONE	;R5=-1

LOOP3	ADD R3,R3,R5
	BRn WRITEO
	ADD R4,R4,#1
	BRnzp LOOP3
WRITEO	LDR R6,R0,#2
	ADD R6,R6,R4
	STR R6,R0,#2
	AND R4,R4,#0	;R4 is zero now
	ADD R3,R3,#1
OUTPUT	LEA R0,STROUT
	ADD R4,R7,#0	;Store R7 in R4, b/c PUTS will overwrite it.
	PUTS
	AND R7,R7,#0
	ADD R7,R4,#0	;Restore R7
	LD R3,ZEROC
	STR R3,R0,#0
	STR R3,R0,#1
	STR R3,R0,#2
	RET
	HALT

MINUSM	.FILL #-1000	;constant for negative 1000
NHUN	.FILL #-100
NTEN	.FILL #-10
NONE	.FILL #-1
HUN	.FILL #100
STROUT	.STRINGZ "000\n";string to fill
ZEROC	.FILL x0030
.END
