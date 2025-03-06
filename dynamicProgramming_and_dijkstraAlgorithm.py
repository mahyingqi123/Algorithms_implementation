"""
FIT2004 Assignment 2 Semester 2, 2022
Lasr edit: 17/9/2022
Author:Mah Ying Qi, 32796765, ymah0009@student.monash.edu
"""

from math import inf

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
        self.next = None
        self.pos = None
        self.distance = inf
        self.visited = False
        self.index = None


class Edge:
    """
    An edge class that stores attributes of the edge
    """
    def __init__(self, u, v, w) -> None:
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
        self.u = u
        self.v = v
        self.w = w

class MinHeap:
    """
    An implementation of a MinHeap Class adapted from FIT1008 Lecture
    """
    def __init__(self, max_size) -> None:
        """
        A function to initialize a MinHeap
        Precondition: max_size is an integer
        Input:
            max_size: An integer showing the maximum element the MinHeap can have
        Output, return or postcondition: An MinHeap is created
        TTime complexity: O(1), no loop or repetition inside the function
        Space complexity: O(N), N = max_size
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(N), a list of size N is created
        """
        self.length = 0
        self.the_array = [0]*max_size

    def __len__(self):
        """
        A function to return length of MinHeap
        Precondition: MinHeap is created
        Input:
            no input
        Output, return or postcondition: Length of MinHeap is returned
        TTime complexity: O(1), no loop or repetition inside the function
        Space complexity: O(1)
            Input:  O(1), No input, hence the size is constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        return self.length

    def swap(self, a, b):
        """
        A function to swap the position of two elements
        Precondition: a and b are integers
        Input:
            a: item 1 to be swapped
            b: item 2 to be swapped
        Output, return or postcondition: position of item 1 and item 2 in list are swapped
        Time complexity: O(1), no loop or repetition inside the function
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        self.the_array[a], self.the_array[b] = self.the_array[b], self.the_array[a]
        self.the_array[a].index, self.the_array[b].index = self.the_array[b].index, self.the_array[a].index
        
    def rise(self, k):
        """
        A function to rise the position of an item
        Preconditionk is an integer
        Input:
            k: An integer showing which item to be rised
        Output, return or postcondition: item k is rised to a suitable position
        Time complexity: O(logN), N = number of elements in MinHeap
                            Loops for at most logN times to reach a suitable position as maximum height is logN
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        while k>1 and self.the_array[k].distance < self.the_array[k//2].distance:
            self.swap(k,k//2)
            k = k//2

    def add(self, element):
        """
        A function to add an item
        Precondition: element is a vertex object
        Input:
            element: An vertex object to be inserted into MinHeap
        Output, return or postcondition: element is inserted at a suitable position
        Time complexity: O(logN), N = number of elements in MinHeap
                        Function calls rise which has a time complexiy of O(logN)
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        if self.length != len(self.the_array):
            self.length += 1
            element.index = self.length
            self.the_array[self.length] = element
            self.rise(self.length)

    def get_min(self):
        """
        A function to get the minimum item in the MinHeap
        Precondition: MinHeap is not empty
        Input:
            no input
        Output, return or postcondition: Smallest item in the MinHeap is returned
        Time complexity: O(logN), N = number of elements in MinHeap
                        Function calls sink which has a time complexiy of O(logN)
        Space complexity: O(1)
            Input:  O(1), No input, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        result = self.the_array[1]
        self.the_array[1] = self.the_array[self.length]
        self.length -= 1
        self.sink(1)
        return result

    def smallest_child(self, k):
        """
        A function to get the smallest child of an item
        Precondition: k is an integer
        Input:
            k: An integer to indicate which item we want to find the smallest child
        Output, return or postcondition: position of the smaller child is returned
        Time complexity: O(1), no loop or repetition inside the function
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        if 2*k == self.length or self.the_array[2*k].distance <self.the_array[2*k+1].distance:
            return 2*k
        else:
            return 2*k+1

    def sink(self, k):
        """
        A function to lower the position of an item
        Preconditionk is an integer
        Input:
            k: An integer showing which item to be lowered
        Output, return or postcondition: item k is lowered to a suitable position
        Time complexity: O(logN), N = number of elements in MinHeap
                            Loops for at most logN times to reach a suitable position 
        Space complexity: O(1)
            Input:  O(1), Input is an integer, hence the size it constant 
            Aux:    O(1), auxilary space complexity does not rely on any value, hence it has constant space complexity
        """
        while 2*k <= self.length:
            child = self.smallest_child(k)
            if self.the_array[k].distance <= self.the_array[child].distance:
                break
            self.swap(k,child)
            k = child


class RoadGraph:
    def __init__(self, roads, cafes):
        """
        A function to initialize all the attribute variables of a graph
        Precondition:  roads and cafes are valid input
        Postcondition: Two graphs are created according to the input roads
        Input:
            roads: A list of lists containing information about the set of roads
            cafes: A list of list containing information about cafe locations and waiting time
        Output, return or postcondition: Two graphs are created
        Time complexity:O(|V|+|E| |V| = numer of unique locations in roads, |E| = number of of roads
                        Searching for total number of unique locations uses O(|E|) time
                        Initializing two adjacency lists uses O(|2V|) time
                        Inserting unique locations into adjacency lists uses O(|V|) time
                        Inserting edges into adjacency lists uses O(|E|) time
                        Inserting cafes into adjacency list uses O(|V|) time
                        Hence, overall the time complexity is 
                        O(|E|+|2V|+|V|+|E|+|V|) which is O(|E|+|V).

        Space complexity: O(V+E)
            Input:  O(|E|), |E| = number of of roads
            Aux:    O(|V|+|E|), |V| = numer of unique locations in roads, |E| = number of of roads
            Created two adjacency lists with |V| number of vertices, 
            and populated the adjacency lists with |E| number of roads,
            Hence, the space complexity of the function is O(|V|+|E|)

        """
        self.z = 0

        # Find the number of unique locations(vertex) in the roads
        for (u,v,w) in roads:
            if self.z < max(u,v):
                self.z = max(u,v)
        
        # initializing two adjacency lists for two opposite graphs
        self.vertices1 = [None for _ in range(self.z+1)]
        self.vertices2 = [None for _ in range(self.z+1)]
        
        # Inserting unique locations into adjacency lists
        for i in range(self.z+1): 
            self.vertices1[i] = Vertex(i)
            self.vertices2[i] = Vertex(i)

        # Adding edges into adjacency lists
        for (u,v,w) in roads: 
            a = self.vertices1[u]
            b = self.vertices1[v]
            a.edges.append(Edge(a,b,w))
            a = self.vertices2[u]
            b = self.vertices2[v]
            b.edges.append(Edge(b,a,w))

        # Saving the cafes
        self.cafes = cafes

    def routing(self, start, end):
        """
        A function to find the shortest route from the start location to the 
        end location, going through at least 1 od the locations listed in cafes
        Precondition: start and end are valid locations
        Input:
            u: Starting location of the path
            v: Ending location of the path
        Output, return or postcondition: If the path exists, one of the shortest paths is returned, else return None
        Time complexity:O(|E|log|V|), |V| = numer of unique locations in roads, |E| = number of of roads
            Running two dijkstra algorithm has a time complexity of O(2|E|log|V|)
            Then, loop through every cafes has a worst case time complexity of O(|V|)
            Next constructing the path has a worst case time complextiy of O(|V|)
            Last, reversing the list has a worst case complexity of O(|V|)
            As a result, the overall time complexity is O(|E|log|V|)
                        
        Aux space complexity: O(|V|+|E|), |V| = numer of unique locations in roads, |E| = number of of roads
            Input:  O(1), Constant space complexity
            Aux:    O(|V|+|E|), |V| = numer of unique locations in roads, |E| = number of of roads
            Dijkstra algorithm use O(|V|) space, then path construction uses O(|V|) space as well.
            Hence, the overall space complexity is O(|V|)
        """

        if len(self.vertices1) == 1:
            return None
        
        self.dijkstra(start, 1)
        self.dijkstra(end, 2)

        path_length = inf
        cafe_choice = None

        # Find the best cafe to go through
        for i in self.cafes:
            location = self.vertices1[i[0]]
            if location.distance+i[1] + self.vertices2[i[0]].distance <path_length:
                path_length = location.distance + self.vertices2[i[0]].distance+i[1]
                cafe_choice = location

        # If no cafe is chosen return None
        if cafe_choice is None:
            return None

        path1 = []
        v = cafe_choice
        # Constructing path from start to cafe
        while v is not None:
            path1.append(v.num)
            v = v.next
        path2 = []

        if cafe_choice is not None:
            v= self.vertices2[cafe_choice.num].next

        # Constructing path from end to cafe
        while v is not None:
            path2.append(v.num)
            v = v.next
        
        path1.reverse()
        return  path1+path2



    def dijkstra(self, start,graph_num):
        """
        A dijkstra function to find the shortest route from the start location to every other locations in the graph
        Precondition: start is a valid location, graph is created
        Input:
            start: Source to start the dijkstra
            graph_num: An integer indicating which graph to run the algorithm
        Output, return or postcondition: Return
        Time complexity:O(|E|log|V|), V = unique locations in roads, E = set of roads
            Adding every locations into the MinHeap has a cost of O(|V|)
            Dijkstra algorithm has a complexity of O(|E|log|V|)
            The loop loops for |V| times to access every vertices, then loop through every edges for each vertices
            to compute the shortest distance to each locations.
            Hence, it is basically looping through every edges, which gives a time complexity of O(|E|).
            Then in each iteration of inner loop, it can perform a rise in MinHeap when updating the value, 
            this gives a complexity of O(log|V|).
            Thus, the overall time complexity for the functin is O(|E|log|V|)

        Aux space complexity: O(|V|)
            Input:  O(1), input has constant space complexity
            Aux:    O(|V|), |V| = numer of unique locations in roads, |E| = number of of roads
                    A MinHeap with size |V|, hence the space complexity is O(|V|) 
        """
        # Checking whihc graph to be used
        if graph_num == 1:
            graph = self.vertices1
        else:
            graph = self.vertices2
        
        # resetting attributes of the vertices
        for i in graph:
            i.next = None
            i.distance = inf
            i.visited = False
            i.index = None

        # Creating a MinHeap priority queue to sort the locations according to distance
        discovered = MinHeap(len(graph)+1)
        # Adding every vertex into the MinHeap
        for v in graph:
            discovered.add(v) 

        # Distance from starting location to itself is 0
        graph[start].distance = 0

        # Update the position of starting location in MinHeap
        discovered.rise(graph[start].index) 
        # Running dijkstra algorithm
        while len(discovered)>0: # Continue looping if there's still locations not visited
            current_v = discovered.get_min() 
            current_v.visited = True
            for e in current_v.edges: # Looping through every edges of the vertex
                v = e.v             
                if not v.visited and v.distance > current_v.distance + e.w: # Update the vertex if a shorter distance found
                    v.distance = current_v.distance + e.w
                    v.next = current_v
                    discovered.rise(v.index)

def optimalRoute(downhillScores, start, finish):
    """
        A function to find the shortest route from the start location to the 
        end location, going through at least 1 od the locations listed in cafes
        Precondition: start and end are valid locations
        Input:
            u: Starting location of the path
            v: Ending location of the path
        Output, return or postcondition: If the path exists, one of the shortest paths is returned, else return None
        Time complexity:O(|D|), |D| = Number of downhill segments
            Finding total number of intersection point has a time complexity of O(|D|)
            Creating an adjacency list of intersection points and downhill segments has a time complexity of O(|P|)
            Creating a memo of length |P| has a time complexity of O(|P|)
            Inserting all the downhill segments into the adjacency list has a time complexity of O(|D|)
            Counting incoming edges for each vertex has a time complexity of O(|P|)
            Inserting all vertices with no incoming edges into process list has a complexity of O(|P|)
            Sorting the vertices topologically has a complexity of O(|D|)
            Reveres the sorted list has a time complexity of O(|P|)
            Record the position for each vertex in the list has a complexity of O(|P|)
            Finding path that scores the most for each vertex from finish to start has a complexity of O(|D|)
            Constructing the solution has a complexity of O(|P|)
            As a result, the overall time complexity of the function is O(|D|) 
                        
        Aux space complexity: O(|D|), |D| = Number of downhill segments
            Input:  O(|D|), |D| = Number of downhill segments
            Aux:    O(|D|), |D| = Number of downhill segments
                    The adjacency list containing all the downhill segments has a space complexity of O(|D|)
                    The memo list has a space complextiy of O(|P|)
                    The list for recording incoming edges has a space complexity of O(|P|)
                    The process and sorted list has a space complexity of O(|P|)
                    The result list has a spcae complexity of O(|P|)

        """
    # Find the total number of intersection point
    max_num = -1
    for (a,b,c) in downhillScores: 
        if max(a,b) > max_num:
            max_num = max(a,b)
    
    # Create an adjacency list to represent the connection between the intersection points
    vertices = [Vertex(i) for i in range(max_num+1)] #O(|P|)
    
    # Create a memo for recording the optimal scores
    memo = [-inf for _ in range(max_num+1)] #O(|P|)

    # Populate the adjacency list with the available edges
    for (a,b,c) in downhillScores:#O(|D|)
        vertices[a].edges.append(Edge(vertices[a],vertices[b],c))
    
    # Counting the number of incoming edges for each vertices
    incoming_edges = [0] * len(vertices)
    for v in vertices: # O(|D|)
        for e in v.edges:
            incoming_edges[e.v.num] += 1

            
    process = []
    sorted_list = []
    
    # Put vertices that has no incoming edges into process list
    for v in range(len(incoming_edges)): # O(|P|)
        if incoming_edges[v] == 0:
            process.append(vertices[v])

    # Sort the vertices topologically
    while len(process)>0: # O(|D|)
        vertex_u = process.pop()
        sorted_list.append(vertex_u)
        for e in vertex_u.edges:
            incoming_edges[e.v.num] -= 1
            if incoming_edges[e.v.num] == 0:
                process.append(e.v)
    
    # Reverse the list so the lowest vertex is in the front
    sorted_list.reverse() # O(|P|)

    # Record the position in list for each vertex 
    for i in range(len(sorted_list)):# O(|P|)
        sorted_list[i].pos = i

    # now we have sorted list, this should map to the memo list

    # Base case, finish = start, score = 0
    memo[vertices[finish].pos] = 0

    # Finding path that scores the most for each vertex from finish to start 
    # Loop from finish to start, in topological order
    for i in range(vertices[finish].pos+1, vertices[start].pos+1): # O(|D|)
        for e in sorted_list[i].edges:
            if e.w + memo[e.v.pos] > memo[i]:
                memo[i] = e.w + memo[e.v.pos]
                sorted_list[i].next = e.v

    result = []
    k = sorted_list[vertices[start].pos]

    # Construct the solution
    while k is not None:# O(|P|)
        result.append(k.num)
        k = k.next
    
    # if the solution starts from start and ends at finish, return the result, else return None
    return result if result[0] == start and result[-1] == finish else None