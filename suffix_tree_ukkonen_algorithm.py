import sys

class Node:
    def __init__(self, is_leaf, id=None):
        # determine whether node is leaf or not
        self.is_leaf = is_leaf
        # list of edges for each character
        self.edges = [None for i in range(94)] 
        # suffix id for the suffix
        self.suffix_id = id
        self.suffix_link = None

class Edge:
    # optimized edge representation
    def __init__(self, start,end):
        # start and end of the edge
        self.start = start
        self.end = end
        self.next_node = None
        
    def get_length(self):
        if type(self.end) == End:
            return self.end.value - self.start + 1
        return self.end - self.start + 1

class End:
    # leaf is always leaf
    def __init__(self, end):
        self.value = end

class SkipCountPointer:
    # keep track of active point and use edge and length to represent remainder
    def __init__(self, node, edge, count):
        self.active_node = node
        self.active_edge = edge
        self.active_length = count

class SuffixTree:
    def __init__(self, string) -> None:
        self.end = End(-1) # global end pointer
        self.root = Node(False)
        self.root.suffix_link = self.root
        self.string = string 
        self.skip_count = SkipCountPointer(self.root, None, 0) # active point and remainder
        self.previous_node = self.root
        self.ukkonen()

    def ukkonen(self):
        """
        Construct suffix tree
        """

        self.end.value = 0
        j = 0
        # set initial previous node to root
        self.previous_node = self.root
        for i in range(0,len(self.string)):
            # rapid leaf extension
            self.rule_1()

            while j <= i:

                # if active length is 0, next edge will start with the last character
                self.skip_count.active_edge = i if self.skip_count.active_length == 0 else self.skip_count.active_edge

                # get the active edge from active node
                edge = self.skip_count.active_node.edges[ord(self.string[self.skip_count.active_edge]) - 33]

                # edge is present, traverse down the edge
                if edge is not None:

                    # if active length is greater than edge length, we need to skip count down the path to the next node
                    if self.skip_count.active_length >= edge.get_length():
                        self.skip_count_traverse(edge)
                        # restart the iteration with new active node
                        continue
                    
                    # next character of the active pointer matches
                    # rule 3, path exists in edge, showtopper to move to next phase
                    if self.string[i] == self.string[edge.start + self.skip_count.active_length]:
                        self.rule_3()
                        break

                    # rule 2 case 1, extending from edge
                    self.rule_2_case_1(edge, i,j)

                # edge is not present, create new edge
                else:
                    # rule 2 case 2, extending from active node
                    self.rule_2_case_2(i,j)

                # move to next starting
                j += 1
                
                # update skip count pointer for insertion of next substring
                self.update_skip_count_pointer(j)

    def update_skip_count_pointer(self,j):

        # if active node is root and remainder is not empty
        if self.skip_count.active_node is self.root and self.skip_count.active_length > 0:
            # adjust active length and edge as the next substring will be shorter by 1 character
            # and will start from j
            self.skip_count.active_length -= 1
            self.skip_count.active_edge = j

        # traverse to suffix link of active node to speed up traversal of the next j
        self.skip_count.active_node = self.skip_count.active_node.suffix_link


    def skip_count_traverse(self, edge):
        # move to next node
        self.skip_count.active_node = edge.next_node
        # adjust edge and length for next node
        self.skip_count.active_edge += edge.get_length()
        self.skip_count.active_length -= edge.get_length()

    def rule_1(self):
        # extend leaf using global pointer for rapid leaf extension
        self.end.value = self.end.value + 1

    def rule_2_case_1(self, edge,i,j):

        # split edge in half, create new node and edge for new substring
        new_node = Node(False)
        # create default suffix link for to root for new node
        new_node.suffix_link = self.root
        new_edge = Edge(i, self.end)

        # split original edge into two
        lower_edge = Edge(edge.start + self.skip_count.active_length, edge.end)
        lower_edge.next_node = edge.next_node

        # save j as suffix id
        new_edge.next_node = Node(True, j) 
        edge.end = edge.start + self.skip_count.active_length - 1
        new_node.edges[ord(self.string[lower_edge.start]) - 33] = lower_edge
        new_node.edges[ord(self.string[new_edge.start])-33] = new_edge
        edge.next_node = new_node

        # link previously created node to new node
        # link as they have common subtree
        if self.previous_node is not self.root:
            self.previous_node.suffix_link = new_node

        # save new node as previous node to link to next node
        self.previous_node = new_node

    def rule_2_case_2(self, i,j):

        # create new edge from active node
        new_edge = Edge(i, self.end)
        # save j as suffix id
        new_edge.next_node = Node(True, j)
        # add new edge
        self.skip_count.active_node.edges[ord(self.string[self.skip_count.active_edge]) - 33] = new_edge
        # set suffix link from previous node to active node
        # link as they have common subtree
        if self.previous_node is not self.root:
            self.previous_node.suffix_link = self.skip_count.active_node
            self.previous_node = self.root
    
    def rule_3(self):
        """
        Rule 3 of Ukkonen's algorithm
        """

        # link previous node to active node for rapid traversal
        # link as they have common subtree
        if self.previous_node is not self.root:
            self.previous_node.suffix_link = self.skip_count.active_node
            self.previous_node = self.root

        # adjust active length for next substring
        self.skip_count.active_length += 1

    def print_suffix_tree(self, node, level):
        """
        Print suffix tree
        """
        result = ""
        for i in range(len(node.edges)):
            if node.edges[i] is not None:
                end = node.edges[i].end.value if type(node.edges[i].end) == End else node.edges[i].end
                result += "\n"
                result += "|-" * level + self.string[node.edges[i].start:end+1]
                result += self.print_suffix_tree(node.edges[i].next_node, level + 1)
        return result

    def traverse_inorder(self, node):
        """
        Traverse the entire tree to get suffix id of each leaf node
        """
        # return suffix id if node is leaf
        if node.is_leaf:
            return [node.suffix_id]
        result = []
        # traverse all edges in lexicographical order
        for i in range(len(node.edges)):
            if node.edges[i] is not None:
                # combine all suffix id from all edges
                result += self.traverse_inorder(node.edges[i].next_node)
        return result

    def suffix_rank(self, node, ranks):
        """
        Map suffix id to suffix rank
        """
        ranks = [i - 1 for i in ranks]
        result = [0 for _ in range(len(ranks))]

        # traverse inorder to get build suffix array
        suffix_id = self.traverse_inorder(node)
        table = [0 for _ in range(len(suffix_id))]

        # create mapping of suffix id to suffix rank
        for i in range(len(suffix_id)):
            table[suffix_id[i]] = i + 1

        # map suffix rank to suffix id
        for i in range(len(ranks)):
            result[i] = table[ranks[i]]
        return result

def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    f = open(file_path, 'r')
    line = f.read()
    f.close()
    return line

if __name__ == "__main__":
    _, input1, input2 = sys.argv
    text = read_file(input1)
    positions = [int(i) for i in read_file(input2).split()]
    tree = SuffixTree(text)
    ranks = tree.suffix_rank(tree.root, positions)
    with open("output_q1.txt", "w") as f:
        for i in ranks:
            f.write(str(i) + "\n")
