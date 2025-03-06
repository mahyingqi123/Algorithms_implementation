from bitarray import bitarray
import sys

"""
Name: Mah Ying Qi
Student ID: 32796765
Email: ymah0009@student.monash.edu

This file contains the implementation of the bit pattern matching algorithm.

"""


def bit_pattern_matching(txt, pat):
    """
    Bit matching algorithm that finds all occurences of the pattern in the text.
    Identify the matches in the first window first, then shift by 1 place every iteration
    In every iteration, compare the last character of the window with the last character of the pattern
    Combine the bitvector of the previous window with the delta of the current window
    If the first bit of the bitvector is 0, then the pattern is found
    """
    res = []
    bitvector = bitarray(len(pat)) 
    delta = bitarray(len(pat))

    # Create the bitvector for the first window
    for i in range(len(pat)):
        bitvector[i] = 0
        index_pattern = 0
        index_text = i
        # Compare each character of the pattern with the text, set the bitvector to 1 if there is a mismatch
        while index_text <len(pat) :
            if txt[index_text] != pat[index_pattern]:
                bitvector[i] = 1
                break
            index_text+=1
            index_pattern+=1
    
    # If the first bit of the bitvector is 0, then the pattern is found at first index
    if bitvector[0] == 0:
        res.append(1)

    # Slide the window and update the bitvector
    for i in range(len(pat),len(txt)):

        # Compare last character of the window with the last character of the each region
        for j in range(len(pat)-1,-1,-1):
            if txt[i] == pat[j]:
                delta[len(pat)-1-j] = 0
            else:  
                delta[len(pat)-1-j] = 1

        # Shift the bitvector to the left and add the new delta
        bitvector = bitvector << 1 | delta

        # If the first bit of the bitvector is 0, then the pattern is found
        if bitvector[0] == 0:
            res.append(i-len(pat)+2)
    return res

def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line

if __name__ == "__main__":
    _, input1, input2 = sys.argv
    text = read_file(input1)
    pattern = read_file(input2)
    result = bit_pattern_matching(text[0], pattern[0])
    with open("output_q2.txt", "w") as f:
        for i in result:
            f.write(str(i) + "\n")





