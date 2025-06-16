import reedsolo

'''
Objective:
To translate the user input into binary data, which is then formatted and encoded
This is done for version 1 and version 2
'''

def binary_len(binary_string):
    # I calculate the total amount of bits in the binary string
    # eg. [['0','1','0','0'], ['0','0','1','0']] = 8
    binary_length = 0
    for byte in binary_string:
        binary_length += len(byte)
    return binary_length

def manage_input(qr_input):
    # I add the words to a search query if the words entered are not part of a website

    #ISO 8859-1, use byte mode
    #I use ISO 8859-1 to encode the input and turn each character into a byte of data
    byte_data = qr_input.encode('iso-8859-1')
    binary_list = [format(byte, '08b') for byte in byte_data]

    # If the binary list is too long then I get a outside website to help with shortening the url
    # I get a new url
    # Version 1 L byte mode character capacity 17
    # Version 2 L byte mode character capacity 32
    # Byte mode is 0100 = 4

    # I check that the encoding worked and followed the proper formatting
    assert all(0 <= b <= 255 for b in byte_data), "Non-ISO-8859-1 byte detected"
    assert isinstance(byte_data, bytes), "Byte encoding failed"
    assert all(len(b) == 8 for b in binary_list), "Each binary string must be 8 bits"

    count = len(qr_input)

    return format(count, '08b'), format(4, '04b'), binary_list

def format_input(length, binary_length, character_count, byte_indicator, binary_list):
    length_complete = False
    terminator_count = 0
    specified_bytes = list("1110110000010001")
    count_specified = 0
    
    while length_complete == False:
        # Here I call a function to return the total bits in binary list
        binary_length = binary_len(binary_list)
        # I then ensure that the loop continues to run while the total data is underneath the length
        # the 9 stands for the character_count which should be 9, and 4 is for the binary length which should be 4
        if len(character_count) + len(byte_indicator) + binary_length < length:
            assert len(character_count) == 8
            assert len(byte_indicator) == 4
            
            # I add the terminator directly to the binary list
            if terminator_count < 4:
                terminator_count += 1
                binary_list[-1] += '0'

            # encode using selected mode?
            # If the total bits is not a multiple of 8 then I fill until it is a total of 8
            # if the terminator has been added then I fill 
            elif binary_len(binary_list) % 8  != 0 and len(binary_list[-1]) < 8:
                assert terminator_count == 4
                assert binary_len(binary_list) % 8 > 0
                assert len(binary_list[-1]) < 8
                binary_list[-1] += '0'
            
            # I go through the list and make sure to add a bit to a byte one by one until the length required is reached
            elif count_specified < len(specified_bytes):
                bit = specified_bytes[count_specified]
                if len(binary_list[-1]) == 8:
                    assert len(binary_list[-1]) == 8
                    binary_list.append("")
                
                binary_list[-1] += bit
                
                count_specified += 1
                if count_specified == len(specified_bytes):
                    count_specified = 0
        else:
            assert len(character_count) + len(byte_indicator) + binary_length == length
            length_complete = True

    # I turn the list of bytes into a string
    binary_string_input = ''.join(byte for byte in binary_list)

    #I return the byte/mode indicator, the character count, and the binary string together
    return byte_indicator + character_count + binary_string_input

def putting_it_togetherVersion(character_count, byte_indicator, binary_list, v1):
    ch_capacity = 0
    version1 = False
    
    binary_length = binary_len(binary_list)
    
    if v1 == "v1":
        version1 = True
        ch_capacity = 19
    elif v1 == "v2":
        version1 = False
        ch_capacity = 34
    else:
        #If the amount is for version 1, then version 1 is set to True and character capacity is set
        if binary_length <= 152:
            version1 = True
            ch_capacity = 19
        elif binary_length > 152 and binary_length <= 272:
            #If the amount is not for version 1, then version 1 is set to False and character capacity is set
            version1 = False
            ch_capacity = 34
    
    # I format the character count so that if the total is not 9 bits I fill the left with '0' to get 9 bits
    while len(character_count) < 8:
        temp = '0' + character_count
        character_count = temp

    #The length based on character capacity is set
    length = ch_capacity * 8
    
    # I call a function to format  the data that has been set
    formatted_data = format_input(length, binary_length, character_count, byte_indicator, binary_list)

    # I return the version and the formatted_data that is encoded as well
    return version1, formatted_data

def error_correction(v1, data):
    # Data is seperated into bytes into a list
    data_codewords = [int(data[i:i+8], 2) for i in range(0, len(data), 8)]
    assert len(data) % 8 == 0
    expected_data_len = 19 if v1 else 34
    assert len(data_codewords) == expected_data_len
    expected_ecc_len = 7 if v1 else 10
    #For version 1 and version 2 the data encoding is set for 7 and 10 for the encoding
    # That 7 and 10 bits are separated from the data_codewords and error corrected
    if v1:
        rs = reedsolo.RSCodec(7)
        ecc = rs.encode(bytes(data_codewords))[-7:]
        assert len(ecc) == expected_ecc_len
    else:
        rs = reedsolo.RSCodec(10)
        ecc = rs.encode(bytes(data_codewords))[-10:]
        assert len(ecc) == expected_ecc_len

    #the data_codewords and error corrected bits are added back and turned into a string
    full_codewords = data_codewords + list(ecc)
    bit_stream = ''.join(format(b, '08b') for b in full_codewords)

    if not v1:
        bit_stream += '0' * 7

    assert len(full_codewords) == expected_data_len + expected_ecc_len
    return bit_stream, v1

def enterData(qr_enter, v1_enter):
    # The encoded and formatted data is created for the qr matrix with the functions and returned
    qr_input = qr_enter
    v1_yes_no = v1_enter
    character_count, byte_indicator, binary_list = manage_input(qr_input)
    
    v1, data = putting_it_togetherVersion(character_count, byte_indicator, binary_list, v1_yes_no)
    return error_correction(v1, data)

if __name__ == '__main__':
    count, byte, binary_list = manage_input("https://short.io/")
    print(f"Binary count: {count}, byte mode: {byte}, binary list data: {binary_list}")
    v1, formatted_data = putting_it_togetherVersion(count, byte, binary_list, 'v2')
    print(f"Is it version 1: {v1}, and formatted data: {formatted_data}")
    bit_stream, v1 = error_correction(v1, formatted_data)
    print(f"Data now with error correction: {bit_stream}")