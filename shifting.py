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

def dot_range(start,stop,step):
    start=int(start)
    stop=int(stop)
    diff=(stop>start)-(start>stop)
    return list(range(start,stop+diff,int(step)*diff))

def find_end(string):
    c=1;i=d=0
    while c:
        d+=-~'<>>'.count(string[i])%3-1
        i+=1
        c=i<len(string)and 0<d
    return i

def split_on_commas(string):
    if len(string)<1:return[]
    i=0
    while i<len(string) and','!=string[i]: i+=find_end(string[i:])
    return [string[:i]] + split_on_commas(string[i+1:])

#combine=lambda a,b:[c+d for c in a for d in b]if a and b else b if not a else a

def brace_expression(s):
    h=s.count
    if h('<')<1:return[float(s)]
    f,l=s.index('<'),find_end(s)
    if h('<')<2and h('..')>0and f<1:s=s[1:len(s)-1].split('..');return dot_range(s[0],s[1],s[2])if len(s)>2else dot_range(s[0],s[1],1)
    return list(map(list,map(brace_expression,split_on_commas(s[1:len(s)-1]))))


