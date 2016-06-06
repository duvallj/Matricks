def cut_from_tl(matrix, down, left):
    return [row[int(left):] for row in matrix[int(down):]]

def cut_from_br(matrix, up, right):
    return [row[:len(row)-int(right)] for row in matrix[:len(matrix)-int(up)]]

def shift_up(matrix, up):
    return matrix[int(up):]+matrix[:int(up)]

def shift_down(matrix, down):
    return shift_up(matrix, len(matrix)-int(down))

def shift_left(matrix, right):
    return [shift_up(row, int(right)) for row in matrix]

def shift_right(matrix, left):
    return [shift_down(row, int(left)) for row in matrix]


