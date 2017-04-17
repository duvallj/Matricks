import matrix_math as mm
import matrix_utils as uu
import lexer
import sys
import copy
import random

last_input = 0
SPECIAL_COMS = {'m','i','F','<','[','{','#'}
USED_CHARS = {'[', ']', '{', '}', 'm', 'r', 'c', 'L',
              'l', 'k', 's', 'g', 'j', 'i', 'a', 'b',
              'v', 'u', 'A', 'B', 'V', 'U', 'q', 'z',
              '"', "'", 'y', 'n', 'p', 'd', '~', 'Y',
              'X', 'M', 'R', '?', '_', 'P', 'D', '+',
              '-', '*', '/', '%', '^', '|', '$', '&', '=',
              '!', 'e', 'E', 't', 'T', '0', '1', '2',
              '3', '4', '5', '6', '7', '8', '9',
              '.', '<', '>', ',', 'C', ':', ';',
              'W', 'Q', 'N', 'S'}

MATHSET = {'+','-','*','/','%','^','|','$','=',
               '&','!','e','E','t','T'}

MATHDICT = {'+':mm.add,
            '-':mm.subtract,
            '*':mm.multiply,
            '/':mm.divide,
            '%':mm.modulus,
            '^':mm.power,
            '|':mm.bit_or,
            '$':mm.bit_xor,
            '=':mm.equals,
            '&':mm.bit_and,
            '!':mm.not_equals,
            'e':mm.less_than,
            'E':mm.less_than_oreq,
            't':mm.grea_than,
            'T':mm.grea_than_oreq}

UNMATHSET = {'~','`','_'}

UNMATHDICT = {'~':mm.bit_not,
              '`':mm.inverse,
              '_':mm.floor}

ADDSET = {'a','u','v','b'}
SHIFTSET = {'A','U','V','B'}
OPSET = {'Y','X','M','R'}
            
class Memory:
    def __init__(self):
        self.matrix = [[]]
        # I made this a class in case
        # I could store other data

        # This used to store multi-line files, but that
        # was for jumps, which are now not needed

def as_float(val):
    if isinstance(val, list):
        return mm.matrix_sum(val)
    else:
        return float(val)

def _as_matrix(val):
    if isinstance(val,list):
        if isinstance(val[0],list):
            return val
        else:
            return [val]
    else:
        return [[float(val)]]

def as_matrix(val):
    val = _as_matrix(val)
    return uu.pad(lexer.rectanglize(copy.deepcopy(val)))

def _get(row, col, mem):
    if row<0 or int(row)>=len(mem.matrix) or col<0 or int(col)>=len(mem.matrix[int(row)]):
        return 0
    return mem.matrix[int(row)][int(col)]

def _set(val, row, col, mem):
    row, col = int(row), int(col)
    for r in range(len(val)):
        for c in range(len(val[r])):
            mem.matrix[row+r][col+c] = val[r][c]
    return 0

def interpret_list(inslist,mem,index=0,_rpl_Q=10,_rpl_W=0):
    val=0
    inslist = copy.deepcopy(inslist)
    while index<len(inslist):
        val = interpret(inslist[index],mem,rpl_Q=_rpl_Q,rpl_W=_rpl_W)
        index += 1
    return val

def interpret(ins,mem,rpl_r=32,rpl_c=1,rpl_Q=10,rpl_W=0):
    cmd = ins[0]
    global program_input
    global last_input
    to_return = 0
    if cmd == '[':       # I only want for loops to pass through
        newmem = Memory()
        #newmem.instructions = copy.deepcopy(mem.instructions)
        interpret_list(ins[1],newmem,_rpl_Q=rpl_Q,_rpl_W=rpl_W)
        to_return = newmem.matrix
    elif cmd == '{':
        newmem = Memory()
        #newmem.instructions = copy.deepcopy(mem.instructions)
        newmem.matrix = copy.deepcopy(mem.matrix)
        interpret_list(ins[1],newmem,_rpl_Q=rpl_Q,_rpl_W=rpl_W)
        to_return = newmem.matrix

    if len(ins)>2: del ins[2]

    cpy = 0

    if cmd in SPECIAL_COMS:
        cpy = ins[1]
    else:
        cpy = [interpret(i,mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W) for i in ins[1]]

    cpy = copy.deepcopy(cpy)

    ins.append(cpy)
    
    if cmd == '#':
        to_return = ins[2][0]
    elif cmd in MATHSET:
        to_return= mm.apply_math(ins[2][0],ins[2][1],MATHDICT[cmd])
    elif cmd in UNMATHSET:
        to_return= mm.apply_unmath(ins[2][0],UNMATHDICT[cmd])
    elif cmd in ADDSET:
        mem.matrix = uu.add(mem.matrix,as_matrix(ins[2][0]),cmd)
        to_return= mem.matrix
    elif cmd in SHIFTSET:
        mem.matrix = uu.shift(mem.matrix,as_float(ins[2][0]),cmd)
        to_return= mem.matrix
    elif cmd in OPSET:
        mem.matrix = uu.apply_op(mem.matrix,cmd)
        to_return= mem.matrix
    elif cmd == 'r':
        to_return= rpl_r
    elif cmd == 'c':
        to_return= rpl_c
    elif cmd == 'Q':
        to_return= rpl_Q
    elif cmd == 'W':
        to_return= rpl_W
    elif cmd == 'L':
        to_return = float(len(mem.matrix))
    elif cmd == 'l':
        to_return = float(len(mem.matrix[0]))
    elif cmd == 'm':
        rows = int(as_float(interpret(ins[2][1],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W)))
        cols = int(as_float(interpret(ins[2][2],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W)))
        mem.matrix = []
        for r in range(rows):
            row = []
            for c in range(cols):
                row.append(interpret(ins[2][0],mem,rpl_r=r,rpl_c=c,rpl_Q=rpl_Q,rpl_W=rpl_W))
            mem.matrix.append(row)
        to_return= mem.matrix
    elif cmd == 'F':
        rows = int(as_float(interpret(ins[2][1],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W)))
        cols = int(as_float(interpret(ins[2][2],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W)))
        for W in range(rows):
            for Q in range(cols):
                interpret(ins[2][0],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=Q,rpl_W=W)
        to_return= 0
    elif cmd == 'k':
        mem.matrix = as_matrix(ins[2][0])
        to_return= mem.matrix
    elif cmd == 's':
        _set(as_matrix(ins[2][0]),as_float(ins[2][1]),as_float(ins[2][2]),mem)
        to_return= as_matrix(ins[2][0])
    elif cmd == 'g':
        to_return= _get(as_float(ins[2][0]),as_float(ins[2][1]),mem)
    # jumps are unecesary for now. Just use for loops
    # I plan to add them back in eventually,
    # but for now it's just too big of a hassle
    #elif cmd == 'j':
    #    to_return = 0
    #    _inslist = copy.deepcopy(mem.instructions[int(as_float(ins[2][0]))])
    #    _index = int(as_float(ins[2][1]))-1
    elif cmd == 'i':
        to_return = 0
        if as_float(interpret(ins[2][0],mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W))!=0:
            to_return = ins[2][1]
        else:
            to_return = ins[2][2]
        to_return = interpret(to_return,mem,rpl_r=rpl_r,rpl_c=rpl_c,rpl_Q=rpl_Q,rpl_W=rpl_W)
    #no use for this, just use ascii codes
    #elif cmd == '"': 
    #    pass
    elif cmd == '\'':
        print(chr(int(as_float(ins[2][0]))),end="")
        to_return = 0
    elif cmd == 'y':
        if len(program_input)==0:
            last_input = 0
            to_return= 0
        else:
            last_input = ord(program_input[0])
            program_input = program_input[1:]
            to_return= last_input
    elif cmd == 'n':
        last_input = 0
        if len(program_input)>0:
            newinput = lexer.tokenize([c for c in program_input])
            index=0
            for num in newinput:
                try:
                    nnum = float(num)
                    last_input = nnum
                    index = newinput.index(num)
                    break
                except (TypeError, ValueError):
                    continue
            if index>=len(newinput):
                program_input=''
            else:
                program_input = program_input[program_input.index(newinput[index])+len(newinput[index]):]
        to_return= last_input
    elif cmd == 'p':
        to_return= mm.matrix_product(as_matrix(ins[2][0]))
    elif cmd == 'd':
        to_return= mm.matrix_sum(as_matrix(ins[2][0]))
    elif cmd == 'P':
        to_return= mm.dot_product(as_matrix(ins[2][0]),as_matrix(ins[2][1]))
    elif cmd == 'D':
        to_return= mm.dot_sum(as_matrix(ins[2][0]),as_matrix(ins[2][1]))
    elif cmd=='q':
        mem.matrix=uu.cut_from_tl(mem.matrix,as_float(ins[2][0]),as_float(ins[2][1]))
        to_return= mem.matrix
    elif cmd=='z':
        mem.matrix=uu.cut_from_br(mem.matrix,as_float(ins[2][0]),as_float(ins[2][1]))
        to_return= mem.matrix
    elif cmd == '?':
        to_return= random.uniform(as_float(ins[2][0]),as_float(ins[2][1]))
    elif cmd == '<':
        ins[2] = [[interpret_list(col,mem,_rpl_Q=rpl_Q,_rpl_W=rpl_W) for col in row] for row in ins[2]]
        to_return = uu.pad(ins[2])
    elif cmd == 'N':
        to_return = last_input
    elif cmd == 'S':
        print(str(ins[2][0]))
        to_return = 0
    elif cmd == 'C':
        to_return = uu.contains(as_matrix(ins[2][0]), as_float(ins[2][1]))

    return to_return

def parse_args(args):
    arg_dict = {'A':'0',
                'P':'0',
                'a':'""',
                'm':'[[]]',
                'i':'""'}
    for index in range(len(args)):
        if args[index].startswith('-'):
            arg_dict[args[index][1:]] = args[index+1]

    return arg_dict

def read_file(filename):
    file = open(filename,'r')
    data = file.read()
    file.close()
    return data

def print_matrix_to_console(arg_dict, mem):
    if arg_dict['A']:
        for row in mem.matrix:
            for col in row:
                if int(col) == 0:  # some fonts can't handle null chars
                    print(' ', end='')
                else:
                    print(chr(int(col)), end='')
            print()
    elif arg_dict['P']:
        for row in mem.matrix:
            for col in row:
                print(col, end='\t')
            print()
    else:
        print(mem.matrix)

if __name__ == '__main__':
    #testprg = 'k|[m=rc4 4][a0Fk{s1QQa0u0}1 4z1 1X]'
    
    mem = Memory()
    arg_dict = parse_args(sys.argv[2:])

    import ast

    for key in arg_dict:
        arg_dict[key] = ast.literal_eval(arg_dict[key])

    if arg_dict['a'] != "":
        mem.matrix = [[ord(char) for char in line] for line in arg_dict['a'].split('\n')]
        mem.matrix = uu.pad(mem.matrix)
    else:
        mem.matrix = arg_dict['m']

    global program_input
    program_input = arg_dict['i']

    if len(sys.argv) <= 1 or sys.argv[1].startswith('-'):
        i = input(">>> ")
        while i != ".quit":
            try:
                ins = lexer.lex(i)
                interpret_list(ins, mem)
                print_matrix_to_console(arg_dict, mem)
            except Exception as e:
                print(e)
            i = input(">>> ")
    else:
        filename = sys.argv[1]
        ins = lexer.lex(read_file(filename))
        arg_dict = parse_args(sys.argv[2:])

        interpret_list(ins, mem)

        print_matrix_to_console(arg_dict, mem)
