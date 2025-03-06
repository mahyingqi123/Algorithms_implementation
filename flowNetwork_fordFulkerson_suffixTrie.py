"""
FIT2004 Assignment 3 Semester 2, 2022
Last edit: 21/10/2022
Author:Mah Ying Qi, 32796765, ymah0009@student.monash.edu
"""
from math import inf
from queue import Queue
from math import ceil
from math import floor

class FlowNetwork:
    """
    A flow network class that stores attributes of a flow network
    """
    def __init__(self, num_of_v, flows) -> None:
        """
        A function to initialize all the attribute variables of a flow network
        Precondition:
            num_of_v is a positive integer
            each element in the flows has the format (from, to, capacity)
        Input:
            num_of_v: Total number of vertices in flow network
            flows: A list of edges in the network
        Output, return or postcondition: A flow network and a residual network is created
        Time complexity: O(|E|+|V|), |E| = number of edges, |V| = number of vertices 
            Inserting vertices into adjacency list uses O(|V|) time
            Inserting edges into each vertices uses O(|E|) time
        Space complexity: O(|E|+|V|), |E| = number of edges, |V| = number of vertices 
            Input:  O(|E|), Input has a size of |E|
            Aux:    O(|E|+|V|), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        self.source = 3
        self.sink = 4
        self.vertices = [None for _ in range(num_of_v+1)]
        self.residual = [None for _ in range(num_of_v+1)]
        for i in range(1,num_of_v+1):
            self.vertices[i] = Vertex(i)
            self.residual[i] = Vertex(i)
        for i in flows:
            # populating flow network
            u = self.vertices[i[0]]
            v = self.vertices[i[1]]
            c = i[2]
            e1 = Edge(u,v,c)
            u.edges.append(e1)
            # populating residual network
            u = self.residual[i[0]]
            v = self.residual[i[1]]
            e2 = Edge(u,v,c)
            # match residual network edge to flow network edge 
            e2.correspond = e1
            u.edges.append(e2)
        

    def ford_fulkerson(self, day):
        """
        A function to run ford fulkerson method on the flow and residual network
        Precondition:
            A flow and a residual network is formed
        Input:
            day: Number of days we want to prepare meal
        Output, return or postcondition: The flow and residual network has been updated,
                                            An arrangement for meal preparation is returned, if available, else None.

        Time complexity: O(F|E|)), F = number of flows, |E| = number of edges, N = days * 2
            For the main loop, it will loop for F times hence time complexity is O(F)
            Inside the main loop, we run the update_network function and bfs function
            update_network has a time complexity of O(|E|) and BFS has a time complexity of O(|E|+|V|)
            Hence the overall time complexity for The main loop is O(F|E| + F|V|)

            Loop for every person has time complexity of O(1), since the number of person is fixed
            Then finding which meals they prepare has a time complexity of O(N)

            Looping to find which meals ordered by restaurant will have the time complexity of O(N)

            Hence the overall time complexity is O(F|E|)

        Space complexity: O(|V|+|E|), |V| = number of vertices, |E| = number of flows, N = days * 2
            Input:  O(1), constant space complexity
            Aux:    O(|V|+|E|), 
                    bfs has uses space complexity of O(|V|+|E|)
                    constructing the result has time complexity of O(N)
        """
        flow = 0

        # initial bfs
        path, min_flow= self.bfs()

        # Main loop
        while path is not None:

            # summing up the flow
            flow += min_flow

            # update flow network
            self.update_network(path,min_flow)
            # search for new path

            path, min_flow= self.bfs()
            
        result = ([None for _ in range(day)],[None for _ in range(day)])

        def indicator(day,num):
            """
            An indicator function that indicates whether a person is preparing breakfast or dinner
            Input:
                day: number of days
                num: day index
            Output, return or postcondition: If the person prepare dinner, return True, else false
            Time complexity: O(1)
                Constant time complexity
            Space complexity: O(1)
                Constant space complexity

            """
            if day%2 == 0:
                return num%2 == 0
            else:
                return (num+1)%2 == 0

        # loop for every person
        for i in range(6,11):
            vertex = self.vertices[i]
            # find for every person, every day they prepare a meal
            for e in vertex.edges:
                if e.flow == 1:
                    # find they breakfast or dinner 
                    for j in e.v.edges:
                        if j.flow == 1:  
                            if indicator(day,j.v.num): # they prepare dinner
                                put = 1
                            else: # they prepare breakfast
                                put = 0
                            result[put][(j.v.num-(11+day*5))//2] = i-6

        # find meals ordered from restaurant
        for i in self.vertices[5].edges:
            if i.flow == 1:  
                if indicator(day,i.v.num):
                    put = 1
                else:
                    put = 0
                result[put][(i.v.num-(11+day*5))//2] = 5
 
        return result, flow
    
            
    def update_network(self, path, min_flow):
        """
        A function to update the flow and residual network using the given path and minimum flow
        Precondition:
            a new path from source to sink has been found
        Input:
            path: A path from sink to source
            flow: The minimum flow capacity within the path
        Output, return or postcondition: The flow and residual network has been updated by adding flows in flow network, 
                                            and adding and removing flows in residual network 
        Time complexity: O(|F|), |F| = number of flows in the network
            The longest path that we can have is the one including every flow, 
            Hence by looping through the path, the time complexity will be O(|F|)
            
        Space complexity: O(|V|), |V| = number of vertices 
            Input:  O(|F|), The input is a list of flows, 
                    longest path we can have is |F| hence the space complexity is O(|F|)
            Aux:    O(1), Constant space complexity

        """
        # each element in path is an edge, loop through every edge
        for e_in_residual in path:

            # update flow network
            e_in_network = e_in_residual.correspond
            if not e_in_residual.isbackward: 
                e_in_network.flow += min_flow
            else:
                e_in_network.flow -= min_flow 

            # update residual
            if not e_in_residual.isbackward: 
                e_in_residual.capacity -= min_flow
                if e_in_residual.backward is not None:
                    e_in_residual.backward.capacity += min_flow
                else:
                    u = e_in_residual.u
                    v = e_in_residual.v
                    new_backward = Edge(v,u,min_flow)
                    new_backward.isbackward = True
                    e_in_residual.backward = new_backward
                    new_backward.backward = e_in_residual 
                    new_backward.correspond = e_in_residual.correspond
                    v.edges.append(new_backward)
            else:
                e_in_residual.capacity += min_flow
                e_in_residual.backward.capacity -= min_flow
            
    def reset_residual(self):
        """
        A function to reset the "discovered" attribute to False
        Precondition:
            a residual network is formed.
        Input:
            None
        Output, return or postcondition: All discovered attribute is set to False
        Time complexity: O(|V|), |V| = number of vertices 
            Looping through all the vertices hence loops |V| times
        Space complexity: O(1)
            Input:  O(1), constant space complexity
            Aux:    O(1), constant space complexity
        """
        for i in self.residual:
            if i is not None:
                i.discovered = False


    def bfs(self):
        """
        A function to find a path from source to sink and the minimnum flow in the path
        Precondition:
            a residual network is formed.
        Input:
            None
        Output, return or postcondition: The path from source to sink, the minimum flow in the path, if available 
        Time complexity: O(|V|+|E|), |V| = number of vertices, |E| = number of flows 
            Resetting the vertices takes O(|V|) time
            While running the breadth first search, the worst case is every vertex and every edge is went through
            Going through every vertex takes O(|V|) time
            Going through every flow takes O(|E|) time
            Reversing result list takes O(|E|) time
            Hence overall time complexity is O(|V|+|E|)
        Space complexity: O(|V|+|E|), |V| = number of vertices, |E| = number of flows 
            Input:  O(1), constant space complexity
            Aux:    O(|V|+|E|), vertices
                    Every vertex is inserted into the queue in one loop, hence O(|V|)
                    Path from source to sink went through every edge, hence O(|E|)

        """

        # reset all vertices to make them undiscovered
        self.reset_residual()

        # get starting vertex number
        start = self.source

        # get ending vertex number
        end = self.sink

        # Create a queue for bfs
        discovered = Queue()
        discovered.put(self.residual[start])  # put the starting vertex in the queue
        self.residual[start].discovered = True  # set vertex as discovered

        found = False  # variable to track whether ending vertex is found
        while not discovered.empty():  # loop as long as queue is not empty
            current_v = discovered.get()  # get the first vertex from the queue

            for e in current_v.edges:  # loop through every edges of current vertex  
                if e.capacity == 0:  # if no flow possible in this edge, proceed to next edge
                    continue

                v = e.v  # get the vertex of this edge connecting to

                if not v.discovered:  # if not discovered yet
                    v.discovered = True  # mark it as discovered
                    v.previous = e  # save this edge
                    if v.num == end:  # if it is ending vertex, sink is found
                        found = True
                        break
                    discovered.put(v)  # if it is not, put it into the queue
            
            # stop searching if sink is found
            if found:
                break

        # if sink is not found
        if not found:
            return None, None

        result = [] # list to store edges that has been went through
        min_flow = inf

        # trace back to start from end
        current = self.residual[end]
        while current.num != start:
            # put the edge in result for further process
            result.append(current.previous)

            # proceed to previous edge
            e = current.previous

            # Find minimum flow
            if e.capacity < min_flow:
                min_flow = e.capacity
            
            # proceed to previous vertex
            current = e.u

        # reverse the result list
        result.reverse()

        return result,min_flow



class Vertex:
    """
    A vertex class that stores attributes of the vertex
    """
    def __init__(self,V) -> None:
        """
        A function to initialize all the attribute variables of a vertex
        Precondition:   V is a an integer
        Input:
            V: An integer that shows the value of the vertex
            cafe: A boolean variable indicating whether the vertex is a cafe
        Output, return or postcondition: A new vertex is created
        Time complexity: O(1), no loop or repetition inside the function
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        self.num = V
        self.edges = []
        self.discovered = False
        self.previous = None


class Edge:
    """
    An edge class that stores attributes of the edge
    """
    def __init__(self, u, v, c) -> None:
        """
        A function to initialize all the attribute variables of an edge
        Precondition:   u, v, w are integer
        Input:
            u: An integer showing the value of source vertex
            v: An integer showing the value of destination vertex
        Output, return or postcondition: An edge is created
        TTime complexity: O(1), no loop or repetition inside the function
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        self.flow = 0
        self.capacity = c
        self.isbackward = False
        self.backward = None
        self.correspond = None
        self.u = u
        self.v = v

def allocate(availability):
    """
        A function to find a meal preparation schedule that suits all the housemates 

        Precondition:   availability has the format where :
                            availability[i][j]= 0 = not available for both meals on day i for person j
                            availability[i][j]= 1 = available for breakfast on day i for person j
                            availability[i][j]= 2 = available for dinner on day i for person j
                            availability[i][j]= 2 = available for both meals on day i for person j
        Input:
            availability: a data showing availability of a person to prepare a meal
        Output, return or postcondition: A schedule for every meal to be prepared by who is returned, if available 

        Time complexity: O(N^2), N = number of days, |V| = number of vertices, |E| = number of flows, |F| = number of flows
        Connecting meals to sink has a time complexity of O(N)
        Connecting intermediate to meals has a time complexity of O(N) 
        Connecting restaurant to meals has a time complexity of O(N)
        Forming a flow network has time complexity of O(|E|+|V|)
        
        Running ford fulkerson on flow network has time complexity of O(F|E|)
        Since the number of flows F will be equal to 2N, which is the number of meals to be prepared,
        and |E| will approximately be the same as N, 
        this is because the number of edges from distributor to student,
        source to distributor, acceptor to sink, source to students and source to restaurant are all constant.
        Only edges between students, intermediate and meals are varying, and they will have a maximum of 5*2N,
        which comes from each housemate has N intermediates and each intermediates has at most 2 links each connecting to breakfast or dinner.

        Hence, the overall time complexity will be O(N*N) = O(N^2) 

        Space complexity: O(N)
            Input:  O(N), Input has a length of N * 5, 
            Aux:    O(N), Ford fulkerson and network construction uses O(|V|+|E|) space, 
                        O(|V|) and O(|E|) can both be approximated to O(N), hence the space complexity is O(N)
        """
    
    # 2 meals per day
    meal_count = 2 * len(availability)
    distributor = 1
    acceptor = 2
    source = 3
    sink = 4
    restaurant = 5
    person_begin = 6

    # intermediate to ensure each student only prepare one meal a day
    intermediate = 11
    meal_start = 11 + len(availability)*5

    pairing = []

    # connect source to students 
    for i in range(5):
        pairing.append((source, i+person_begin, floor(0.36*len(availability))))
    
    # connect source to distributor
    pairing.append((source,distributor,meal_count-5*floor(0.36*len(availability))))

    # connect acceptor to sink
    pairing.append((acceptor,sink,meal_count))

    # connect meals to sink
    for i in range(meal_start,meal_start+meal_count):
        pairing.append((i, sink,1))

    # connections from intermediate to meals
    for person in range(5):
        for day in range(len(availability)):
            # connect students to intermediate
            intermediate_day = person*len(availability)+day+intermediate
            pairing.append((person+person_begin,intermediate_day,1))
            # connect intermediate to meals
            if availability[day][person] == 0:
                pass
            elif availability[day][person] == 1:
                pairing.append((intermediate_day,2*day+meal_start,1))
            elif availability[day][person] == 2:
                pairing.append((intermediate_day,2*day+1+meal_start,1))
            elif availability[day][person] == 3:
                pairing.append((intermediate_day,2*day+meal_start,1))
                pairing.append((intermediate_day,2*day+1+meal_start,1))

    # connections from restaurant to meals
    for i in range(meal_start, meal_start + meal_count):
        pairing.append((restaurant,i,1))

    # connect distributor to students
    meal_restriction = ceil(0.44*len(availability))-floor(0.36*len(availability))
    for i in range(person_begin, intermediate):
        pairing.append((distributor, i, meal_restriction))
    
    # connect distributor to restaurant
    pairing.append((1,restaurant,floor(0.1*len(availability))))

    # creating a network flow
    network = FlowNetwork(num_of_v=meal_start+meal_count, flows=pairing)
    # running ford fulkerson and get the result
    arrangement,flow = network.ford_fulkerson(len(availability))

    # if the flow does not match the number of meals
    if flow != meal_count:
        return None

    return arrangement


class Node:
    """
    A node class made for nodes in suffix tree
    """
    def __init__(self,size = 28) -> None:
        """
        A function to initialize attributes for a node
        Input:
            size: size of the child list
        Output, return or postcondition: A node is created with default value attributes
        Time complexity: O(1), Constant time complexity
        Space complexity: O(N), N = size of child list (self.link)
        """

        self.link = [None]*size
        self.from1 = False
        self.common_length = 0
        self.start = -1
        self.end = -1


class SuffixTrie:
    """
    A suffix trie class that stores the root of the suffix trie
    """
    def __init__(self) -> None:
        """
        A function to initialize attributes for a suffix trie
        Input:
            None
        Output, return or postcondition: A suffix tree root is created.
        Time complexity: O(1), Constant time complexity
        Space complexity: O(1), Constant space complexity
        """
        self.root=Node()

    # update this for suffix    
    def insert_recur(self, key, two): 
        """
        A function to insert suffixes of a string into the suffix trie
        Precondition: A suffix trie root node has been created
        Input:
            key: the string to be inserted into the suffix trie
            two: a boolean variable to indicate whethe it's the first string or not
        Output, return or postcondition: The suffixes of the string are inserted into the suffix trie
        Time complexity: O(N^2), N = length of the key
                            Inserting N suffixes with maximum of N length 
        Space complexity: O(N^2), N = length of the key
                            N number of prefixes with a maximum of N length are saved in the trie 

        """

        # insert every suffix
        for i in range(len(key)):

            current = self.root 
            # starts from root
            end = self.insert_recur_aux(key, i, current, two)

            if end-i > current.common_length and two: # check if a longer common subtring found 
                current.start = i  # record the starting index
                current.end = end  # record the ending index
                current.common_length = end - i  # record the length of common substring


    def insert_recur_aux(self, key, i, current, two):
        """
        An auxilary function for the recursive insertion function to insert suffix of a string into the suffix trie
        Precondition: A suffix trie root node has been created
        Input:
            key: the string to be inserted into the suffix trie
            i: the index of character to start from
            current: current node the function located at
            two: a boolean variable to indicate whethe it's the first string or not
        Output, return or postcondition: The suffix of the string are inserted into the suffix trie
        Time complexity: O(N), N = length of the key[i:len(key)] 
                            Inserting suffix with length N
        Space complexity: O(N), N = length of the key[i:len(key)] 
                            Suffix with length N is saved in the trie

        """
        # keep traversing if not reach the end
        if i == len(key):

            # if it is not yet a terminal
            if current.link[0] is None:
                current.link[0] = Node()  # make new terminal
                if two:
                    if current.from1: # inserting string 2 and current node is from string 1, we found the end of common 
                        end = i
                        return end
                else: # inserting string 1, mark vertex as from 1
                    current.link[0].from1 = True
            else:
                # if inserting string 2 and is common with string 1
                if two and current.from1:
                    # commmon is a terminal, return index
                    return i

            # return -11, common is not found
            return -1
        else:

            # check if it's space
            if ord(key[i]) == 32:
                index = 1
            else:
                index = ord(key[i])-97+2

            end = -1  # this variable marks the end of common

            # check if child is available
            if current.link[index] is None:

                current.link[index] = Node() # create one if not available
                if two: # inserting string 2
                    if current.from1: # current node is from string 1, we found the end of common 
                        end = i
                else:
                    current.link[index].from1 = True

            # traverse to the next node
            next_end = self.insert_recur_aux(key,i+1, current.link[index], two)
            
            # if current Node is the end of common, we want to return this index
            if end == i:
                return end

            # if current Node is not the end of common, return the number passed from lower node
            return next_end
        
def my_round(n):
    """
        A function to round the number to their nearest number
        Precondition:
            n is a number
        Input:
            n: a number to be rounded
        Output, return or postcondition: An integer rounded from n
        Time complexity: O(1), Constant time complexity
        Space complexity: O(1), Constant time complexity
    """
    if n%1 >= 0.5:
        return int(n//1 + 1)
    else:
        return int(n//1)

def compare_subs(submission1, submission2):
    """
        A function to compare two strings and return result of comparing
        Input:
            submission1: first string to be compared
            submission2: second string to be compared
        Output, return or postcondition: The longest common substring, percentage of similarity for first and second string.
        Time complexity: O(N^2 + M^2), N = length of submission 1, N = length of submission 2
        Inserting submission 1 has time complexity of N^2, 
        Inserting submission 2 has time complexity of M^2
        Getting the common substring by string slicing has the time complexity of O(N+M)
        Hence the overall time complexity is O(N^2+M^2)
        Space complexity: O(N^2 + M^2), N = length of submission 1, N = length of submission 2
        Inserting submission 1 uses space complexity of N^2, 
        Inserting submission 2 uses space complexity of M^2
        Storing the common substring has the space complexity of O(N+M)
    """
    # if one of the submission is empty
    if len(submission1) == 0 or len(submission2) == 0:
        return ['',0,0]

    # creating suffix trie
    compare_trie = SuffixTrie()

    # inserting submission 1 and submission 2 into suffix trie
    compare_trie.insert_recur(submission1,False)
    compare_trie.insert_recur(submission2,True) 

    # getting the longest common substring
    start = compare_trie.root.start
    end = compare_trie.root.end
    common_string = submission2[start:end]

    # calculating percentage of similarity
    percent1 = my_round((len(common_string)/len(submission1))*100)
    percent2 = my_round((len(common_string)/len(submission2))*100)
    return [common_string,percent1,percent2]

