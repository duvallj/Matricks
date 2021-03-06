num_reflect = lambda num,l:~(num-l)+1

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

def flip_y(matrix):
    return [row[::-1] for row in matrix]

def flip_x(matrix):
    return matrix[::-1]

def turn_left(matrix):
    out = []
    num_cols = len(matrix[0])
    for col in range(num_cols):
        outrow = []
        for row in range(len(matrix)):
            outrow.append(matrix[row][num_reflect(col,num_cols-1)])
        out.append(outrow)
    return out

def turn_right(matrix):
    out = []
    for col in range(len(matrix[0])):
        outrow=[]
        num_rows = len(matrix)
        for row in range(num_rows):
            outrow.append(matrix[num_reflect(row,num_rows-1)][col])
        out.append(outrow)
    return out

def pad(matrix):
    row_len = max(map(len,matrix))
    out = []
    for row in matrix:
        outrow = []
        for col in row:
            outrow.append(col)
        outrow.extend([0]*(row_len-len(row)))
        out.append(outrow)
    return out

def pprint(matrix):
    for row in matrix:
        for col in row:
            print(col,end=' ')
        print('')

def contains(matrix, num):
    for row in matrix:
        for col in row:
            if col==num:
                return 1
    return 0
        
def to_string(val):
    return [[int(c) for c in str(val)]]
