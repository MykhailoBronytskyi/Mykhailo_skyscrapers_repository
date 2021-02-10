'''Module for checking field of a game'''


def read_file(path: str) -> list:
    '''Reads a board from given file into the list

    >>> read_file('check.txt')
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*', '*2*1***']

    '''
    board = []
    with open(path, 'r') as file:
        for row in file:
            board.append(row.strip('\n'))
    return board


# print(read_file('check.txt'))


def check_unfinised_board(board: list) -> bool:
    '''
    Check if skyscraper board is not finished, i.e., '?' present on the game board.
    Return True if finished, False otherwise.

    >>> check_unfinised_board(['***21**', '4?????*', '4?????*', '*?????*', '*2*1***'])
    False
    >>> check_unfinised_board(['***21**', '412453*', '423145*', '*41532*', '*2*1***'])
    True
    >>> check_unfinised_board(['***21**', '4?2453*', '423145*', '*41532*', '*2*1***'])
    False
    '''
    board = board[1:-1]

    for row in board:
        if '?' in row:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215', '*2*1***'])
    False
    """
    board = board[1:-1]

    for row in board:
        row = row[1:-1]
        # print(row, len(row), len(set(row)))
        if len(row) != len(set(row)):
            return False
    return True


def left_to_right_check(row: str, pivot: int) -> bool:
    '''
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    '''

    row = row[1:-1]
    visiable = 0
    largest = -1

    for char in row:
        num = int(char)
        if num > largest:
            visiable += 1
            largest = num

    if pivot != visiable:
        return False
    return True


def check_horizontal_visibility(board: str) -> bool:
    '''
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '*35214*', '*41532*', '*2*1***'])
    False
    '''

    result = True

    for row in board:
        for _ in ['left', 'right']:
            pivot = row[0]
            if pivot == '*':
                pass
            else:
                pivot = int(pivot)
                result &= left_to_right_check(row, pivot)
            row = row[::-1]

    return result


def check_skyscrapers(path: str) -> bool:
    '''Full check of the field for on winning combination.

    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    '''
    board = read_file(path)
    if not check_unfinised_board(board):
        return False

    new_board = []
    new_row = ''
    row_len = len(board[0])

    for char in range(row_len):
        for row in board:
            new_row += row[char]
        new_board.append(new_row)
        new_row = ''

    for game in [board, new_board]:
        if not (check_uniqueness_in_rows(game) and check_horizontal_visibility(game)):
            return False

    return True



if __name__ == '__main__':
    import doctest
    doctest.testmod()
