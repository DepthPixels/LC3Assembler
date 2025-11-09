def parse_lines(file_lines):
  """
  Reads lines from a file and returns them as a list,
  stripping whitespace, and returning separated opcode and operands
  """
  
  parsed_data = []
  extra = []
  
  for line in file_lines:
    if line != "\n" and not line.startswith(';'):
      parts = line.split(',')
      parts = [part.strip() for part in parts]
      
      found_comment = False
      new_parts = []
      for part in parts:
        if ';' in part:
          sub_part = part.split(';')[0].strip()
          new_parts.append(sub_part)
          found_comment = True
        if found_comment == False:
          new_parts.append(part)
      
      parts = new_parts
      opcode = parts[0]
      operands = parts[1:] if len(parts) > 1 else []
      
      split_code = opcode.split()
      opcode = split_code[0]
      if len(split_code) > 1:
        operands = split_code[1:] + operands
      
      if len(operands) > 1:
        if operands[0] == ".STRINGZ":
          if operands[1].startswith('"') and operands[1].endswith('"'):
            string_content = operands[1][1:-1]
            for i in range(len(string_content)):
              char = string_content[i]
              ascii_value = ord(char)
              binary_value = format(ascii_value, '016b')
              if i == 0:
                parsed_data.append((opcode, [".STRINGZ", ".FILL", f"{binary_value}"]))
              else:
                parsed_data.append((".FILL", [f"{binary_value}"]))
              
            parsed_data.append((".FILL", ['0x0000']))
          continue 
        
      if opcode == ".STRINGZ":
        if operands[0].startswith('"') and operands[0].endswith('"'):
          string_content = operands[0][1:-1]
          for i in range(len(string_content)):
            char = string_content[i]
            ascii_value = ord(char)
            binary_value = format(ascii_value, '016b')
            if i == 0:
              parsed_data.append((".STRINGZ", [".FILL", f"{binary_value}"]))
            else:
              parsed_data.append((".FILL", [f"{binary_value}"]))
            
          parsed_data.append((".FILL", ['0x0000']))
        continue        
            
      parsed_data.append((opcode, operands))
      
      if opcode == ".END":
        break
      
      print(f"Parsed Line: Opcode: {opcode}, Operands: {operands}")
    
  return parsed_data