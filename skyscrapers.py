'''Module for checking field of a game
https://github.com/MykhailoBronytskyi/Mykhailo_skyscrapers_repository.git
'''


def read_input(path: str):
    """
    Read game board file from path.
    Return list of str.

    """
    lines = []
    with open(path) as file:
        for line in file:
            lines.append(line.strip('\n'))
    return lines
# print(read_input('check.txt'))


def left_to_right_check(input_line: str, pivot: int):
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible looking to the right,
    False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 5)
    False
    """
    row = input_line[1:-1]
    last_num = -1
    visiable = 0

    for num in row:
        if int(num) > last_num:
            visiable += 1
            last_num = int(num)

    if visiable == pivot:
        return True
    return False

# print(left_to_right_check('*52314*', 1))
# print(left_to_right_check("412453*", 4))
# print(left_to_right_check("452453*", 5))


def check_not_finished_board(board: list):
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*',\
         '*?????5', '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*',\
     '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*',\
         '*5?3215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board:
        if '?' in row:
            return False
    return True


def check_uniqueness_in_rows(board: list):
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*',\
         '*553215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    for row in board[1:-1]:
        set_row = set(row[1:-1])
        if len(row[1:-1]) != len(set_row):
            return False
    return True


def check_horizontal_visibility(board: list):
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    result = True
    for row in board[1:-1]:

        for _ in ['left', 'right']:
            if row[0] == '*':
                pass
            else:
                result &= left_to_right_check(row, int(row[0]))

            row = row[::-1]

    return result


def check_columns(board: list):
    """
    Check column-wise compliance of the board for uniqueness
    (buildings of unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated
    in one function for vertical case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*',\
         '*543215', '*35214*', '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*',\
         '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """

    new_board = []
    new_row = ''

    for index in range(len(board[0])):
        for row in board:
            new_row += row[index]
        new_board.append(new_row)
        new_row = ''

    result = True & check_horizontal_visibility(new_board) & \
        check_uniqueness_in_rows(new_board)
    return result


# print(check_columns((['***21**', '412453*', '423145*',
#                       '*543215', '*35214*', '*41532*', '*2*1***'])))


def check_skyscrapers(input_path: str):
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    """
    board = read_input(input_path)
    if not check_not_finished_board(board):
        return False

    if not (check_uniqueness_in_rows(board) and check_horizontal_visibility(board)):
        return False

    if not check_columns(board):
        return False

    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # print(check_skyscrapers("check.txt"))
