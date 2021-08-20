"""Takes a text file and dtm, and copies the edited inputs in the text file to a new dtm.
Arguments are DTM input, then text file input."""

import sys
from ast import literal_eval
from shutil import copy

def condense_bitfield(bits:list[int], length:int):
    """Takes a bunch of 1's and 0's in a list and returns an int of all the bits together."""

    output = 0
    bits.reverse()
    for i in range(length):
        output <<= 1 #Order is important here to ensure the output doesn't end up one bit too long.
        output += bits[i]
    return output

def input_list_to_bytes(inputs:list):
    """Takes a list of inputs such as those in the text file and returns the 8 byte data found in DTM files."""
    ints_list = []
    ints_list.append(condense_bitfield(inputs[:8], 8))
    ints_list.append(condense_bitfield(inputs[8:16], 8))
    ints_list.extend(inputs[16:18])
    ints_list.extend(inputs[18])
    ints_list.extend(inputs[19])

    assert len(ints_list) == 8, "Ints list broke. Expecting length 8, got " + str(len(ints_list))
    return bytes(ints_list)

source_dtm = sys.argv[1]
dest_dtm = source_dtm[:-4] + "_edited.dtm"

copy(source_dtm, dest_dtm)

with open(sys.argv[2]) as text_input:
    text_list = text_input.read().splitlines()

inputs_list = [literal_eval(line) for line in text_list]
inputs_bytes_list = [input_list_to_bytes(frame) for frame in inputs_list]

with open(dest_dtm, "r+b") as dtm_output:
    dtm_output.seek(0x100) #Skip the header
    for frame in inputs_bytes_list:
        dtm_output.write(frame)
