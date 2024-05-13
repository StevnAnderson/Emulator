# Emulator Design
- Allocate Directive space
    - Create class "Address", and a list "Variable" of Addresses.
    - Get list of Directives
    - For each Directive allocate the propper memory

-----------------------------------------

## Address Class
- Attributes
    - value
- Methods
    -  Read(str): str - Returns the value at address as str, int, or raw based on parameter str.
    - Write(val): None - writes the val to value, making it a string of all 1's and 0's that's no more than 96 in length, and fills in 0's to any not written.
    - 