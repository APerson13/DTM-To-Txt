"""Takes a Dolphin input file as input and outputs a text file to allow for easy input editing."""

import sys

# STRING_OUTPUT = """Inputs: [START, A, B, X, Y, Z, UP, DOWN, LEFT, RIGHT, L, R, disc, reset, \
# connect controller, reset analog, L analog, R analog, (Analog X, Y), (Cstick X, Y)]
# Note that connect controller and reset analog are not present in Dolphin releases before 5.0-5911 \
# and 5.0-1049 respectively."""
STRING_OUTPUT = ""

def decode_bitfield(bitfield:int, return_length:int):
    """Takes an int input and returns a list of 'return_length' entries of each bit in 'bitfield' as true or false."""
    output_list = []
    for i in range(return_length):
        output_list.append(bitfield & 1)
        bitfield >>= 1 #This will make a list of least to most significant bits.
    # output_list.reverse()
    return output_list

def decode_inputs(inputs:bytes):
    """Returns a string with inputs for a given frame."""
    byte_list = list(inputs)
    assert len(byte_list) == 8
    input_list = decode_bitfield(byte_list[0], 8)
    input_list.extend(decode_bitfield(byte_list[1], 8))
    #This gives the following set of inputs in order:
    #START, A, B, X, Y, Z, UP, DOWN, LEFT, RIGHT, L, R, change disc, reset, nothing, nothing
    input_list.append(byte_list[2]) #L analog
    input_list.append(byte_list[3]) #R analog
    input_list.append((byte_list[4], byte_list[5])) #Analog stick (x, y)
    input_list.append((byte_list[6], byte_list[7])) #C stick (x, y)
    return str(input_list)

with open(sys.argv[1], "rb") as file_input:
    file_input.seek(0x100)

    while True:
        try:
            STRING_OUTPUT += decode_inputs(file_input.read(8)) + '\n'
        except AssertionError:
            break

with open("inputs_text.txt", "w+") as file_output:
    file_output.write(STRING_OUTPUT)