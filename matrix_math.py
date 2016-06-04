import numbers

class InvalidMatrixError(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def dot_product(matrix1, matrix2):
    if len(matrix1[0])!=len(matrix2):
        raise InvalidMatrixError("Matrix {} does not have the same dimension as {}"\
                                 .format(matrix1,matrix2))
    common = len(matrix2)
    width = len(matrix1)
    height = len(matrix2[0])
    temp = [[0]*width]*height
    for row in range(height):
        for col in range(width):
            temp[row][col] = sum([matrix1[row][x]*matrix2[x][col] for x in range(common)])

    return temp


def dot_sum(matrix1, matrix2):
    if len(matrix1[0])!=len(matrix2):
        raise InvalidMatrixError("Matrix {} does not have the same dimension as {}"\
                                 .format(matrix1,matrix2))
    common = len(matrix2)
    width = len(matrix1)
    height = len(matrix2[0])
    temp = [[0]*width]*height
    for row in range(height):
        for col in range(width):
            temp[row][col] = sum([matrix1[row][x]+matrix2[x][col] for x in range(common)])

    return temp

def matrix_sum(matrix):
    acc = 0
    for row in matrix:
        for col in row:
            acc+=col
    return acc

def matrix_product(matrix):
    acc = 1
    for row in matrix:
        for col in row:
            acc*=col
    return acc

def isnum(val):
    return isinstance(val, numbers.Number)

def apply_math(val1, val2, func):
    n1= isnum(val1)
    n2= isnum(val2)
    if n1 and n2:
        return func(val1, val2)
    if n1 and not n2:
        return [[func(val1, col) for col in row] for row in val2]
    if not n1 and n2:
        return [[func(col, val2) for col in row] for row in val1]
    if not n1 and not n2:
        return [[func(val1[x][y], val2[x][y]) \
                 for y in range(min(len(val1[x]),len(val2[x])))] \
                for x in range(min(len(val1),len(val2)))]
    
def add(val1, val2):
    return val1+val2

def subtract(val1, val2):
    return val1-val2

def multiply(val1, val2):
    return val1*val2

def divide(val1, val2):
    return val1/val2
    
def modulus(val1, val2):
    return val1%val2

def power(val1, val2):
    return val1**val2

def bit_and(val1, val2):
    return val1&val2

def bit_or(val1, val2):
    return val1|val2

def bit_xor(val1, val2):
    return val1^val2

def bit_not(val):
    if isnum(val):
        return ~val
    else:
        return [[~col for col in row] for row in val]

def equals(val1, val2):
    return val1==val2

def not_equals(val1, val2):
    return val1!=val2

def less_than(val1, val2):
    return val1<val2

def less_than_oreq(val1, val2):
    return val1<=val2

def grea_than(val1, val2):
    return val1>val2

def grea_than_oreq(val1, val2):
    return val1>=val2

def main():
    print("Starting unit tests...")
    print("(no unit tests yet)")
    print("done!")
    
