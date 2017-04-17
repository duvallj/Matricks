import subprocess

def do_tests():
    files = {'w': 'k|[m=rc4 4][a0Fk{s1QQa0u0}1 4z1 1X]',
             'x': 'm=rc5 5k|{}{X}',
             'y': 'm=rc2 2a{X}u[m=2r2 4]',
             'z': 'mWQQFk{sc0Wsc9WscWW}Q1Y',
             'a1': 'k<1,2,3>',
             'a2': 'k<<1,2,3>,<4,5,6.7>>',
             'a3': 'k<<.8>,<<9>>,<<<10>>>>',
             'b1': 'i=1 1\'97\'98',
             'b2': 'i=1 0\'97\'98',
             'c1': 'a1b2v3u4',
             'c2': 'a1b2v3u4A1V2',
             'c3': 'a1b2v3u4B1U2',
             'd': 'm+*r7c7 7q1 2z4 3',
             'e1': 'kp<1,1,2,3,5,7>',
             'e2': 'kd<1,1,2,3,5,7>',
             'f1': 'k`~<1,2>',
             'f2': 'k~`<1,2>',
             'g1': 'm+*r4c4 4YR',
             'g2': 'm+*r4c4 4MX',
             'h1': 'k?cr',
             'h2': 'k_?cr',
             'i1': 'kC<1,2,3> 3',
             'i2': 'kC<1,2,3> 4',
             }
    for filename in files:
        file = open(filename+'.mtrx', 'w')
        file.write(files[filename])
        file.close()
    print("Files made succesfully")
    for filename in files:
        print(f"Running {filename}...")
        print(subprocess.check_output(
            'python matricks.py '+filename+'.mtrx -P 1',
            shell=True
        ))
    print("Done!")

if __name__=="__main__":
    do_tests()