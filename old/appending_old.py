import copy
from matrix_utils_old import pad,pprint

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

def main():
    print("Running unit tests...")
    a=[[1,2,3]]
    b=[[4],[5],[6]]
    pprint(a)
    pprint(b)
    c=add_below(a,b)
    print("below")
    pprint(c)
    c=add_above(a,b)
    print("above")
    pprint(c)
    c=add_left(a,b)
    print("left")
    pprint(c)
    c=add_right(a,b)
    print("right")
    pprint(c)
    print("done")

if __name__ == "__main__":
    main()
    
