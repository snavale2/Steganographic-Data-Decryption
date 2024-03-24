import sys

def extract_hidden_data(file_path):
    with open(file_path, 'rb') as file:
        # Ignore the first 100 bytes
        file.seek(100)
        
        # Read the next 64 bytes and extract LSBs from each byte individually, then reverse the bits
        indicator_bits = []
        for _ in range(64):
            byte = file.read(1)
            if not byte:
                break  # End of file reached unexpectedly
            lsb = byte[0] & 1  # Extract LSB
            indicator_bits.append(lsb)
        
        # Reverse the bits
        reversed_indicator_bits = indicator_bits[::-1]
        
        # Combine the bits into bytes and convert to bytes object
        reversed_indicator = bytes([int(''.join(map(str, reversed_indicator_bits[i:i+8])), 2) for i in range(0, len(reversed_indicator_bits), 8)])

        # Check if the reversed indicator matches 0xa5 repeated 8 times
        if reversed_indicator != b'\xa5' * 8:
            print("Non-stegan file.")
            return None
        
        # Extract the size of the hidden information (27 bytes)
        size_bits = []
        for _ in range(27):
            byte = file.read(1)
            if not byte:
                break  # End of file reached unexpectedly
            lsb = byte[0] & 1  # Extract LSB
            size_bits.append(lsb)
        
        # Reverse the bits and convert to integer
        reversed_size_bits = size_bits[::-1]
        size = int(''.join(map(str, reversed_size_bits)), 2)  # Convert bits to integer

        # Extract the hidden data using LSB from subsequent bytes until size is reached
        hidden_data = bytearray()
        bit_count = 0
        current_byte = ''
        while bit_count < size * 8:
            byte = file.read(1)
            if not byte:
                break  # End of file reached unexpectedly
            current_byte += str(byte[0] & 1)  # Extract LSB
            bit_count += 1
            if bit_count % 8 == 0:
                hidden_data.append(int(current_byte[::-1],2))
                current_byte = ''
        
        return hidden_data
    
if len(sys.argv) != 3:
    print("Invalid input; Usage: python ./your_prog.py input_file output_file")
    sys.exit(1)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

hidden_data = extract_hidden_data(input_file_path)

if hidden_data:
# Write the hidden data to an output PDF file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(hidden_data)
