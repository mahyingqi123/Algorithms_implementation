import sys

"""
Name: Mah Ying Qi
Student ID: 32796765
Email: ymah0009@student.monash.edu

This file contains the implementation of the reverse boyer moore algorithm.

"""

def gusfield_z(string):
    """
    Calculates the Z-values for each position in the input string.
    Z-value at index i == the length of the longest substring starting from i that matches the prefix.
    """
    n = len(string)
    z = [None] * n

    current_index = 1
    compare_index = 0
    r = 0
    l = 0

    for i in range(1, n):

        # if right is less than i, calculate z[i] from scratch
        if i > r:
            current_index = i
            compare_index = 0
            while current_index < n and string[current_index] == string[compare_index]:
                compare_index += 1
                current_index += 1
            if compare_index > 0:
                l = i
                r = current_index - 1
                z[i] = r - l + 1
            else:
                z[i] = 0
        else:
            # if the current index is within the z-box, copy the value from the corresponding index
            if z[i - l] < r - i + 1:
                z[i] = z[i - l]
            # if the current index is at the end of the z-box, calculate z[i] from scratch
            else:
                current_index = r + 1
                compare_index = r - i + 1
                while current_index < len(string) and string[current_index] == string[compare_index]:
                    compare_index += 1
                    current_index += 1
                z[i] = current_index - i
                r = current_index - 1
                l = i
    return z



def bad_character_preprocess(pattern):
    '''
    Bad character array, but reversed,
    shows the first occurrence of a character in the pattern
    If the character is not in the pattern, it is -1
    '''
    result = [[-1 for i in range(94)] for i in range(len(pattern))]

    for i in range(len(pattern)):
        start = len(pattern) - i - 1
        for j in range(len(pattern) - 1, start - 1, -1):
            result[i][ord(pattern[j]) - 33] = j

    return result

def good_suffix_preprocess(pattern):
    """
    Good suffix array, but reversed,
    shows the leftmost occurrence of a suffix in the pattern
    """
    z_suffix = gusfield_z(pattern)
    good_suffix = [0] * (len(pattern) + 1)
    for i in range(len(pattern) - 1, 0, -1):
        j = z_suffix[i] - 1
        good_suffix[j] = i
    return good_suffix

def matched_prefix_preprocess(pattern):
    """
    Matched prefix array, but reversed,
    shows the length of the longest prefix that is also a suffix
    """
    z = gusfield_z(pattern[::-1])[::-1]
    matched_prefix = [0] * (len(pattern) + 1)
    matched_prefix[-2] = len(pattern)
    j = 0
    for i in range(len(pattern) - 1):
        if z[i] - 1 == i:
            j = z[i]
        matched_prefix[i] = j
    return matched_prefix


def bad_character_rule(bad_character, i, c,length):
    """
    Shows how many places to shift based on bad character array
    If the character is not in the pattern, return 1

    """
    return max(1, bad_character[i][ord(c) - 33]-i)

def good_suffix_rule(good_suffix, matched_prefix, i,length):
    """
    Shows how many places to shift based on good suffix array
    If the good suffix is 0, return the matched prefix
    """
    if good_suffix[i - 1] > 0:
        return good_suffix[i - 1]
    else:
        return length - matched_prefix[i - 1]

def reverse_boyer_moore(txt, pat):
    """
    Performs the reversed Boyer-Moore algorithm to find all occurrences of the pattern in the text in reverse.
    Returns a list of starting positions of the pattern in the text.
    """
    res = []
    if len(pat) == 0:
        return [0]
    if len(pat) > len(txt):
        return []
    if len(pat) == 1:
        for i in range(len(txt)):
            if txt[i] == pat[0]:
                res.append(i)
        return res
    bad_character = bad_character_preprocess(pat)
    matched_prefix = matched_prefix_preprocess(pat)
    good_suffix = good_suffix_preprocess(pat)
    i = len(txt) - len(pat)
    stop = -1
    while i >= 0:
        left = i
        j = 0
        while j < len(pat) and txt[i] == pat[j]:
            i += 1
            j += 1
            if j == stop:
                j = start
                i = i + (start - stop)


        if j >= len(pat):
            # Pattern matched, shift by the length of the safest suffix

            res.append(left + 1)
            shift = len(pat) - matched_prefix[-3]
        else:
            # Getting the maximum shift, by either good suffix, matched prefix or bad character
            shift = max(good_suffix_rule(good_suffix, matched_prefix, j, len(pat)),
                         bad_character_rule(bad_character, j, txt[i],len(pat)))
        i = left - shift
        # Performing Galil's Optimization
        if good_suffix[j - 1] > 0:
            stop = good_suffix[j - 1] 
            start = good_suffix[j - 1] + j+1
        else:
            stop = matched_prefix[j - 1]
            start = len(pat)
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

    result = reverse_boyer_moore(text[0], pattern[0])
    with open("output_q1.txt", "w") as f:
        for i in result:
            f.write(str(i) + "\n")
    


