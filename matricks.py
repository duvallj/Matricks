import matrix_math as mm
import appending as aa
import removal as rr
import shifting as ss
import lexer
import sys
import copy

program_input = ''

def rec_replace(matrx, to, fill):
    if isinstance(matrx,list):
        for x in range(len(matrx)):
            if matrx[x]==to: matrx[x] = fill
            else: rec_replace(matrx[x], to, fill)
            
class Memory:
    def __init__(self):
        self.current = [[]]
        self.instructions = []
        self.pointers = []

def as_float(val,mem):
    if str(val)=='False': ret=0
    else: ret = eval(str(val).replace('L',str(len(mem.current))).replace('l',str(len(mem.current[0]))))
    if isinstance(ret, list):
        return mm.matrix_sum(ret)
    else:
        return float(ret)

def make_matrix(formula, rows, cols, mem):
    temp = []
    for row in range(int(rows)):
        temp.append([])
        for col in range(int(cols)):
            cpy = copy.deepcopy(formula)
            rec_replace(cpy,'r',str(row))
            rec_replace(cpy,'c',str(col))
            temp[len(temp)-1].append(as_float(interpret(cpy,mem),mem))
    mem.current = temp
    return 0

def for_loop(formula, rows, cols, mem):
    for row in range(int(rows)):
        for col in range(int(cols)):
            cpy = copy.deepcopy(formula)
            rec_replace(cpy,'W',str(row))
            rec_replace(cpy,'Q',str(col))
            interpret(cpy,mem)

def as_matrix(val):
    if isinstance(val,list):
        if isinstance(val[0],list):
            return val
        else:
            return [val]
    else:
        return [[float(val)]]

def _get(row, col, mem):
    if row<0 or int(row)>=len(mem.current) or col<0 or int(col)>=len(mem.current[int(row)]):
        return 0
    return mem.current[int(row)][int(col)]

def _set(row, col, val, mem):
    mem.current[int(row)][int(col)] = val
    return 0

def interpret(line,mem,main=-1):
    global program_input
    to_return = []
    index = 0
    while index<len(line):
        cmd = line[index]
        if not isinstance(cmd,list):
            return cmd
        char = cmd[0]
        if char=='[':
            newmem = Memory()
            newmem.instructions = copy.deepcopy(mem.instructions)
            interpret(cmd[1],newmem)
            return newmem.current
        elif char=='{':
            newmem = Memory()
            newmem.instructions = copy.deepcopy(mem.instructions)
            newmem.current = copy.deepcopy(mem.current)
            interpret(cmd[1],newmem)
            return newmem.current
        if len(cmd)>2: del cmd[2]
        cmd.append(copy.deepcopy((char=='m' or char=='i') and cmd[1] or [interpret(val,mem) for val in cmd[1]]))
        rec_replace(cmd[2], 'l', str(len(mem.current[0])))
        rec_replace(cmd[2], 'L', str(len(mem.current)))
        if char=='m':
            make_matrix(cmd[2][0],as_float(interpret(cmd[2][1],mem),mem),as_float(interpret(cmd[2][2],mem),mem),mem)
        elif char=='F':
            for_loop(cmd[2][0],as_float(cmd[2][1],mem),as_float(cmd[2][2],mem),mem)
        elif char=='k':
            mem.current = as_matrix(cmd[2][0])
        elif char=='s':
            _set(int(as_float(cmd[2][0],mem)),int(as_float(cmd[2][1],mem)),as_float(cmd[2][2],mem),mem)
        elif char=='g':
            to_return.append(str(_get(as_float(cmd[2][0],mem),as_float(cmd[2][1],mem),mem)))
        elif char=='j':
            where = int(as_float(cmd[2][0],mem))
            if where == main:
                mem.pointers[where] = 0
                main=where
            line = mem.instructions[where]
            index = mem.pointers[where]-1
        elif char=='i':
            line = copy.deepcopy(line)
            to_ins=[]
            if as_float(interpret(cmd[2][0],mem),mem):
                to_ins=cmd[2][1]
            else:
                to_ins=cmd[2][2]
            for c in range(len(to_ins)-1, -1, -1):
                line.insert(index+1,to_ins[c])
        elif char=='a':
            mem.current=aa.add_right(mem.current,as_matrix(cmd[2][0]))
        elif char=='u':
            mem.current=aa.add_below(mem.current,as_matrix(cmd[2][0]))
        elif char=='b':
            mem.current=aa.add_left(mem.current,as_matrix(cmd[2][0]))
        elif char=='v':
            mem.current=aa.add_above(mem.current,as_matrix(cmd[2][0]))
        elif char=='A':
            mem.current=rr.shift_right(mem.current,as_float(cmd[2][0],mem))
        elif char=='U':
            mem.current=rr.shift_below(mem.current,as_float(cmd[2][0],mem))
        elif char=='B':
            mem.current=rr.shift_left(mem.current,as_float(cmd[2][0],mem))
        elif char=='V':
            mem.current=rr.shift_up(mem.current,as_float(cmd[2][0],mem))
        elif char=='q':
            mem.current=rr.cut_from_tl(mem.current,as_float(cmd[2][0],mem),as_float(cmd[2][1],mem))
        elif char=='z':
            mem.current=rr.cut_from_br(mem.current,as_float(cmd[2][0],mem),as_float(cmd[2][1],mem))
        elif char=='"':
            to_return.append("{}".format(ord(cmd[2][0])))
        elif char=="'":
            print(chr(int(as_float(cmd[2][0],mem))),end="")
        elif char=='y':
            if len(program_input)==0:
                to_return.append("0")
            else:
                to_return.append(str(ord(program_input[0])))
                program_input = program_input[1:]
        elif char=='n':
            if len(program_input)==0:
                to_return.append("0")
            else:
                newinput = lexer.fuse_nums([c for c in program_input])
                index=0
                for num in newinput:
                    try:
                        nnum = float(num)
                        to_return.append(str(nnum))
                        index = newinput.index(num)
                        break
                    except (TypeError, ValueError):
                        continue
                if index>=len(newinput):
                    program_input=''
                else:
                    program_input = program_input[program_input.index(newinput[index])+len(newinput[index]):]
        elif char=='p':
            to_return.append(str(mm.matrix_product(as_matrix(cmd[2][0]))))
        elif char=='d':
            to_return.append(str(mm.matrix_sum(as_matrix(cmd[2][0]))))
        elif char=='w':
            mem.current=ss.rotate_up(mem.current,as_float(cmd[2][0]))
        elif char=='x':
            mem.current=ss.rotate_down(mem.current,as_float(cmd[2][0]))
        elif char=='I':
            mem.current=ss.rotate_left(mem.current,as_float(cmd[2][0]))
        elif char=='K':
            mem.current=ss.rotate_right(mem.current,as_float(cmd[2][0]))
        elif char=='Y':
            mem.current=ss.flip_y(mem.current)
        elif char=='X':
            mem.current=ss.flip_y(mem.current)
        elif char=='M':
            mem.current=ss.turn_left(mem.current)
        elif char=='R':
            mem.current=ss.turn_right(mem.current)
        elif char=='P':
            to_return.append(mm.dot_product(as_matrix(cmd[2][0]),as_matrix(cmd[2][1])))
        elif char=='D':
            to_return.append(mm.dot_sum(as_matrix(cmd[2][0]),as_matrix(cmd[2][1])))
        elif char=='+':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.add)))
        elif char=='-':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.subtract)))
        elif char=='*':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.multiply)))
        elif char=='/':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.divide)))
        elif char=='%':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.modulus)))
        elif char=='^':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.power)))
        elif char=='&':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.bit_and)))
        elif char=='|':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.bit_or)))
        elif char=='$':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.bit_xor)))
        elif char=='~':
            to_return.append(mm.bit_not(cmd[1][0]))
        elif char=='=':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.equals)))
        elif char=='!':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.not_equals)))
        elif char=='e':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.less_than)))
        elif char=='E':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.less_than_oreq)))
        elif char=='t':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.grea_than)))
        elif char=='T':
            to_return.append(str(mm.apply_math(eval(cmd[2][0]),eval(cmd[2][1]),mm.grea_than_oreq)))
        elif char=='x':
            to_return.append(copy.deepcopy(mem.current))
        index+=1
        if main != -1:
            mem.pointers[main] = index

    if len(to_return)==0:
        return '0'
    elif isinstance(to_return[0],list):
        return to_return[0]
    else:
        return str(eval("+".join(to_return)))

def main(mem):
    mem.instructions = [lexer.parse_line(line) for line in lexer.read_file(sys.argv[1])]
    mem.pointers = [0 for x in range(len(mem.instructions))]
    mem.current = as_matrix(eval(sys.argv[2]))
    global program_input
    program_input = sys.argv[3]
    interpret(copy.deepcopy(mem.instructions[0]),mem,0)

if __name__ == "__main__":
    asciiprint=False
    prettyprint=False
    if sys.argv.count("--asciiprint"):
        asciiprint=True
        del sys.argv[sys.argv.index("--asciiprint")]
    if sys.argv.count("--prettyprint"):
        prettyprint=True
        del sys.argv[sys.argv.index("--prettyprint")]
    if len(sys.argv)==0:
        sys.argv.append("")
    if len(sys.argv)==1:
        sys.argv.append("whydontyouhaveafile.cks")
    if len(sys.argv)==2:
        sys.argv.append('[[]]')
    if len(sys.argv)==3:
        sys.argv.append('')
    mem=Memory()
    main(mem)
    if asciiprint:
        for row in mem.current:
            st=""
            for col in row:
                st+=chr(int(col))
            print(st)
    elif prettyprint:
        for row in mem.current:
            st=""
            for col in row:
                st+=str(col)+" "
            print(st)
    else:
        print(mem.current)
