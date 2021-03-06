COMMANDS = set(['m','k','s','g','j',\
                'i','a','u','b','v',\
                'A','U','B','V','q',\
                'z','o','"',"'",'y',\
                'n','p','d','~','x',\
                'w','I','K','Y','X',\
                'M','R','F','?','_',\
                'C','N'])

DYADS = [['=','!'],['e','E','t','T'],\
         ['|'],['$'],['&'],['+','-'],\
         ['*','/','%'],['^'],['P','D']]

ALL_DYADS = set(['=','!','e','E','t','T',\
                 '|','$','&','+','-','*',\
                 '/','%','^','P','D'])

SCOPE = set(['[','{','<'])
DESCOPE = set([']','}','>'])


def read_file(filename):
    mfile = open(filename,'r')
    data = mfile.read().split("\n")
    mfile.close()
    return data
    #print(filename)
    #return [filename]

def isnum(val):
    try:
        val = float(val)
        return True
    except (TypeError, ValueError):
        return False

def get(lst,pos):
    if pos<0 or pos>=len(lst): return '+'
    else: return lst[pos]

def fuse_nums(lst):
    for p in range(len(lst)-1,-1,-1):
        if isnum(get(lst,p)) and get(lst,p-1)!='"' and get(lst,p-2)!='"' and \
           (isnum(get(lst,p-1)) or \
           (get(lst,p-1)=='-' and get(lst,p-2) in ALL_DYADS) or \
            get(lst,p-1)=='.'):
            lst[p] = lst[p-1]+lst[p]
            del lst[p-1]
        elif isinstance(lst[p],list):
            fuse_nums(lst[p])
    return lst

def build_dyad_tree(lst):
    for operations in DYADS:
        t=0
        while t<len(lst):
            if lst[t]=='(':
                old=t
                t+=1
                stk=[]
                stk.append(1)
                while len(stk)>0:
                    if lst[t]=='(' and lst[t-1]!='"': stk.append(1)
                    if lst[t]==')' and lst[t-1]!='"': stk.pop()
                    t+=1
                if old==0 and t==len(lst): return build_dyad_tree(lst[1:len(lst)-1])
            if t>=len(lst): break
            for op in operations:
                if lst[t]==op:
                    return [[lst[t], [build_dyad_tree(lst[:t]), build_dyad_tree(lst[t+1:])]]]
            t+=1
    return lst

def parse_line(cmds):
    if len(cmds)==0: return ['0']
    ins=0
    last=-1
    commands=[]
    while ins<len(cmds):
        char = cmds[ins]
        if char in COMMANDS:
            args=[]
            current=':'
            while current==':':
                stk=[]
                stk.append(1)
                old=ins
                ins+=1
                while len(stk)>0:
                    if cmds[ins] in COMMANDS and cmds[ins-1]!='"':stk.append(1)
                    if (cmds[ins]==';' or (len(stk)==1 and cmds[ins]==':')) and cmds[ins-1]!='"':stk.pop()
                    ins+=1
                ins-=1
                if char!='"':args.append(parse_line(cmds[old+1:ins]))
                else: args.append(cmds[old+1:ins])
                current=cmds[ins]
                last = ins
            commands.append([char,args])
        elif char in SCOPE:
            ins+=1
            old=ins
            stk=[]
            stk.append(char)
            while len(stk)>0:
                if cmds[ins] in SCOPE and cmds[ins-1]!='"': stk.append(1)
                if cmds[ins] in DESCOPE and cmds[ins-1]!='"': stk.pop()
                ins+=1
            ins-=1
            commands.append([char,parse_line(cmds[old:ins])])
        elif char=='<': #special list building case
            end = find_end(cmds[ins:])+ins
            expr = rectanglize(brace_expression(cmds[ins:end]))
            expr = [[parse_line(col) for col in row] for row in expr]
            commands.append([char,expr])
            ins = end
        else:
            commands.append(char)
        ins+=1
    fuse_nums(commands)
    commands = build_dyad_tree(commands)
    return commands

def rectanglize(matrix):
    d = depth(matrix)
    if d==0:
        return [[matrix]]
    elif d==1:
        return [matrix]
    elif d==2:
        return matrix
    elif d>2:
        for row in range(len(matrix)):
            matrix[row] = flatten(matrix[row])
        return matrix

def flatten(v):
    if isinstance(v,list):
        return sum(list(map(flatten,v)),[])
    else:
        return [v]
    
def depth(matrix):
    if isinstance(matrix,list):
        if len(matrix)<1:
            return 1
        return max(map(depth,matrix))+1
    else:
        return 0

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

def brace_expression(s):
    h=s.count
    if h('<')<1:return s
    f,l=s.index('<'),find_end(s)
    return list(map(brace_expression,split_on_commas(s[1:len(s)-1])))

def main():
    print("starting unit test...")
    line = "mr=c:n;:n;;k9;"
    print(line)
    print(parse_line(line))
    expr = '<<>,<>,<>>'
    print(expr)
    print(brace_expression(expr))
    print("done!")

if __name__ == "__main__":
    main()
