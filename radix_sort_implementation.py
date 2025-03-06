"""
FIT2004 Assignment 1 Semester 2, 2022
Lasr edit: 17/8/2022
Author:Mah Ying Qi, 32796765, ymah0009@student.monash.edu
"""
def analyze(results, roster, score):
    '''
    A function that analyses the results of matches and return one list containing matches with top 10 scores, 
    and another list with matches that has the same score of higher closest score wtih given score
    Precondition:   Every element in results has the format [team1,team2,score]
                    roster matches the character set in team naming
    Postcondition:  results is modified
    :Input:
        results: A list of matches
        roster:  A number indicating how many characters are there in the team
        score: A target score to be matched
    :Output, return:   Return list containing matches with top 10 scores and list with matches that has the same score of higher closest score wtih given score
    :Time complexity:   O(NM)
        Best: O(NM), N = length of results, M = number of characters within a team
        Worst: O(NM), N = length of results, M = number of characters within a team
    Sorting characters for all teams has time complexity of O(NM) as it calls character sorting that has O(M) time complexity N times
    Generating opposite result loops through the whole list, hence having time complexity of O(N)
    Sorting according to teams calls the sort_team function hence has time complexity of O(NM)
    Sorting according to score calls the sort_score function hence has time complexity of O(N)
    Finding top 10 matches has a worst case complexity of O(N)
    Searching the matches with the score has a worst case complexity of O(N)
    As a result, the time complexity of this function is mainly on characters sorting and team sorting, 
    Hence, the time complexity is O(NM).
    :Space complexity: O(NM), N = length of results, M = number of characters within a team
        Input: O(NM), N = length of results, M = number of characters within a team
        Aux: O(NM), N = length of results, M = number of characters within a team
    Both sort_team and sort_score has auxilary space complexity of O(NM) and 
    other parts of the function has constant auxilary space complexity, hence the space complexity for the function is O(NM)
    '''
    # sort each of the characters in each strings of both teams
    for i in range(len(results)):
        results[i][0] = character_sorting(results[i][0],roster)
        results[i][1] = character_sorting(results[i][1],roster)

    
    # Generating opposite result 
    for i in range(len(results)): 
        results.append([results [i][1], results [i][0], 100 - results [i][2]])

    # sorting team2(least significant), team1, then score(most significant)
    # sorting team2
    results = sort_team(results,roster,1)
    # sorting team1
    results = sort_team(results,roster,0) 
    # counting sort on score
    results = sort_score(results)
    
    # insert the first match into output
    top10matches = [results[0]]
    # pointer for results
    i = 1

    # find the first ten matches that are not similar
    while len(top10matches) < 10 and i <len(results):
        # Check for anagram
        if top10matches[len(top10matches)-1][2] == results[i][2]:
            if same_matches(top10matches[len(top10matches)-1],results[i]):
                i += 1
                continue
        top10matches.append(results[i])

    searched_matches = []
    # binary search, return closest higher item if score is not found 
    position = binary_search(results,score)

    # append all the matches with the same score to searched_matches
    if position >= 0:
        searched_matches.append(results[position])
        position += 1
        while position <len(results) and results[position][2] == searched_matches[0][2]:
            if not same_matches(searched_matches[len(searched_matches)-1],results[position]):
                searched_matches.append(results[position])
            position += 1

    return [top10matches,searched_matches]

def same_matches(match1,match2):
    """
    Check if two matches have the same team name
    Precondition:   match1 and match2 has the format [team1,team2,score]
    Postcondition:  match1 and match2 are not modified
    :Input:
        match1: One of the match to be checked
        match2: One of the match to be checked
    :Output, return or postcondition: A boolean indicating if the matches have the same team name
    :Time complexity: O(1), single line, no loop, hence constant time complexity
    :Aux space complexity: O(1), no extra variable formed, hence constant space complexity
    """
    return (match1[0] == match2[0] and match1[1] == match2[1])

def character_sorting(string,roster): 
    """
    Sort the characters in a string alphabetically using counting sort
    Precondition:   string contains only upper case letter 
                    roster matches the character set in string
    Postcondition:  result is sorted characters in string
    :Input:
        string: A string containing uppercase alphabets
        roster: A number indicating how many characters are there
    :Output, return or postcondition:   String with sorted characters
    :Time complexity: O(M), M = length of string
        Best: O(M), M = length of string
        Worst: O(M), M = length of string
        The function loops through the whole string no matter what it is 
    :Space complexity:  O(M)
        Input: O(M), M = length of string
        Aux:  O(M), M = length of string
        A list of int with length of roster is created, 
        A string with length N is creted,
        since roster can be considered constant, hence the auxilary space completiy is O(N) 
    """
    # list for counting
    count_arr = [0 for _ in range(roster)]

    # string sorting, mapping roster to within 0-25 using -65
    for character in string:
        count_arr[ord(character)-65]+=1
    
    # forming back the string with sorted characters and return the reruslt
    result = ""
    for i in range(len(count_arr)):
        result += chr(i+65)*count_arr[i]
    return result

def sort_team(arr,roster,team):
    """
    Sort the matches in ascending order alphabetically according to team selected(team1 or team2) using radix sort
    Precondition:   Every element in results has the format [team1,team2,score]
                    roster matches the character set in team naming
                    team is 0 or 1
    Postcondition:  arr is sorted according to team chosen
    :Input:
        arr: A list of matches with the format [team1, team2, score]
        roster: A number indicating how many characters are there
        team: A number indicating which team to sort
    :Output, return or postcondition: Return a list of matches that are sorted by team1 or team2
    :Time complexity: O(NM), N = length of arr, M = number of characters in the team
        Best: O(NM), N = length of arr, M = number of characters in the team
        Worst: O(NM), N = length of arr, M = number of characters in the team
        The main loop loops for M times which is the number of characters in the team,
        then in the loop it calls the count_sort() function with time complexity of O(N) once, 
        hence calling M times count_sort gives the time complexity O(NM)
    :Space complexity: O(NM) N = length of arr, M = number of characters within a team
        input: O(NM), N = length of arr, M = number of characters within a team
        Aux :  O(NM), N = length of arr, M = number of characters within a team
        Each call of count_sort() function uses has O(NM) space complexity, 
        and it is eliminated after the exiting the function hence space complexity is O(NM)   
    """
    def count_sort(arr: list,index,team,roster):
        """
        Sort the matches in ascending order alphabetically according to index selected using counting sort
        Precondition:   Every element in results has the format [team1,team2,score]
                        roster matches the character set in team naming
                        team is 0 or 1
                        index is less than length of team name
        Postcondition:  result is arr sorted according to one character of the string of one team
        :Input:
            arr: A list of matches with the format [team1, team2, score]
            index: A number indicating which character to sort
            roster: A number indicating how many characters are there
            team: A number indicating which team to sort
        :Output, return or postcondition: Return a list of matches that are sorted by character of selected team at selected index 
        Time complexity: O(N), N = length of arr 
            Best: O(N), N = length of arr
            Worst: O(N), N = length of arr
            The function loops through the whole list no matter what the input is
        Space complexity:   N = length of arr, M = number of characters within a team
            input: O(NM), N = length of arr, M = number of characters within a team
            Aux :  O(NM), N = length of arr, M = number of characters within a team
            it creates a new list of lists which has length of 100, which is constant, 
            then put all elements in the original list into the lists of new list,
            which has a total number of N with each item having size 2N+1 (two teams + score), 
            hence the auxilary space used is 2N+1 + 100, which becomes O(N) 
        """
        # stable counting sort algorithm
        # forming temporary list with every elements
        temp_arr = [[] for _ in range(roster)]
        
        # putting elements into sorting array
        for match in arr:
            temp_arr[ord(match[team][index])-65].append(match)
           
        arr = []
        # putting elements back into the list
        for i in range(len(temp_arr)):
            for j in temp_arr[i]:
                arr.append(j)
        return arr

    length = len(arr[0][team])
    # loop for every character
    for i in range(length-1, -1, -1): # time O(NM)
        # sort using stable counting sort
        arr = count_sort(arr, i, team,roster)
    return arr

def sort_score(arr):
    """
    Sort the matches according to their score using counting sort
    Precondition:   Every element in results has the format [team1,team2,score]
    Postcondition:  arr is sorted according to score
    :Input:
        roster: A list of matches with the format [team1, team2, score]
    :Output, return or postcondition:   Return a list of matches that are sorted by score
    :Time complexity:   O(N)
        Best: O(N), N = length of arr
        Worst: O(N), N = length of arr
        The function loops through the whole list no matter what the input is
    Space complexity:   O(NM)
        input: O(NM), N = length of arr, M = number of characters within a team
        Aux :  O(NM), N = length of arr, M = number of characters within a team
        it creates a new list of lists which has length of 100, which is constant, 
        then put all elements in the original list into the lists of new list,
        which has a total number of N with each item having size 2M+1 (two teams + score), 
        hence the auxilary space used is 2N*M+N + 100, which becomes O(NM) 
    """
    
    temp_arr = [[] for _ in range(101)]

    for match in arr:
        temp_arr[match[2]].append(match)
    
    arr = []
    for i in range(len(temp_arr)-1,-1,-1):
        for match in temp_arr[i]:
            arr.append(match)
    return arr

def binary_search(arr,target):
    """
    Search for the first occurence of the results with target score or with a closest higher score
    Precondition:   Elements in arr is sorted according to the score
    Postcondition:  arr is not modified
    :Input:
        arr:    A list containing a series of matches with sorted score
        target: The target score to be searched
    :Output, return or postcondition:   Return the first occurence position of the target if the target is found, 
                                        return the first occurence position of the closest highest item to the target if target is not found  
    :Time complexity:  O(N) , N = length of arr
        Best:   O(1), occurs when target is in the middle, hence so extra steps needed
        Worst:  O(N) , N = length of arr, occurs when target is not in arr, 
                and all items in arr is bigger than target, it loops from the back of the list to the first
    :Space complexity: O(N), N = length of arr
        Input: O(N), N = length of arr
        Aux : O(1), constant aux space complexity as variables has constant size 
    """
    hi = 0
    lo = len(arr)-1
    res = None
    # Binary search to search for the first position of target
    while hi <= lo:
        mid = (hi+lo)//2
        if arr[mid][2] == target:
            res = mid
            lo = mid - 1
        elif arr[mid][2] > target:
            hi = mid + 1
        else:
            lo = mid - 1

    # If target is not found
    if res is None:
        if arr[mid][2] < target:
            # Item is greater than every element in arr, hence return -1 as marked invalid
            if mid == 0:
                return -1
            # move pointer to the item that is greater than target
            else:
                mid -= 1
        # move pointer to the first position of closest highest item to the target
        while mid >0 and arr[mid][2] == arr[mid-1][2]:
            mid -= 1
        return mid
    return res

