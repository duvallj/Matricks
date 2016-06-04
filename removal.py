def cut_from_tr(matrix, down, left):
    return [row[left:] for row in matrix[down:]]

def cut_from_bl(matrix, up, right):
    return [row[:len(row)-right] for row in matrix[:len(matrix)-down]]

def shift_up(matrix, up):
    return matrix[up:]+matrix[:up]

def shift_down(matrix, down):
    return shift_up(matrix, len(matrix)-down)

def shift_right(matrix, right):
    return [shift_up(row, right) for row in matrix]

def shift_left(matrix, left):
    return [shift_down(row, left) for row in matrix]


