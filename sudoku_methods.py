import itertools

# reference code for solutions below taken from
# stack overflow: https://stackoverflow.com/questions/17605898/sudoku-checker-in-python
# geeks for geeks: https://www.geeksforgeeks.org/sudoku-backtracking-7/
# techwithtim: https://www.techwithtim.net/tutorials/python-programming/sudoku-solver-backtracking/
# medium.com: https://medium.com/swlh/this-is-how-to-create-a-simple-minesweeper-game-in-python-af02077a8de


def legal_move_check(array, number, box):

    for i in range(9):
        if array[box[0]][i] == number and box[1] != i:
            return False

    for i in range(len(array)):
        if array[i][box[1]] == number and box[0] != i:
            return False

    row = box[1] // 3
    column = box[0] // 3

    for i in range(column*3, column * 3 + 3):
        for j in range(row * 3, row * 3 + 3):
            if array[i][j] == number and (i, j) != box:
                return False

    return True


def print_sudoku_board(array):
    for row in array:
        print(row)


def find_empty_box(array):
    for i in range(len(array)):
        for j in range(len(array[0])):
            if array[i][j] == 0:
                return (i, j)

    return None


def solve_sudoku_board(array):
    solved_array = array
    empty_box = find_empty_box(solved_array)
    if not empty_box:
        return solved_array
    else:
        row, column = empty_box

    for i in range(1, 10):
        if legal_move_check(solved_array, i, (row, column)):
            solved_array[row][column] = i

            if solve_sudoku_board(solved_array):
                return solved_array

            solved_array[row][column] = 0

    return False


def verify_row(row):
    return (len(row) == 9 and sum(row) == sum(set(row)))

def verify_solution(sudoku_board):
    rows = [row for row in sudoku_board if not verify_row(row)] 
    board = list(zip(*sudoku_board))
    for i in board:
        if 0 in i:
            return False
    columns = [column for column in sudoku_board if not verify_row(column)]
    boxes = []
    for i in range(1, 9, 3):
        for j in range(1, 9, 3):
            box = list(itertools.chain(row[j:j+3]for row in board[i:i+3]))
            boxes.append(box)
    solved_boxes = [box for box in boxes if not verify_row(box)]
    return not rows or not columns or not solved_boxes
if __name__ == "__main__":

    sudoku_board = [[0 for i in range(9)] for k in range(9)]

    sudoku_board = [[3, 0, 6, 5, 0, 8, 4, 0, 0],

                    [5, 2, 0, 0, 0, 0, 0, 0, 0],

                    [0, 8, 7, 0, 0, 0, 0, 3, 1],

                    [0, 0, 3, 0, 1, 0, 0, 8, 0],

                    [9, 0, 0, 8, 6, 3, 0, 0, 5],

                    [0, 5, 0, 0, 9, 0, 6, 0, 0],

                    [1, 3, 0, 0, 0, 0, 2, 5, 0],

                    [0, 0, 0, 0, 0, 0, 0, 7, 4],
    
                    [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    print_sudoku_board(sudoku_board)
    print(verify_solution(sudoku_board))
    print("--------------------------")

    if solve_sudoku_board(sudoku_board):
        solve_sudoku_board(sudoku_board)
        print_sudoku_board(sudoku_board)
        print(verify_solution(sudoku_board))

    else:
        print("Solution not possible")
