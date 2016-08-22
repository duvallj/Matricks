import copy

num_reflect = lambda num,l:~(num-l)+1

def add(matrix1, matrix2, where):
    if where=='a':
        return add_right(matrix1, matrix2)
    elif where=='b':
        return add_left(matrix1, matrix2)
    elif where=='v':
        return add_above(matrix1, matrix2)
    else:
        return add_below(matrix1, matrix2)

def shift(matrix, val, where):
    if where=='A':
        return shift_right(matrix, val)
    elif where=='B':
        return shift_left(matrix, val)
    elif where=='V':
        return shift_up(matrix, val)
    else:
        return shift_down(matrix,val)

def apply_op(matrix, op):
    if op=='Y':
        return flip_y(matrix)
    elif op=='X':
        return flip_x(matrix)
    elif op=='M':
        return turn_left(matrix)
    else:
        return turn_right(matrix)

def add_below(matrix1, matrix2):
    temp = []
    for row in matrix1:
        temp.append(copy.deepcopy(row))
    for row in matrix2:
        temp.append(copy.deepcopy(row))
    return pad(temp)

def add_above(matrix1, matrix2):
    return add_below(matrix2, matrix1)

def add_right(matrix1, matrix2):
    temp=[]
    l1=len(matrix1)
    l2=len(matrix2)
    for row in range(min(l1,l2)):
        temp.append(matrix1[row]+matrix2[row])
    for row in range(l2-l1):
        temp.append([0]*len(matrix1[0])+matrix2[l1+row])
    for row in range(l1-l2):
        temp.append(matrix1[l2+row]+[0]*len(matrix2[0]))
    return pad(temp)

def add_left(matrix1, matrix2):
    return add_right(matrix2, matrix1)

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
