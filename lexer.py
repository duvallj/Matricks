COMMANDS = set(['m','k','s','g','j',\
                'i','a','u','b','v',\
                    'A','U','B','V',\
                    'q','z','o',\
                '"',"'",'y','n','p',\
                'd','~','x'])
DYADS = [['=','!'],['e','E','t','T'],\
         ['|'],['$'],['&'],['+','-'],\
         ['*','/','%'],['^'],['P','D']]

ALL_DYADS = ['=','!','e','E','t','T','|','$','&','+','-','*','/','%','^','p','d']

SCOPE = set(['[','{'])
DESCOPE = set([']','}'])


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
                args.append(parse_line(cmds[old+1:ins]))
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
            commands.append([char,parse_line(cmds[old:ins-1])])
        else:
            commands.append(char)
        ins+=1
    fuse_nums(commands)
    commands = build_dyad_tree(commands)
    return commands

def main():
    print("starting unit tests...")
    line = "((3+2)&1)+5"
    print(line)
    print(parse_line(line))
    print("done!")

if __name__ == "__main__":
    main()
