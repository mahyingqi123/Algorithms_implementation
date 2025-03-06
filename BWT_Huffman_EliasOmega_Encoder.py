from bitarray import bitarray
import sys

class Decoder:
    """
    Decoder for the encoded bwt bitstream
    """
    def __init__(self, codeword) -> None:
        self.pointer = 0 # pointer to keep track of the current position in the bitstream
        self.codeword = codeword # bitstream
        self.huffman_tree = Huffman_tree() # huffman tree to decode the characters
        self.number_of_characters = 0 # number of characters in the bwt
        self.decoded_bwt = [] # decoded bwt

    def decode(self):
        """
        General function to decode the bwt bitstream
        """

        self.number_of_characters = self.decompress_elias() # decompress the elias omega code to get the number of characters
        unique_char_count = self.decompress_elias() # decompress the elias omega code to get the number of unique characters
        self.extract_character_set(unique_char_count) # decode the character set with the number of unique characters
        self.decode_characters() # decode the characters
        return self.invert_bwt() # invert the bwt to get the original string

    def decompress_elias(self):
        """
        Function to decompress elias omega code
        """
        # initialize the readlength and component
        readlength = 1
        component = self.codeword[self.pointer:self.pointer+readlength]

        # while the first bit is not 1, keep reading
        while component[0] != 1:
            component[0] = 1 # flip the first bit
            self.pointer += readlength # move the pointer
            readlength = bin_to_dec(component) +1 # get the new readlength
            component = self.codeword[self.pointer:self.pointer + readlength] # get the next set of bits

        # move the pointer to next element
        self.pointer += readlength

        # return the decimal value of the number
        return bin_to_dec(component)
    
    def extract_character_set(self, unique_char_count):
        """
        Extract the character set 
        """
        huffman_list = []

        # Extract all the characters and their huffman codes
        for _ in range(unique_char_count):
            # get the ascii of character
            character_ascii = self.codeword[self.pointer:self.pointer+7]

            # convert the ascii to character
            character = chr(bin_to_dec(character_ascii))

            # move the pointer to the code length
            self.pointer += 7

            # get the huffman code length
            huffman_code_length = self.decompress_elias()

            # get the huffman code
            huffman_code = self.codeword[self.pointer:self.pointer+huffman_code_length]

            # move the pointer to the next element
            self.pointer += huffman_code_length
            huffman_list.append((character, huffman_code))

        # build the huffman tree using the character set
        self.huffman_tree.build_tree(huffman_list)

    def decode_characters(self):
        """
        Decode the characters using the huffman tree
        """
        count = 0

        # decode the characters until the end of bistream
        while count < self.number_of_characters:
            # decode the character and move the pointer
            character, self.pointer = self.huffman_tree.decode(self.codeword, self.pointer)
            runlength = self.decompress_elias()
            count += runlength

            # append the character to the decoded bwt
            for _ in range(runlength):
                self.decoded_bwt.append(character)
        
    def invert_bwt(self):
        """
        Invert the bwt to get the original string
        """
        frequency_table = [0 for _ in range(91)]
        count_table = []

        # create frequency table and count table
        for i in self.decoded_bwt:
            frequency_table[ord(i)-36] += 1
            count_table.append(frequency_table[ord(i)-36])
        rank_table = [None for _ in range(91)]
        next = 0

        # create rank table
        for i in range(len(frequency_table)):
            if frequency_table[i] != 0:
                if next ==0 :
                    rank_table[i] = 1
                    next = frequency_table[i]
                else:
                    rank_table[i] = next
                    next = frequency_table[i] + next

        result = "$"
        pointer = 0
        # invert the bwt using LF mapping
        for i in range(len(self.decoded_bwt)-1):
            result = self.decoded_bwt[pointer] + result
            pointer = count_table[pointer] + rank_table[ord(self.decoded_bwt[pointer])-36] -1
        return result
            
        





class Huffman_tree:
    """
    Huffman tree to decode the characters
    """
    def __init__(self):
        self.root = Huffman_node(None)

    def build_tree(self, huffman_list):
        """
        build the huffman tree using the character set
        """
        for i in huffman_list:
            current_node = self.root

            for j in i[1]:
                # put 0 to left and 1 to right
                if j == 0:
                    if current_node.left is None:
                        current_node.left = Huffman_node(None)
                    current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = Huffman_node(None)
                    current_node = current_node.right
            # add the character to the leaf node
            current_node.character = i[0]

    def decode(self, codeword, pointer):
        """ 
        Decode the character using the huffman tree
        """
        current_node = self.root

        # traverse the tree until the leaf node is reached
        while current_node.character is None:
            # move to left if 0 and right if 1
            if codeword[pointer] == 0:
                current_node = current_node.left
            else:
                current_node = current_node.right
            pointer += 1
        
        return current_node.character, pointer




class Huffman_node:
    """
    Node for Huffman tree
    """
    def __init__(self, character, left=None, right=None) -> None:
        self.character = character
        self.left = left
        self.right = right


            
def bin_to_dec(binary):
    """
    Converts a binary number to a decimal number
    """
    binary = binary[::-1]
    decimal = 0
    for i in range(len(binary)):
        decimal += binary[i] * (2**i)
    return decimal
    
def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    x = bitarray()
    x.fromfile(open(file_path, "rb"))
    return x

if __name__ == "__main__":
    _, inputFile = sys.argv
    
    text = read_file(inputFile)
    decoder = Decoder(text)
    result = decoder.decode()
    with open("q2_decoder_output.txt", "w") as f:
        f.write(result)