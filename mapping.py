opcode_dict = {
    "ADD": "0001",
    "AND": "0101",
    "BR": "0000",
    "JMP": "1100",
    "JSR": "0100",
    "JSRR": "0100",
    "LD": "0010",
    "LDI": "1010",
    "LDR": "0110",
    "LEA": "1110",
    "NOT": "1001",
    "RET": "1100",
    "RTI": "1000",
    "ST": "0011",
    "STI": "1011",
    "STR": "0111",
    "TRAP": "1111",
}

register_dict = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "R7": "111",
}

label_dict = {}

hex_convert_pseudo_ops = [".ORIG", ".FILL"]

short_ops = {"GETC": "1111000000100000", "OUT": "1111000000100001", "PUTS": "1111000000100010", "IN": "1111000000100011", "PUTSP": "1111000000100100", "HALT": "1111000000100101"}

def sign_extend(value, bits):
    """
    Sign extends a value to the specified number of bits.
    """
    # Create a mask for the specified number of bits
    mask = (1 << bits) - 1
    
    # Apply mask and format to binary string
    return format(value & mask, f'0{bits}b')

def hex_to_bin(hex_string):
    """
    Converts a hexadecimal string to a binary string of specified bits.
    """
    bits = len(hex_string) * 4  # Each hex digit represents 4 bits
    value = int(hex_string, 16)
    return sign_extend(value, bits)


def map_opcodes_and_operands(opcodes, operands):
    """
    Maps a list of opcode strings to their corresponding binary values.
    """
    
    label_parse(opcodes, operands)
    
    mapped_lines = []
    pc = 0
    for i in range(len(opcodes)):
        if mapped_lines:
            pc = int(mapped_lines[0], 2) + i
            print(f"Mapping line {i}: Opcode: {opcodes[i]}, Operands: {operands[i]}, at PC: {hex(pc)}")
        if opcodes[i] in opcode_dict:
            mapped_opcode = opcode_dict[opcodes[i]]
            mapped_operand = map_operand(opcodes[i], operands[i], pc)
            mapped_lines.append((mapped_opcode, mapped_operand))
        elif opcodes[i][:2] == "BR":
            mapped_opcode = opcode_dict["BR"]
            condition_codes = opcodes[i][2:]
            n = '1' if 'n' in condition_codes else '0'
            z = '1' if 'z' in condition_codes else '0'
            p = '1' if 'p' in condition_codes else '0'
            mapped_opcode += n + z + p
            mapped_operand = map_operand("BR", operands[i], pc)
            mapped_lines.append((mapped_opcode, mapped_operand))
        else:
            # Handle pseudo-ops if necessary
            converted = map_special_opcode(opcodes[i], operands[i], pc)
            if converted is not None:
                mapped_opcode = map_special_opcode(opcodes[i], operands[i], pc)
                mapped_lines.append(mapped_opcode)

    return mapped_lines

def label_parse(opcodes, operands):
    """
    First pass to parse labels and store their locations.
    """
    pc = 0
    orig = None
    for i in range(len(opcodes)):
        if orig:
            pc = int(orig, 2) + i
        if opcodes[i] == ".ORIG":
            orig = map_special_opcode(opcodes[i], operands[i], pc)
        elif opcodes[i] not in opcode_dict and opcodes[i][:2] != "BR" and opcodes[i] not in short_ops and opcodes[i] not in hex_convert_pseudo_ops and opcodes[i] != ".END":
            label_dict[opcodes[i]] = (pc-1)
            
    print(f"Label Dictionary: {label_dict}")


def map_special_opcode(opcode, operands, pc):
    if len(operands) == 1:
        operands = operands[0]
        if operands.startswith('x'):
            operands = operands[1:]
        if operands.startswith('0x'):
            operands = operands[2:]
        
    if opcode in hex_convert_pseudo_ops:
        converted = hex_to_bin(operands)
    elif opcode == ".END":
        return None
    elif opcode in opcode_dict:
        mapped_opcode = opcode_dict[opcode]
        mapped_operand = map_operand(opcode, operands, pc)
        converted = (mapped_opcode, mapped_operand)
    elif opcode in short_ops:
        converted = short_ops[opcode]
    else:
        sub_opcode = operands[0]
        operands = operands[1:]
        converted = map_special_opcode(sub_opcode, operands, pc)
        label_dict[opcode] = (pc-1)
  
    return converted
    
  
def map_operand(opcode, operand, pc):
    """
    Maps a list of operand strings to their corresponding binary values.
    """
    mapped_operand = []
    for i in range(len(operand)):
        part = operand[i]
        if part in register_dict:
            if (opcode == "ADD" or opcode == "AND") and i == 2:
                    mapped_operand.append('000')  # Indicate register mode
            if opcode == "JMP" and i == 0:
                mapped_operand.append('000')
                
            mapped_operand.append(register_dict[part])
            
            if (opcode == "JSRR") and i == 0:
                mapped_operand.insert(0, '000')
                mapped_operand.append('000000')
            if (opcode == "NOT") and i == 1:
                mapped_operand.append('111111')
                    
        elif part.startswith('#'):
            # Immediate value
            # Attempt to parse as an immediate value
            part = int(part[1:])
            if opcode in ["BR", "LD", "LDI", "LEA", "ST", "STI"]:
                offset_limit = 9
            elif opcode in ["ADD", "AND"]:
                mapped_operand.append('1')
                offset_limit = 5
            elif opcode == "LDR" or opcode == "STR":
                offset_limit = 6
            elif opcode == "JSR":
                mapped_operand.append('1')
                offset_limit = 11
            negative_limit = 2**(offset_limit - 1) * -1
            positive_limit = 2**(offset_limit - 1) - 1
            if (part < negative_limit) or (part > positive_limit):
                raise ValueError(f"Immediate value out of range: {part}")
            value = sign_extend(part, offset_limit)
            mapped_operand.append(value)
            
        elif part.startswith('x') or part.startswith('0x'):
            if opcode == "TRAP":
                mapped_operand.append('0000')
            if opcode == "JSR":
                mapped_operand.append('1')
            # Hexadecimal value
            if part.startswith('x'):
                part = part[1:]
            elif part.startswith('0x'):
                part = part[2:]
                
            value = hex_to_bin(part)
            mapped_operand.append(value)
        elif all(char == '0' or char == '1' for char in part):
            if opcode == "JSR":
                mapped_operand.append('1')
            # Binary value
            mapped_operand.append(part)
        elif part in label_dict:
            # This is an encountered label
            label_location = label_dict[part]
            offset = label_location - pc
            if opcode in ["BR", "LD", "LDI", "LEA", "ST", "STI"]:
                offset = sign_extend(offset, 9)
            elif opcode == "LDR" or opcode == "STR":
                offset = sign_extend(offset, 6)
            elif opcode == "JSR":
                offset = sign_extend(offset, 11)
            mapped_operand.append(offset)
            
    if operand == []:
        if opcode == "RET":
            mapped_operand = ["000111000000"]
        if opcode == "RTI":
            mapped_operand = ["000000000000"]
            
    
    return mapped_operand