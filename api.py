from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import Response
from parser import parse_lines
import mapping
import io

app = FastAPI(title="LC-3 Assembler API")

@app.post("/assemble")
async def assemble_code(file: UploadFile = File(...), format: str = "bin"):
    """
    Assembles LC-3 assembly code
    format: 'bin' or 'obj'
    """
    try:
        # Read the uploaded file
        content = await file.read()
        file_lines = content.decode('utf-8').splitlines(keepends=True)
        
        # Parse
        parsed_lines = parse_lines(file_lines)
        
        # Map
        converted = mapping.map_opcodes_and_operands(
            [opcode for opcode, _ in parsed_lines], 
            [operands for _, operands in parsed_lines]
        )
        
        # Generate output
        output = io.BytesIO() if format == "obj" else io.StringIO()
        
        for i in range(len(converted)):
            item = converted[i]
            if len(item) == 2:
                opcode, operand = item
                binary_string = opcode + ''.join(operand)
            else:
                binary_string = item
            
            if format == "bin":
                comment_string = "    ; " + parsed_lines[i][0] + " " + ' '.join(parsed_lines[i][1])
                output.write(binary_string + comment_string + '\n')
            elif format == "obj":
                byte_value = int(binary_string, 2)
                byte_array = byte_value.to_bytes(2, byteorder='big')
                output.write(byte_array)
        
        # Return response
        if format == "bin":
            return Response(content=output.getvalue(), media_type="text/plain")
        else:
            return Response(content=output.getvalue(), media_type="application/octet-stream")
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)