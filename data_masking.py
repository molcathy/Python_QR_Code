import qr_matrix
from math import floor

'''
Here the qr matrix is masked and penalties are calculated for each mask
the mask with the least amount of penalties is used for the qr code
the formatting string is calculated based on the mask chosen and then entered into the qr matrix
the qr matrix is then changed so that it is easier to convert to be shown visually on the GUI
'''

def apply_masking_pattern0(qr):
    # Masking pattern 0 is applied to the qr matrix based on this formula: (row + column) mod 2 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and ((i + j) % 2 == 0):
                assert (i + j) % 2 == 0, "Mask 0 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")

    return qr

def apply_masking_pattern1(qr):
    # Masking pattern 1 is applied to the qr matrix based on this formula: (row) mod 2 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and (i % 2 == 0):
                assert i % 2 == 0, "Mask 1 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern2(qr):
    # Masking pattern 2 is applied to the qr matrix based on this formula: (column) mod 3 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and (j % 3 == 0):
                assert j % 3 == 0, "Mask 2 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern3(qr):
    # Masking pattern 3 is applied to the qr matrix based on this formula: (row + column) mod 3 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and ((i + j) % 3 == 0):
                assert (i + j) % 3 == 0, "Mask 3 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern4(qr):
    # Masking pattern 4 is applied to the qr matrix based on this formula: ( floor(row / 2) + floor(column / 3) ) mod 2 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and ((floor(i/2) + floor(j/3)) % 2 == 0):
                assert (floor(i / 2) + floor(j / 3)) % 2 == 0, "Mask 4 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern5(qr):
    # Masking pattern 5 is applied to the qr matrix based on this formula: ((row * column) mod 2) + ((row * column) mod 3) == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and (((i * j) % 2) + ((i * j) % 3) == 0):
                prod = i * j
                assert ((prod % 2) + (prod % 3)) == 0, "Mask 5 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern6(qr):
    # Masking pattern 6 is applied to the qr matrix based on this formula: 	( ((row * column) mod 2) + ((row * column) mod 3) ) mod 2 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and ((((i * j) % 2) + ((i * j) % 3)) % 2 == 0):
                prod = i * j
                assert ((prod % 2 + prod % 3) % 2) == 0, "Mask 6 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def apply_masking_pattern7(qr):
    # Masking pattern 7 is applied to the qr matrix based on this formula: 	( ((row + column) mod 2) + ((row * column) mod 3) ) mod 2 == 0
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if (qr[i][j] != 'W' and qr[i][j] != 'B' and qr[i][j] != 'R') and ((((i + j) % 2) + ((i * j) % 3)) % 2 == 0):
                assert (((i + j) % 2 + (i * j) % 3) % 2) == 0, "Mask 7 condition failed"
                try:
                    if qr[i][j] == 0:
                        qr[i][j] = 1
                    elif qr[i][j] == 1:
                        qr[i][j] = 0
                except Exception as e:
                    raise ValueError(f"Masking failed at cell ({i}, {j}): {e}")
    return qr

def temp_change_qr(qr):
    # The characters such as W, B or R are turned into integers 0 or 1 as patterns and reserved areas are used to calculate the penalty
    # if there is a character '0' or '1' then those are converted into integers so that the penalties can be calculated for the qr matrix
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if qr[i][j] == 'W' or qr[i][j] == 'R':
                qr[i][j] = 0
            elif qr[i][j] == 'B':
                qr[i][j] = 1
            elif qr[i][j] == '0' or qr[i][j] == '1':
                qr[i][j] = int(qr[i][j])
    return qr

def penalty1(qr):
    # If there are 5 or more consecutive same colours then penalties are added
    penalty_total = 0
    for i in range(len(qr)):
        # trackR checks consecutive colours in the same row
        # trackC checks consecutive colours in the same column
        trackR = 0
        trackC = 0

        # the for loop starts at one as the previous bit and current bit are checked against each other
        # If the same, then at the beginning where trackR or trackC is 0 two is added for the two same bits compared, otherwise just 1 is added
        # If it is different then trackR or trackC is checked to see if it is 5 or more and the corresponding points are added
        for j in range(1, len(qr[i])):
            # this checks for the row
            if qr[i][j-1] == qr[i][j]:
                if trackR == 0:
                    trackR += 2
                elif trackR > 0:
                    trackR += 1
            elif qr[i][j-1] != qr[i][j]:
                if trackR == 5:
                    penalty_total += 3
                elif trackR > 5:
                    penalty_total += 3 + (trackR - 5)
                trackR = 0

            # this checks for the column
            if qr[j-1][i] == qr[j][i]:
                if trackC == 0:
                    trackC += 2
                elif trackC > 0:
                    trackC += 1
            elif qr[j-1][i] != qr[j][i]:
                if trackC == 5:
                    penalty_total += 3
                elif trackC > 5:
                    penalty_total += 3 + (trackC - 5)
                trackC = 0
    return penalty_total

def penalty2(qr):
    # The loop starts from one as a square is checked from the current and previous co-ordinates
    penalty_total = 0
    for i in range(1, len(qr)):
        for j in range(1, len(qr[i])):
            # All of the co-ordinates are checked for a 2x2 square of the same colour
            # if all of the co-ordinates equal each other then the 2x2 is the same colour and penalties are added
            if qr[i-1][j-1] == qr[i-1][j] and qr[i-1][j-1] == qr[i][j-1] and qr[i][j-1] == qr[i][j]:
                penalty_total += 3
    return penalty_total

def penalty3(qr):
    # This goes through the qr matrix and checks for two specific patterns in either columns or rows
    # the loop starts from 10 in the 2d matrix list as I check the previous 10 places to see if it matches up with the rest of the patterns
    # if the pattern matches up with what is in the qr matrix an appropriate penalty is added

    #dark-light-dark-dark-dark-light-dark-light-light-light-light
    #light-light-light-light-dark-light-dark-dark-dark-light-dark
    penalty_total = 0
    pattern1 = [1,0,1,1,1,0,1,0,0,0,0]
    pattern2 = [0,0,0,0,1,0,1,1,1,0,1]
    for i in range(10, len(qr)):
        for j in range(len(qr[i])):
            # the column is checked for pattern 1 or pattern 2
            if qr[i-10][j] == pattern1[0] and qr[i-9][j] == pattern1[1] and qr[i-8][j] == pattern1[2] and qr[i-7][j] == pattern1[3] and qr[i-6][j] == pattern1[4] and qr[i-5][j] == pattern1[5] and qr[i-4][j] == pattern1[6] and qr[i-3][j] == pattern1[7] and qr[i-2][j] == pattern1[8] and qr[i-1][j] == pattern1[9] and qr[i][j] == pattern1[10]:
                penalty_total += 40
            elif qr[i-10][j] == pattern2[0] and qr[i-9][j] == pattern2[1] and qr[i-8][j] == pattern2[2] and qr[i-7][j] == pattern2[3] and qr[i-6][j] == pattern2[4] and qr[i-5][j] == pattern2[5] and qr[i-4][j] == pattern2[6] and qr[i-3][j] == pattern2[7] and qr[i-2][j] == pattern2[8] and qr[i-1][j] == pattern2[9] and qr[i][j] == pattern2[10]:
                penalty_total += 40
            # the row is checked for pattern 1 or pattern 2
            if qr[j][i-10] == pattern1[0] and qr[j][i-9] == pattern1[1] and qr[j][i-8] == pattern1[2] and qr[j][i-7] == pattern1[3] and qr[j][i-6] == pattern1[4] and qr[j][i-5] == pattern1[5] and qr[j][i-4] == pattern1[6] and qr[j][i-3] == pattern1[7] and qr[j][i-2] == pattern1[8] and qr[j][i-1] == pattern1[9] and qr[j][i] == pattern1[10]:
                penalty_total += 40
            elif qr[j][i-10] == pattern2[0] and qr[j][i-9] == pattern2[1] and qr[j][i-8] == pattern2[2] and qr[j][i-7] == pattern2[3] and qr[j][i-6] == pattern2[4] and qr[j][i-5] == pattern2[5] and qr[j][i-4] == pattern2[6] and qr[j][i-3] == pattern2[7] and qr[j][i-2] == pattern2[8] and qr[j][i-1] == pattern2[9] and qr[j][i] == pattern2[10]:
                penalty_total += 40
    return penalty_total

def penalty4(qr):
    # I follow the steps from the Thonky website's rules for penalty for to calculate the ratio of light to dark modules

    # Count the total number of modules in the matrix
    total_modules = len(qr) * len(qr[0])

    #Count how many dark modules there are in the matrix.
    total_dark_modules = 0
    for row in qr:
        for module in row:
            total_dark_modules += module

    # Calculate the percent of modules in the matrix that are dark: (darkmodules / totalmodules) * 100
    percentage = (total_dark_modules/total_modules) * 100

    # Determine the previous and next multiple of five of this percent.
    multiple5_less = 0
    multiple5_more = 0
    num = percentage

    # The percentage if it is 10 or larger is cut down to just deal with the multiple of 5
    # the previous and next multiple of 5 are found and set to its appropriate variables
    if num >= 10:
        num = percentage - (int(percentage/10) * 10)
        if num >= 0 and num < 5:
            multiple5_less = int(percentage/10) * 10
            multiple5_more = (int(percentage/10) * 10) + 5
        elif num >= 5 and num < 10:
            multiple5_less = (int(percentage/10) * 10) + 5
            multiple5_more = (int(percentage/10) * 10) + 10
    else:
        # if the percentage is less than 10 then the multiple is figured out the same way just without the conversion
        if num >= 0 and num < 5:
            multiple5_less = 0
            multiple5_more = 5
        elif num >= 5 and num < 10:
            multiple5_less = 5
            multiple5_more = 10

    # Subtract 50 from each of these multiples of five and take the absolute value of the result
    # Divide each of these by five.
    multiple5_less = abs(multiple5_less - 50) / 5
    multiple5_more = abs(multiple5_more - 50) / 5

    # Finally, take the smallest of the two numbers and multiply it by 10
    # The result is the penalty and that is returned
    if multiple5_more < multiple5_less:
        return multiple5_more * 10
    elif multiple5_less < multiple5_more:
        return multiple5_less * 10

def apply_masking_patterns(qr):
    # a copy is made of the qr so the masking pattern is not permanent, and the qr masked result is stored
    qrs_masked = [apply_masking_pattern0([row.copy() for row in qr]), apply_masking_pattern1([row.copy() for row in qr]), apply_masking_pattern2([row.copy() for row in qr]), apply_masking_pattern3([row.copy() for row in qr]), apply_masking_pattern4([row.copy() for row in qr]), apply_masking_pattern5([row.copy() for row in qr]), apply_masking_pattern6([row.copy() for row in qr]), apply_masking_pattern7([row.copy() for row in qr])]
    penalty_scores = []

    # The masked qr's are copied and temporarily changed so that penalties can apply to W, R and B areas and to ensure everything is an integer, 0 or 1
    # then the penalties are applied to the changed masked qr
    # all penalties are applied and added up, then the total is stored in penalty_scores
    for qrChange in qrs_masked:
        qr_copy = [row.copy() for row in qrChange]
        qr_changed = temp_change_qr(qr_copy)
        total_penalty_score = 0
        total_penalty_score += penalty1(qr_changed)
        total_penalty_score += penalty2(qr_changed)
        total_penalty_score += penalty3(qr_changed)
        total_penalty_score += penalty4(qr_changed)
        penalty_scores.append(total_penalty_score)

    # the lowest value is found in penalty_scores and the index is returned so that the masked qr with the lowest penalty can be returned
    # the kind of mask that it uses is also returned
    lowest_penaltyQR_index = penalty_scores.index(min(penalty_scores))
    return qrs_masked[lowest_penaltyQR_index], lowest_penaltyQR_index

def placeDarkModule(qr, v1):
    # the dark module is placed in the co-ordinates specific to version 1 or version 2
    if v1 == True:
        qr[13][8] = 'B'
    elif v1 == False:
        qr[17][8] = 'B'
    return qr

def format_string(mask):
    # The format string is generated based on the mask that is used for the qr code
    generator_polynomial = '10100110111'
    format_info = '01' + format(mask, '03b')
    format_bits = list(format_info + '0000000000') 

    # This loop runs until the format bits are 10 bits long
    while len(format_bits) > 10:
        # Any 0's at the beginning of format bits are deleted
        beginning_zero = True
        while beginning_zero == True:
            if format_bits[0] == '0':
                del format_bits[0]
            else:
                beginning_zero = False
        assert format_bits[0] != '0'

        # The generator polynomial is padded on the right with 0's until it is the same length with the format bits
        # Temp is so that the generator polynomial can be adjusted each time to do that it cannot be a permanent change
        temp = generator_polynomial
        if len(temp) < len(format_bits):
            while len(temp) < len(format_bits):
                temp += '0'
            assert len(temp) == len(format_bits)

        # Each bit is XOR with the temp generator polynomial and the result is saved as the new format bits
        f_temp = []
        if len(temp) == len(format_bits):
            for a, b in zip(format_bits, temp):
                f_temp.append(str(int(a) ^ int(b)))

            format_bits = f_temp

        # the final check in the loop to ensure that the bits are exactly 10 bits long
        # if they are less then 0's are padded to the left of the format bits to be 10 bits long
        if len(format_bits) < 10:
            while len(format_bits) < 10:
                format_bits.insert(0, '0')

    # A check is done to ensure the length if format bits are 10 long
    assert len(format_bits) == 10
    
    # format result is the string that is XOR with the full format and is 15 bits long
    format_result = '101010000010010'
    # The full format is with the format info and format bits, all converted to string and should be 15 bits long
    full_format = format_info + ''.join(format_bits)
    # the format result is XOR with the full format and converted back to string and then returned
    return ''.join(str(int(full_format[i]) ^ int(format_result[i])) for i in range(len(format_result)))

def input_format_string(qr, format_string):
    # the format string is inputted into the reserved area, R, in the qr matrix
    # the format string is converted into a list
    format_list = list(format_string)
    countX = 0
    countY = len(format_string)-1
    # a similar method is used for entering the reserved section of of the qr matrix
    # instead this time one format string is entered in order where the row, i = 8
    # and the other format string is entered in reverse where the column is, j = 8
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if qr[i][j] != 'B' and qr[i][j] != 'W':
                if j == 8 and (i < 9 or i >= len(qr)-7):
                    qr[i][j] = int(format_list[countY])
                    countY -= 1
                elif i == 8 and (j < 8 or j >= len(qr)-8):
                    qr[i][j] = int(format_list[countX])
                    countX += 1
    return qr

def changeQR(qr):
    # 1 and 0 are changed to characters, B and W
    # this is so that the data can easily be converted into a format ready to be shown visually in the GUI
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if qr[i][j] == '1' or qr[i][j] == 1:
                qr[i][j] = 'B'
            elif qr[i][j] == '0' or qr[i][j] == 0:
                qr[i][j] = 'W'
    return qr

def finishedQR(qr_enter, v1_enter="no"):
    # this function calls all of the functions required for created the qr from:
    # calling the previous file qr_matrix to return the qr
    # then getting the masked qr
    # getting the formatting string
    # inputting the dar module and format string
    # lastly changing the qr and then returning it
    # if anything goes wrong there is a try and except to catch the error
    try:
        qr, v1 = qr_matrix.return_the_qr(qr_enter, v1_enter)
        qr_best, mask = apply_masking_patterns(qr)
        format_bits = format_string(mask)
        qr = placeDarkModule(qr_best, v1)
        qr = input_format_string(qr, format_bits)
        qr = changeQR(qr)
    except Exception as e:
        raise RuntimeError(f"QR generation failed: {e}")
    return qr

#Apply the format information and dark module
#show the image visually
# https://stackoverflow.com/questions/57270300/how-to-display-a-matrix-with-specific-colours-in-matplotlib-pyplot-without-using

if __name__ == '__main__':
    #qr = finishedQR("https://short.io/", "v2")
    qr, v1 = qr_matrix.return_the_qr("https://short.io/", 'v2')
    qr_best, mask = apply_masking_patterns(qr)
    print(f"QR with mask {mask}: ")
    qr_string = ''
    for i in range(len(qr_best)):
        string = ''
        for j in range(len(qr_best[i])):
            string += str(qr_best[i][j]) + " "
        qr_string += string + "\n"
    print(qr_string)
    
    format_bits = format_string(mask)
    print(f"Formatted bits for mask {mask}: {format_bits}")
    qr = placeDarkModule(qr_best, v1)
    qr = input_format_string(qr, format_bits)
    print(f"QR with mask {mask}, that has format string inside: ")
    qr_string = ''
    for i in range(len(qr)):
        string = ''
        for j in range(len(qr[i])):
            string += str(qr[i][j]) + " "
        qr_string += string + "\n"
    qr = changeQR(qr)
    print(qr_string)
