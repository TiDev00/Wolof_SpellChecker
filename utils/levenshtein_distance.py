
def naive_levenshtein(source: str, target: str, m: int, n: int) -> int:
    """
        Naive recursive function to find minimum edit distance between 2 string
        Parameters
        ----------
            source: str
                Source word to calculate minimum edit distance
            target: str
                Target word to calculate minimum edit distance
            m: int
                Length of source word
            n: int
                Length of target word
        Returns
        ----------
            minimum_edit_distance: int
                Distance required to convert a source string to target string
    """

    # If first string is empty, insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, ignore last characters and get count for remaining strings.
    if source[m - 1] == target[n - 1]:
        return naive_levenshtein(source, target, m - 1, n - 1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all operations and take minimum of three values.
    return 1 + min(naive_levenshtein(source, target, m, n - 1), naive_levenshtein(source, target, m - 1, n),
                   naive_levenshtein(source, target, m - 1, n - 1))


def dynamic_levenshtein(source: str, target: str) -> int:
    """
        Space efficient Dynamic Programming function to find minimum edit distance between 2 string
        Parameters
        ----------
            source: str
                Source word to calculate minimum edit distance
            target: str
                Target word to calculate minimum edit distance
        Returns
        ----------
            minimum_edit_distance: int
                Distance required to convert a source string to target string
    """
    length_src = len(source)
    length_trg = len(target)

    # Create a computations_array array to memorize result of previous computations
    computations_array = [[0 for i in range(length_src + 1)] for j in range(2)]

    # Base condition when second String is empty then we remove all characters
    for i in range(0, length_src + 1):
        computations_array[0][i] = i

    # This loop run for every character in second String
    for i in range(1, length_trg + 1):
        # This loop compares the char from second String with first String characters
        for j in range(0, length_src + 1):
            # If first String is empty then we have to perform add character operation to get second String
            if j == 0:
                computations_array[i % 2][j] = i
            # If character from both String is same then we do not perform any operation
            # here i % 2 is for bound the row number
            elif source[j - 1] == target[i - 1]:
                computations_array[i % 2][j] = computations_array[(i - 1) % 2][j - 1]
            # If character from both String is not same then we take the minimum from three specified operation
            else:
                computations_array[i % 2][j] = (1 + min(computations_array[(i - 1) % 2][j],
                                                        min(computations_array[i % 2][j - 1],
                                                            computations_array[(i - 1) % 2][j - 1])))

    return computations_array[length_trg % 2][length_src]


