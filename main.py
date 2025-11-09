import sys
from parser import parse_lines
import mapping

file_location = None

print("\n LC-3 Assembler v0.94 \n")

sys.argv = sys.argv[1:]

if len(sys.argv) == 2 and (sys.argv[1].endswith('.asm')):
    if sys.argv[0] == "-o" or sys.argv[0] == "--obj":
        file_format = ".obj"
        file_location = sys.argv[1]
    else:
        print("Invalid Command")    
elif len(sys.argv) == 1 and sys.argv[0].endswith('.asm'):
    file_format = ".bin"
    file_location = sys.argv[0]
elif len(sys.argv) == 1 and (sys.argv[0] == "-h" or sys.argv[0] == "--help"):
    print("\n Help \n")
    print("Usage (main.py): py main.py [options] <sourcefile.asm>\n")
    print("Usage (LC3Assembler.exe): ./LC3Assembler.exe [options] <sourcefile.asm>\n")
    print("Options:")
    print("  -o, --obj       Output in .obj binary format (default is .bin text format)\n")
    sys.exit(0)
else:
  sys.exit("Please provide a file location as a command line argument.")

print("\n PARSING \n")

with open(file_location, 'r') as file:
    file_lines = file.readlines()
    parsed_lines = parse_lines(file_lines)
        
print("\n MAPPING \n")
    
converted = mapping.map_opcodes_and_operands([opcode for opcode, _ in parsed_lines], [operands for _, operands in parsed_lines])

print("\n WRITING \n")
    
output_location = file_location.replace('.asm', file_format)


with open(output_location, ("w" if file_format == ".bin" else "wb")) as output_file:
    for i in range(len(converted)):
        item = converted[i]
        if len(item) == 2:
            opcode, operand = item
            print(f"Opcode Binary: {opcode}, Operand Binary: {operand}")
            binary_string = opcode + ''.join(operand)
        else:
            binary_string = item
        
        if file_format == ".bin":
            comment_string = "    ; " + parsed_lines[i][0] + " " + ' '.join(parsed_lines[i][1])
            write_string = binary_string + comment_string + '\n'
            print(f"Writing: {write_string}")
            output_file.write(write_string)
        elif file_format == ".obj":
            byte_value = int(binary_string, 2)
            byte_array = byte_value.to_bytes(2, byteorder='big')
            print(f"Writing bytes: {byte_array}")
            output_file.write(byte_array)