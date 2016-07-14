num_reflect = lambda num,l:~(num-l)+1

def rotate_up(matrix,up):
    return [matrix[(row+up)%len(matrix)] for row in range(len(matrix))]

def rotate_down(matrix,down):
    return [matrix[row-down] for row in range(len(matrix))]

def rotate_left(matrix,left):
    return [row[left:] + row[:left] for row in matrix]

def rotate_right(matrix,right):
    return rotate_left(matrix,num_reflect(right,len(matrix[0])))

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
