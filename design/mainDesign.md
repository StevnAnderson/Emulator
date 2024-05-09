# Assembler

## Data Section

- Here is where you define the strings, integer values, and block spaces for the emulator.
- valid data syntax regex: (\s+|[a-zA-Z][a-zA-Z0-9]*) \<directive> \<operand>
- full list of directives: 
  | Directive | Operand |
   |-------|-------|
   |.INT|int in range -2147483648 to 2147483647|
   |.BYT| 1 byte of space (0 if no operand) in range 0 to 255, or apostrophe delineated ascii character|
   |.BTS|required decimal value, allocates that many bytes.|
   |.STR| lenth of string +2 number of bytes allocated, first byte is length of string, last is 0 unless operand is numeric, then allocates that number + 2 bytes, first holds the number, and the rest are 0|

## Code Section

- Here is where you define the code to be executed by the emulator.
- valid code syntax regex: (\s+|[a-zA-Z][a-zA-Z0-9]*) \<instruction> \<operand1> \<operand2>
- full list of instructions found in pdf

---------------------------


### Main layout
 
- take input from file or stdin. save it to list of strings labeled "lines". (delimiting on newline)
- create a variable (dataSection) that represents when the data section is finished.
- enter a for loop over lines (splitting on semicolons and grabbing first part) that matches all viable words:
  - each directive will check if dataSection, else throw error. Then verify syntax.
  - Each instruction will set dataSection to false, then verify syntax.
  - do nothing if blank
