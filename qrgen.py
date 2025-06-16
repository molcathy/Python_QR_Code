import reedsolo

def generate_error_corrected_codewords(data_bytes, ecc_codewords):
    rs = reedsolo.RSCodec(ecc_codewords)
    encoded_data = rs.encode(data_bytes) # error correction
    print(encoded_data)
    corrected_bits = ''.join(format(byte, '08b') for byte in encoded_data) # converts text into byte mode
    return corrected_bits

def build_qr_payload(data_bytes):
    bits = '0100'  # byte mode
    bits += format(len(data_bytes), '08b')  # character count

    for byte in data_bytes:
        bits += format(byte, '08b')  # data bits assembly

    bits += '0000'  # terminator if room / padding

    while len(bits) % 8 != 0:
        bits += '0'

    # Pad with alternating bytes to reach 152 bits
    pad_bytes = ['11101100', '00010001']
    i = 0
    while len(bits) < 152:
        bits += pad_bytes[i % 2]
        i += 1

    data_codewords = [int(bits[i:i+8], 2) for i in range(0, len(bits), 8)] # splits bytes
    return data_codewords

text = input()
textEncoded = bytearray(text, 'utf-8') ## to utf-8 to turn into byte mode | Correct handling of byte mode [/]
print(list(textEncoded))

# config
ecc_codewords = 7
padding = ["11101100", "00010001"]

data_codewords = build_qr_payload(textEncoded) # data_codewords [/]
corrected_bits = generate_error_corrected_codewords(data_codewords, ecc_codewords) # ecc_codewords [/]