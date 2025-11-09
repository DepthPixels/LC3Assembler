def parse_lines(file_lines):
  """
  Reads lines from a file and returns them as a list,
  stripping whitespace, and returning separated opcode and operands
  """
  
  parsed_data = []
  extra = []
  
  for line in file_lines:
    if line != "\n":
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
      
      parsed_data.append((opcode, operands))
      
      if opcode == ".END":
        break
      
      print(f"Parsed Line: Opcode: {opcode}, Operands: {operands}")
    
  return parsed_data