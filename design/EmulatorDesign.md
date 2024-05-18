# Emulator Design
- Allocate Directive space
    - Create class "Address", and a list "Variable" of Addresses.
    - Get list of Directives
    - For each Directive allocate the propper memory
    - For each instruction store the bits
    - For each label update labe

-----------------------------------------

## Address Class
- Attributes
    - value
- Methods
    -  set(val,binary): int sets the value of address in two's complement if binary is not set. \(if it's string sets value to int first). If binary is checked then checks string is of binary format, then copies to value with prepending 0's.
    -  get(): str returns value
    - getInt(): int returns the value converted to integer with two's complement.
     