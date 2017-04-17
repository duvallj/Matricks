SCOPE = ['[','{','<']
DESCOPE = [']','}','>']

ARGS0 = {'r','c','W','Q','L','l','y','n','Y','X','M','R','N'}

ARGS1 = {'k','a','b','v','u','A','V','B','U','\'','~','_','`','p','d'}

ARGS2 = {'g','q','z','?','C',
             '=','!','e','E','t','T',
             '|','$','&','+','-','*',
             '/','%','^','P','D','j'}

ARGS3 = {'m','s','F','i'}

OTHER = {'<','>',',',' '}

#REPLACEWITH1 = set(['m','F','A','B','V','U'])

def read_file(filename):
    mfile = open(filename,'r')
    data = mfile.read().split("\n")
    mfile.close()
    return data

class Node:
    def __init__(self,cmd,pnode,numargs):
        self.cmd = cmd
        self.args = []
        self.pnode = pnode
        self.numargs = numargs

    def add_child(self,cnode):
        self.args.append(cnode)
        cnode.pnode = self
        self.numargs -= 1

    def as_list(self):
        return [self.cmd, [child.as_list() if isinstance(child,Node) else child for child in self.args]]

def numchar(st):
    return '0123456789'.count(st)>0

def tokenize(cmdstring):
    cmds = [c for c in cmdstring]
    i=0
    
    while i<len(cmds)-1:
        if ((numchar(cmds[i][0]) or cmds[i][0]=='.') and numchar(cmds[i+1]))\
           or (not(cmds[i].count('.')>0) and numchar(cmds[i][0]) and cmds[i+1]=='.'):
            cmds[i] += cmds[i+1]
            cmds = cmds[:i+1] + cmds[i+2:]
            i -= 1
        i += 1

    i=0
    #while i<len(cmds):
    #    if cmds[i]==' ':
    #        cmds = cmds[:i]+cmds[i+1:]
    #        i -= 1
    #    i += 1
    # just ignore spaces while parsing
        
    return cmds

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

def tree(cmds,endchar=None,index=0):
    pnode = None
    cmdlist = []
    while index<len(cmds):
        cmd = cmds[index]
        if cmd == endchar:
            return [cmd.as_list() for cmd in cmdlist], index
        
        numflag = False
        numargs = 0
        if cmd == ' ':
            index += 1
            continue
        elif cmd in ARGS1:
            numargs = 1
        elif cmd in ARGS2:
            numargs = 2
        elif cmd in ARGS3:
            numargs = 3
        elif not (cmd in ARGS0 or cmd in SCOPE or cmd in OTHER):
            numflag = True
        
        cnode = Node(cmd,pnode,numargs)

        if numflag:
            cnode = Node('#',pnode,0)
            cnode.args = [float(cmd)]
        elif cmd == '<':
            end = find_end(''.join(cmds[index:]))
            l = rectanglize(brace_expression(''.join(cmds[index:end+1])))
            l = [[lex(col) if col != '' else ['#', [0.0]] for col in row] for row in l]
            index = end+index
            cnode.args = l
        elif cmd in SCOPE:
            cnode.args, index = tree(cmds,endchar=DESCOPE[SCOPE.index(cmd)],index=index+1)
            
        if pnode is None:
            cmdlist.append(cnode)
            pnode = cnode
        else:
            if pnode.numargs:
                pnode.add_child(cnode)
                pnode = cnode
            while not (pnode is None) and not pnode.numargs:
                pnode = pnode.pnode
        
        index += 1
        
    return [cmd.as_list() for cmd in cmdlist], len(cmds)-1

def lex(cmdstring):
    return tree(tokenize(cmdstring))[0]

if __name__ == '__main__':
    print(lex('kC<1,2,3> 3'))
