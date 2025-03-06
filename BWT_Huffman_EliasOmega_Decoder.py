from suffix_array import SuffixTree
from bitarray import bitarray
import heapq
from math import log
import sys

def BWT(string):
    """
    create burrow wheeler's transform of the string
    """
    # create suffix array using ukkonen's algorithm
    suffixtree = SuffixTree(string)
    suffix_array = suffixtree.traverse_inorder(suffixtree.root)
    bwt_string = [0 for _ in range(len(suffix_array))]

    # create bwt string
    for i in range(len(suffix_array)):
        bwt_string[i] = (suffix_array[i] -1) if suffix_array[i] != 0 else len(string)-1

    # count number of different characters in the string
    distinct_char = [i for i in range(len(suffixtree.root.edges)) if suffixtree.root.edges[i] is not None ]

    return bwt_string, distinct_char

def dec_to_bin(number):
    """
    Convert decimal number to binary
    """
    result = bitarray()
    while number > 0:
        result.append(number % 2)
        number = number // 2
    result.reverse()
    return result

def elias_omega_encoder(number):
    """
    Elias omega encoding of a number
    """
    binary = dec_to_bin(number)
    stack = [binary]
    number = len(binary) -1
    while number > 0:
        binary = dec_to_bin(number)
        binary[0] = 0
        number = len(binary) - 1
        stack.append(binary)
    result = bitarray()
    while len(stack) > 0:
        result.extend(stack.pop())
    return result

def count_distinct_char(string):
    """
    Count number of distinct characters in the string
    """
    ascii_list = [0 for _ in range(94)]
    for i in string:
        ascii_list[ord(i)-33]=1
    return sum(ascii_list)

def char_to_ascii(character):
    """
    Convert character to ascii with length 7
    """
    ascii_int = ord(character)
    ascii_bin = dec_to_bin(ascii_int)
    if len(ascii_bin) < 7:
        x = bitarray(1)
        x[0] = 0
        x.extend(ascii_bin)
        ascii_bin = x
    return ascii_bin

class huffman_node:
    """
    A node in the huffman tree
    """
    def __init__(self, frequency, character):
        self.character = character # character in the node
        self.frequency = frequency # frequency of the character

    def __lt__(self, other):
        """
        Comparison function for the huffman node
        """
        return self.frequency < other.frequency or (self.frequency == other.frequency and len(self.character) < len(other.character))

class huffman_encode_tree:
    """
    Huffman encoding of string
    """
    def __init__(self, string):
        self.string = string
        self.character_count = [0 for _ in range(94)] # count of each character in the string
        for i in string:
            self.character_count[ord(i)-33] += 1 
        self.encode_table = [bitarray() for _ in range(94)]
        self.result = bitarray()
        self.huffman_encoding()
    
    
    def huffman_encoding(self):
        """
        Encode the string using huffman encoding
        """
        heap = []

        # insert all characters in the heap
        for i in range(94):
            if self.character_count[i] > 0:
                heapq.heappush(heap, huffman_node(self.character_count[i],chr(i+33)))

        # create huffman tree
        while len(heap) > 1:
            # get two nodes with minimum frequency
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            # add 0 to left and 1 to right character
            for i in left.character:
                new = bitarray('0')
                new.extend(self.encode_table[ord(i)-33])
                self.encode_table[ord(i)-33] = new
            for i in right.character:
                new = bitarray('1')
                new.extend(self.encode_table[ord(i)-33])
                self.encode_table[ord(i)-33] = new

            # create a new node with combined frequency                
            combined = huffman_node(left.frequency + right.frequency, left.character + right.character)
            heapq.heappush(heap, combined)
        
        # create encoding for the entire string
        for i in self.string:
            self.result.extend(self.encode_table[ord(i)-33])
        

        
    def print_huffman_tree(self, node, level=0):
        """
        Function to pretty print the huffman tree recursively
        """
        print('|-'*level,node.character, node.frequency)
        if node.left is not None:
            self.print_huffman_tree(node.left, level+1)
        if node.right is not None:
            self.print_huffman_tree(node.right, level+1)
    
def generate_bit_stream(string):
    result = bitarray()
    # create bwt of the string
    bwt_result, distinct_char = BWT(string)

    # encode the length of the bwt and number of distinct characters
    elias_bwt_length = elias_omega_encoder(len(bwt_result))
    elias_distinct_char = elias_omega_encoder(len(distinct_char))

    # add the length of the bwt and number of distinct characters to the bitstream
    result.extend(elias_bwt_length)
    result.extend(elias_distinct_char)

    # encode the bwt string
    huffman_table = huffman_encode_tree(string).encode_table

    # add each character into bitstream
    for i in distinct_char:
        # add ascii of the character
        result.extend(char_to_ascii(chr(i+33)))
        # add length of the huffman code
        result.extend(elias_omega_encoder(len(huffman_table[i])))
        # add huffman code
        result.extend(huffman_table[i])

    pointer = 0

    # add each character in the bwt string into the bitstream
    while pointer < len(bwt_result):
        # get the character to encode
        character = string[bwt_result[pointer]]
        count = 1

        # count the number of same characters
        while pointer < len(bwt_result)-1 and string[bwt_result[pointer+1]] == character:
            count += 1
            pointer += 1

        # get huffman code of the character
        huffman_code = huffman_table[ord(character)-33]

        # add huffman code to the bitstream
        result.extend(huffman_code)
        # add count of the character to the bitstream
        result.extend(elias_omega_encoder(count))
        pointer += 1

    # add padding to the end bitstream to become full bytes
    result += bitarray('0'*(8-len(result)%8))

    return result

def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line

if __name__ == "__main__":
    _, inputFile = sys.argv
    text = read_file(inputFile)
    result = generate_bit_stream(text[0])
    with open("q2_encoder_output.bin", "wb") as f:
        result.tofile(f)


