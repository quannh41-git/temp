import base64
import os

# Input and output file paths
input_file = r".\out_base64.txt"
output_file = r".\out_restored.zip"

# Read the base64 text file
with open(input_file, 'r') as f:
    base64_content = f.read()

# Decode from base64
file_content = base64.b64decode(base64_content)

# Write to zip file in binary mode
with open(output_file, 'wb') as f:
    f.write(file_content)

print(f"Converted {input_file} from base64")
print(f"Saved to {output_file}")
print(f"Base64 size: {len(base64_content)} characters")
print(f"Restored size: {len(file_content)} bytes")
