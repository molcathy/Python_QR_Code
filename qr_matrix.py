import reedsolo as rs
import numpy as np
import data_encoding_correction

"""
Current Task:

Matrix Layout and Patterns: Finder patterns in corners, timing
pattern, dark module, format information area reserved. Zigzag
placement of the data/ECC bits in the right modules (skipping
reserved cells). Application of one masking pattern (any single
pattern is fine). Resulting text-based QR is structurally
consistent with Version 1 (21×21) and version 2 (25x25).
"""

def matrix_size(version):
    #Based on the whether it is version 1, v1 == True or version 2, v1 == False
    # A qr matrix is created with the required size, 21x21 or 25x25
    qr = []

    if version == True:
        qr = [[1 for i in range(21)] for i in range(21)]
    elif version == False:
        qr = [[1 for i in range(25)] for i in range(25)]
    
    return qr

def add_finder_patterns(qr, version):
    # The finder pattern is always the same size for version 1 and version 2 so it is fixed
    # This places the finder patterns within the qr matrix at the correct positions
    finder_matrix = [['B','B','B','B','B','B','B'],
                     ['B','W','W','W','W','W','B'],
                     ['B','W','B','B','B','W','B'],
                     ['B','W','B','B','B','W','B'],
                     ['B','W','B','B','B','W','B'],
                     ['B','W','W','W','W','W','B'],
                     ['B','B','B','B','B','B','B']]
    #The size is of the finder pattern is double checked
    assert len(finder_matrix) == 7 and all(len(row) == 7 for row in finder_matrix), "Finder pattern must be 7x7"

    # The co-ordinates are set based on the version
    co_ordinates = [] #top left, bottom left, top right
    if version == True:
        co_ordinates = [[0,0], [14, 0], [0, 14]]
    elif version == False:
        co_ordinates = [[0,0], [18, 0], [0, 18]]

    #Now to translate the finder matrix to the qr matrix
    # I make sure to use the size of the finder pattern and the size of the qr matrix entered
    # This allows for the finder pattern to be dynamically allocated in the correct place in the matrix
    size_finder = len(finder_matrix)-1
    size_qr = len(qr)-1
    diff = (size_qr - size_finder)

    for i in range(len(qr)):
        for j in range(len(qr[i])):
            # for the top left
            if i <= size_finder and j <= size_finder:
                qr[i][j] = finder_matrix[i][j]

            # for the bottom left
            if i >= diff and j <= size_finder:
                qr[i][j] = finder_matrix[i-diff][j]

            # for the top right
            if i <= size_finder and j >= diff:
                qr[i][j] = finder_matrix[i][j-diff]

    return qr

def add_separators(qr):
    separator_size = 7
    
    # I know that the separators are always in the same place
    # The qr size is used to dynamically allocate that separator in the same place
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            # top left
            if (i == separator_size and j <= separator_size) or (i <= separator_size and j == separator_size):
                qr[i][j] = 'W'

            # top right
            if (i <= separator_size and j == len(qr) - separator_size - 1) or (i == separator_size and j >= len(qr) - separator_size - 1):
                qr[i][j] = 'W'

            # bottom left
            if (i == len(qr) - separator_size - 1 and j <= separator_size) or (i >= len(qr) - separator_size - 1 and j == separator_size):
                qr[i][j] = 'W'
    return qr

def check_alignment_overlap(qr, alignment_pattern, co_ordinate):
    # I check at a specific co-ordinate, where all of the co-ordinates of the alignment pattern will be
    # W = white, and B = black and R = reserved, where W or B or R is placed there is a pattern
    # I ensure that none of the co-ordinates of the alignment pattern in the qr matrix have B or W or R
    # If there is any R or B or W where i want to place the pattern then there is overlap

    overlap = False
    #The co-ordinate is already entered through the parameters
    start_i = co_ordinate[0]-2

    for i in range(len(alignment_pattern)):
        start_j = co_ordinate[1]-2
        if start_i < 0 or start_i + len(alignment_pattern) > len(qr) or start_j < 0 or start_j + len(alignment_pattern[0]) > len(qr[0]):
            raise ValueError(f"Alignment pattern at {co_ordinate} goes out of bounds")

        for j in range(len(alignment_pattern[i])):
            if qr[start_i][start_j] == 'B' or qr[start_i][start_j] == 'W':
                overlap = True

            start_j += 1
        start_i += 1
    return overlap

def add_alignment_patterns(qr, version):
    # The alignment pattern is always the same size
    alignment_pattern = [['B','B','B','B','B'],
                          ['B','W','W','W','B'],
                          ['B','W','B','W','B'],
                          ['B','W','W','W','B'],
                          ['B','B','B','B','B']]
    # Version 1 is not given an alignment pattern and returned
    if version == True:
        return qr
    elif version == False:
        # The alignment pattern is checked to see at which of these co-ordinates it can be at without overlapping with other patterns
        diff = len(qr) - len(alignment_pattern)
        alignment_patterns = [[6,6], [6, 18], [18, 6], [18, 18]]
        for pattern in alignment_patterns:
            if check_alignment_overlap(qr, alignment_pattern, pattern) != True:
                # Once a pattern is found it is then implemented into the qr matrix
                start_i = pattern[0]-2
                for i in range(len(alignment_pattern)):
                    start_j = pattern[1]-2
                    for j in range(len(alignment_pattern[i])):
                        qr[start_i][start_j] = alignment_pattern[i][j]
                        start_j += 1

                    start_i += 1
        
        return qr

def add_timing_patterns(qr):
    # have a variable to keep track of the previous colour and then to alternate the colour for the given columns
    # there will be specific co-ordinates where either the x or y increases
    # These last_colour variables keep track of each individual timing pattern
    last_colour1 = 'W'
    last_colour2 = 'W'
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if i == 6 and j == 6:
                pass
            elif (i == 6 or j == 6) and (qr[i][j] != 'B' and qr[i][j] != 'W'):
                # When i == 6 then then the timing pattern is being added horizontally
                if i == 6:
                    if last_colour1 == 'W':
                        qr[i][j] = 'B'
                        last_colour1 = 'B'
                    elif last_colour1 == 'B':
                        qr[i][j] = 'W'
                        last_colour1 = 'W'
                # When j == 6 the timing pattern is being added vertically
                elif j == 6:
                    if last_colour2 == 'W':
                        qr[i][j] = 'B'
                        last_colour2 = 'B'
                    elif last_colour2 == 'B':
                        qr[i][j] = 'W'
                        last_colour2 = 'W'
    return qr

def add_reservedData(qr):
    # R is added in the qr matrix where the revered area is and where the format string is entered later
    x = 8
    y = 8

    # the reserved information is either on the x axis at 8 or on the y axis at 8 at specific ranges
    for i in range(len(qr)):
        for j in range(len(qr[i])):
            if qr[i][j] != 'W' and qr[i][j] != 'B':
                if (i == 8 and (j <= 8 or j >= len(qr[i]) - 8)) or (j == 8 and (i <= 8 or i >= len(qr[i]) - 8)):
                    qr[i][j] = 'R'
    return qr


def add_data_bits(qr, bit_stream):
    # I ensure that the bit_stream is in list format
    assert isinstance(bit_stream, list), "Bit stream must be a list"
    n = len(qr)
    col = n - 1
    up = True

    while col > 0:
        if col == 6:  # skip the timing column
            col -= 1

        #I change the up from false to true each time going from up to down every two columns
        row_range = range(n-1, -1, -1) if up else range(n)

        for row in row_range:
            for dx in [0, -1]:  # right column, then left
                x = col + dx
                # I ensure to not add data in any of the patterns or the reserved information area
                if qr[row][x] not in ('B', 'W', 'R') and bit_stream:
                    try:
                        qr[row][x] = int(bit_stream.pop(0)) # removes and returns bit stream data and enters it into the qr matrix
                    except IndexError:
                        raise IndexError(f"Tried to write data bit at ({row},{x}) but bit_stream was empty")

        #The columns are changed to the next two, and the direction is changed
        col -= 2
        up = not up

    return qr

def test():
    # This is a test done to ensure that the add_data_bits are entering data in the correct order, in the right places
    v1 = True
    qr_data = []
    # The data is created to be in a 21 by 21 matrix in an ordered format
    for i in range(21*21):
        qr_data.append(i)

    # The qr is created
    qr = matrix_size(v1)
    qr = add_finder_patterns(qr, v1)
    qr = add_separators(qr)
    qr = add_alignment_patterns(qr, v1)
    qr = add_timing_patterns(qr)
    qr = add_reservedData(qr)
    # The data is added
    qr = add_data_bits(qr, qr_data)

    # The resulting qr is shown, where you can see data starting with 1, 2, 3, 4 etc.
    # The numbers in increasing order shows where and what order the data is being added to the matrix
    qr_string = ""
    for row in qr:
        formatted_row = ""
        for cell in row:
            # strings are formatted for a 3 character width as the numbers will end up being in the hundreds
            # This is for better readability
            if isinstance(cell, str):
                formatted_row += f"{cell:>3}"  # Align B, W, R
            else:
                formatted_row += f"{cell:>3}"  # Align numbers
        qr_string += formatted_row + "\n"
    print("This shows the order of input of data in matrix: ")
    print(qr_string)



def generate_qr_matrix(v1, bit_stream):
    # v1 is used to determine which kind of matrix to created based on the version
    qr = matrix_size(v1)
    # I make sure that the correct sized qr is made and that the qr has the same length and width
    if v1:
        assert len(qr) == 21
    elif not v1:
        assert len(qr) == 25
    assert len(qr) == len(qr[0]), "QR matrix must be square"
    # The rest of the qr is created with the other functions for creating aspects of the qr code being called
    qr = add_finder_patterns(qr, v1)
    qr = add_separators(qr)
    qr = add_alignment_patterns(qr, v1)
    qr = add_timing_patterns(qr)
    qr = add_reservedData(qr)
    qr = add_data_bits(qr, bit_stream)
    return qr

def return_the_qr(qr_enter, v1_enter):
    # The functions from the previous file data_encoding_correction.py is called
    # The encoded data is returned as well as the v1 boolean
    # I ensure that the there is an exception if there is an error with the previous file
    try:
        encoded_data, v1 = data_encoding_correction.enterData(qr_enter, v1_enter)
    except Exception as e:
        raise RuntimeError(f"Data encoding failed: {e}")

    # the function for creating the qr code is called and the qr is made with the data from the previous file
    # an exception is here so that if something goes wrong when creating the qr matrix
    try:
        bit_stream = [bit for bit in encoded_data]
        qr = generate_qr_matrix(v1, bit_stream)
    except Exception as e:
        raise RuntimeError(f"QR matrix generation failed: {e}")

    # The qr matrix and the v1 boolean are returned
    return qr, v1


if __name__ == '__main__':
    # The qr is created here with the data from error_encoding_correction and then shown in the terminal
    encoded_data, v1 = data_encoding_correction.enterData("https://short.io/", "v2")
    bit_stream = [int(bit) for bit in encoded_data]

    qr = generate_qr_matrix(v1, bit_stream)
    qr_string = ''
    for i in range(len(qr)):
        string = ''
        for j in range(len(qr[i])):
            string += str(qr[i][j]) + " "
        qr_string += string + "\n"
    print("Resulting qr string: ")
    print(qr_string)

    # the test is done to see how data is entered in add_data_bits function
    test()

#https://short.io/
#https://www.shorturl.at/