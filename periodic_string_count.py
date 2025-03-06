import sys

def solution(alphabet_size, string_length):
    """
    
    """
    # number of strings of length N from alphabet of size A with exactly 1 distinct cycle rotation
    # is equal to size of alphabet as all the characters are same
    distinct_1 = alphabet_size

    # number of strings of length N from alphabet of size A with 2 or more distinct cycle rotations
    # is equal to the permutations of the alphabets with length N minus the distinct 1
    distinct_2 = alphabet_size ** string_length - distinct_1


    if string_length == 1:
        # if string length is 1, no cycle rotation is possible
        return distinct_2, 0, distinct_1, True
    
    # get number of periodic strings of length N with alphabet size A 
    periodic_count = calculate_periodic_count(alphabet_size, string_length)

    # number of strings of length N with exactly N distinct cycle rotations
    # is equal to the permutations of the alphabets with length N minus the number of periodic strings
    distinct_n = alphabet_size ** string_length - periodic_count


    return distinct_2, distinct_n, distinct_1, distinct_2%string_length == 0

def calculate_periodic_count(alphabet_size, string_length):
    """
    Calculate the number of periodic strings of length string_length with combination of alphabets
    """

    # get factors of string length
    factor_list = factors(string_length)

    # memoization for factor count
    factor_memo = [0 for _ in range(string_length)]

    # calculate the number of periodic strings for each factor
    for i in factor_list:

        # calculate the number of periodic strings for factor i
        factor_memo[i] = alphabet_size ** i 
        if i == 1:
            continue

        # get factors of factor
        factors_of_i = factors(i)

        # minus the number of periodic strings for subfactors to remove overlap
        for j in factors_of_i:
            factor_memo[i] -= factor_memo[j]

    # return the total number of periodic strings
    return sum(factor_memo)

def factors(n):
    """
    Find factors of number n
    """
    big_result = []
    small_result = [1]
    
    i = 2
    while i <= n**0.5: 
          
        if (n % i == 0) : 
            if (n / i == i) : 
                small_result.append(i)
            else : 
                small_result.append(i)
                big_result.append(n//i)
        i = i + 1
    # combine bigger and smaller factors
    big_result.reverse()
    return small_result+big_result

if __name__ == "__main__":

    _, alphabet_size, string_length = sys.argv
    alphabet_size = int(alphabet_size)
    string_length = int(string_length)
    res1, res2, res3, res4 = solution(alphabet_size, string_length)

    print(res1, res2, res3, res4)

