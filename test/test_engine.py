import sys
sys.path.append("./src")

from num import NUM
from sym import SYM
from data import DATA
import utils
import main
from egs import Egs


stdoutOrigin = sys.stdout 
sys.stdout = open("./etc/out/test_engine.out", "w", encoding="utf-8")

help = '''
cluster.lua : an example csv reader script
USAGE: cluster.lua  [OPTIONS] [-g ACTION]
OPTIONS:
  -d  --dump    on crash, dump stack   = false
  -f  --file    name of file           = ../etc/data/auto93.csv
  -F  --Far     distance to "faraway"  = .95
  -g  --go      start-up action        = data
  -h  --help    show help              = false
  -m  --min     stop clusters at N^min = .5
  -p  --p       distance coefficient   = 2
  -s  --seed    random number seed     = 937162211
  -S  --Sample  sampling data size     = 512
ACTIONS:
'''

the = main.cli(main.settings(help))

tester = Egs(help)


def test1():
    utils.oo(the)
    print(the)


def test2():
    sym =SYM(None, None)
    l = ['a','a','a','a','b','b','c']
    for i in l:
        sym.add(i)
    return "a" == sym.mid() and 1.379 == utils.rnd(sym.div(), None)
    

def test3():
    num = NUM(None, None)
    l = [1,1,1,1,2,2,3]
    for n in l:
        num.add(n)
    return 11/7 == num.mid() and 0.787 == utils.rnd(num.div(), None)

def test4():
    global the
    file_path = the['file']
    data = DATA(file_path)
    # since python's indexing starts with 0 data.cols.x[0] will be 0 but in case of lua, it will be 1
    return  len(data.rows) == 398 and data.cols.y[0].w == -1 and data.cols.x[0].at == 0 and  len(data.cols.x) == 4

def test5():
    global the
    file_path = the['file']
    data1 = DATA(file_path)
    data2 = data1.clone(data1.rows)
    return (len(data1.rows) == len(data2.rows)) and (data1.cols.y[1].w == data2.cols.y[1].w) and (data1.cols.x[1].w == data2.cols.x[1].w) and (len(data1.cols.x)==len(data2.cols.x))

def test6():
    global the
    file_path = the['file']
    data = DATA(file_path)
    print(0,0,utils.o(data.rows[0].cells))
    for n,t in enumerate(data.around(data.rows[[0]])):
        if(n%50==0):
            print(n, utils.rnd(t.dist,2),utils.o(t.row.cells))

def test7():
    global the
    file_path = the['file']
    data = DATA(file_path)
    left,right,A,B,mid,c = data.half()
    print(len(left),len(right),len(data.rows))
    print(utils.o(A.cells),c)
    print(utils.o(mid.cells))
    print(utils.o(B.cells))

def test8():
    global the
    file_path = the['file']
    data = DATA(file_path)
    utils.show(data.cluster(),"mid",data.cols.y,1)

def test9():
    global the
    file_path = the['file']
    data = DATA(file_path)
    utils.show(data.sway(),"mid",data.cols.y,1)


tester.eg("the", "show settings", test1)
tester.eg("sym", "check syms", test2)
tester.eg("num", "check nums", test3)
tester.eg("data","read from csv", test4)
tester.eg("clone","duplicate structure", test5)
tester.eg("around","sorting nearest neighbors", test6)
tester.eg("half","1-level bi-clustering", test7)
tester.eg("cluster","N-level bi-clustering", test8)
tester.eg("optimize","semi-supervised optimization", test9)

main.main(the, tester.help, tester.egs)