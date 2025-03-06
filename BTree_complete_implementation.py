import sys 
import random
class BTree:
    def __init__(self, t):
        """
        Initialize BTree with degree parameter t
        """
        self.t = t
        self.root = Node(t)

    def search(self, key):
        """
        Search for key in BTree
        """
        return self.search_btree(self.root, key)

    def search_btree(self, node, key):
        """
        Auxiliary function to search for key in BTree
        """
        if node is None:
            return False
        i = node.get_index_by_key(key)  
        if node.key[i] is None:
            return False
        elif key == node.key[i]:  
            return True
        elif key< node.key[i]:
            return self.search_btree(node.link[i], key)
        else:
            return self.search_btree(node.link[i+1], key)

    def insert(self, key):
        """
        Insert key into BTree
        """
        exist = self.search(key)
        if exist:
            print(f'{key} already exists')
        else:
            # if root is full, split root
            if self.root.key_full():
                new_root = self.root.split_node()
                self.root = new_root
            self.insert_btree(self.root, key)


    def delete(self, key):
        """
        Delete key from BTree
        """
        print(f'deleting {key}')
        exist = self.search(key)
        if not exist:
            print(f'{key} does not exist')
        else:
            self.delete_btree(self.root, key, self.t)

        
    def insert_btree(self, node, key):
        """
        Auxiliary function to insert key into BTree
        """


        # 
        if node.is_leaf() and not node.key_full():
            # if node is not full
            node.add_to_key(key)    
        else:
            # get the next node to enter
            next_node = node.get_link_by_key(key)

            # if next node is full, split node
            if next_node.key_full():
                parent = next_node.split_node(node)
                next_node = parent.get_link_by_key(key)

            # recursively insert key into next node
            self.insert_btree(next_node, key)


    def delete_btree(self, node, key, t):
        """
        Auxiliary function to delete key from BTree
        """
        key_index = node.get_index_by_key(key)
        if node.is_leaf():
            # if node is leaf, can directly delete key
            node.remove_from_key(key)
        elif node.key[key_index] == key:
            # if key is found in internal node
            print("key found", key, "at index", key_index, "in internal node")

            if not node.link[key_index].key_min():
                # left child has key to be deleted
                # replace key with predecessor and delete predecessor
                print("predecessor found")
                key = self.get_predecessor(node.link[key_index])
                node.key[key_index] = key
                node = node.link[key_index]
                print("removed key", key)

            elif not node.link[key_index+1].key_min():
                # right child has key to be deleted
                # replace key with successor and delete successor
                print("successor found")
                key = self.get_successor(node.link[key_index+1])
                node.key[key_index] = key
                node = node.link[key_index+1]
                print("removed key", key)
            else:
                # if both child cannot be deleted
                # merge node
                print("both predecessor and successor are at min")
                node = self.merge_node(node, key_index)
                    
            # recursively delete key from node
            self.delete_btree(node, key, t)

        else:
            # move to next node

            if node.key[key_index] < key:
                # if key is in right subtree, child node is key_index+1, sibling is key_index
                next_node = node.link[key_index+1]
                next_node_index = key_index+1
                sibling_index = key_index
            else:
                # if key is in left subtree, child node is key_index, sibling is key_index+1
                next_node = node.link[key_index]
                next_node_index = key_index
                sibling_index = key_index+1

            if next_node.key_min():
                # if next node is at minimum number of keys

                if not node.link[sibling_index].key_min():
                    # sibling has key to be borrowed, borrow from sibling
                    sibling = node.link[sibling_index]

                    if sibling_index == key_index :
                         # borrow from left sibling
                        print("borrow from left sibling")
                       
                        next_node.key.insert(0, node.key[sibling_index])
                        next_node.link.insert(0, sibling.link[sibling.count])
                        next_node.count += 1
                        node.key[sibling_index] = sibling.key[sibling.count-1]
                        sibling.key[sibling.count-1] = None
                        sibling.link[sibling.count] = None
                        sibling.count -= 1
                    else:
                        # borrow from right sibling
                        print("borrow from right sibling")
                        
                        next_node.key[next_node.count] = node.key[key_index]
                        next_node.count += 1
                        next_node.link[next_node.count] = sibling.link.pop(0)
                        sibling.link.append(None)
                        sibling.count -= 1
                        node.key[key_index] = sibling.key.pop(0)
                        sibling.key.append(None)
                else:
                    # merge node if sibling cannot borrow
                    print("merge node")
                    next_node = self.merge_node(node, key_index)

            self.delete_btree(next_node, key, t)

    def merge_node(self, node, index):
        """
        Merge two nodes based on index
        """

        left = node.link[index]  # left node to merge
        right = node.link[index+1]  # right node to merge

        left.key[left.count] = node.key[index]  # copy key from parent to left node
        left.count += 1

        # copy keys and links from right node to left node
        for i in range(right.count):
            left.key[left.count] = right.key[i]
            left.link[left.count] = right.link[i]
            left.count += 1

        left.link[left.count] = right.link[right.count]  # copy last link from right node to left node

        # remove key and link to right node from parent node
        node.link.pop(index+1)
        node.key.pop(index)
        node.key.append(None)
        node.link.append(None)
        node.count -= 1

        if node == self.root and node.count == 0:
            # if the merged node is root and has no keys, set the left node as root
            self.root = left

        return left


    def print(self):
        """
        Pretty print the BTree
        """
        self.pretty_print(self.root)

    def pretty_print(self, node, level=0):
        """
        Auxilary function to pretty print the BTree
        """
        if node is not None:
            print(f'level {level}: {node.key} , count={node.count}')
            for i in range(node.count+1):
                self.pretty_print(node.link[i], level+1)

    def traverse(self):
        """
        Traverse the entire BTree and collect all keys
        """
        return self.traverse_btree(self.root)
    
    def traverse_btree(self, node):
        """
        Auxilary function to traverse the entire BTree recursively
        """
        result = []
        if node is not None:
            for i in range(node.count):
                result.extend(self.traverse_btree(node.link[i]))
                result.append(node.key[i])
            result.extend(self.traverse_btree(node.link[node.count]))
        return result

    def get_successor(self, node):
        """
        Get successor in subtree
        """
        while not node.is_leaf():
            node = node.link[0]
        return node.key[0]
    
    def get_predecessor(self, node):
        """
        get predecessor in subtree
        """
        while not node.is_leaf():
            node = node.link[node.count]
        return node.key[node.count-1]

    


class Node:
    def __init__(self, t):
        self.t = t
        self.count = 0
        self.key = [None for _ in range(2*t)]
        self.link = [None for _ in range(2*t)]

    def is_leaf(self):
        # check if node is leaf
        return self.link[0] is None
    
    
    def get_index_by_key(self,key):
        """
        Get index by key using binary search
        """
        left = 0
        right = self.count-1
        mid = (left+right)//2
        while left <= right:
            mid = (left+right)//2
            if self.key[mid] == key:
                return mid
            elif self.key[mid] < key:
                left = mid+1
            else:
                right = mid-1
        return mid

    def get_link_by_key(self, key):
        """
        Get next node to by key
        """

        index = self.get_index_by_key(key)
        if self.key[index] is None or key < self.key[index]:
            next_node = self.link[index]
        else:
            next_node = self.link[index+1]
        return next_node

    def add_to_key(self, key):
        """
        Add key to node
        """


        if self.count == 0:
            # if node is empty, add key to start
            self.key[0] = key
            index1 = 0
        else:
            # find index to insert key
            index1 = self.get_index_by_key(key)
            if key < self.key[index1]:
                self.key.insert(index1, key)
            else:
                self.key.insert(index1+1, key)
                index1 += 1

        self.count += 1

        # remove last key if node is full
        if len(self.key) > 2*self.t:
            self.key.pop()

        return index1

    def split_node(self, parent=None):
        """
        Split node into two by median
        """
        
        if parent is None:
            parent = Node(self.t)
            
        # create new nodes
        new_node_left = Node(self.t)
        new_node_right = Node(self.t)

        mid = self.count//2

        # copy keys and links to new nodes
        for i in range(mid):
            new_node_left.key[i] = self.key[i]
            new_node_left.link[i] = self.link[i]
            new_node_left.count += 1
        new_node_left.link[mid] = self.link[mid]

        for i in range(mid+1, self.count):
            new_node_right.key[i-mid-1] = self.key[i]
            new_node_right.link[i-mid-1] = self.link[i]
            new_node_right.count += 1

        new_node_right.link[self.count-mid-1] = self.link[self.count]

        # set median key to parent
        index = parent.add_to_key(self.key[mid])
        parent.link.pop(index)
        parent.link.insert(index, new_node_left)
        parent.link.insert(index+1, new_node_right)

        return parent

    def remove_from_key(self, key):
        """
        Remove key from node
        """
        i = self.get_index_by_key(key)

        if key == self.key[i]:
            deleted = self.key.pop(i)
            self.key.append(None)
            print("deleted", deleted)
            self.count -= 1
        else:
            print("key not found")

    def key_full(self):
        return self.count == 2*self.t-1
    
    def key_min(self):
        return self.count == self.t-1

def read_file(file_path: str) -> str:
    """
    Reads the contents of a file and returns it as a string.
    """
    f = open(file_path, 'r')
    line = f.read()
    f.close()
    return line.split("\n")

if __name__ == "__main__":
    # _, file1, file2 = sys.argv
    # text1 = read_file(file1)
    # text2 = read_file(file2)
    
    # btree = BTree(2)
    # for i in text1:
    #     btree.insert(i)
    # for i in text2:
    #     command = i.split(" ")
    #     if command[0] == "delete":
    #         btree.delete(command[1])
    #     else:
    #         btree.insert(command[1])

    # with open("output_q2.txt", "w") as f:
    #     result = btree.traverse()
    #     f.write("\n".join(result))

    btree = BTree(3)
    input_list = [i for i in range(50)]
    random.shuffle(input_list)
    for i in input_list:
        btree.insert(i)
    btree.print()








