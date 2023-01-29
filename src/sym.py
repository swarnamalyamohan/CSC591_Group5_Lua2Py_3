import math
class SYM:
    def __init__(self, at, txt) -> None:
        self.n = 0
        self.has = dict()
        self.most = 0
        self.mode = None
        
        if at:
            self.at = at
        else:
            self.at = 0
        
        if txt:
            self.txt = txt
        else:
            self.txt = ""

    def add(self, x) -> None:
        if x != '?':
            self.n += 1
            if x in self.has:
                self.has[x] += 1
            else:
                self.has[x] = 1
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x
            

    def mid(self) -> str:
        return self.mode

    def div(self) -> float:
        
        def fun(p):
            return p*math.log(p,2)
        
        e = 0
        for _, n in self.has.items():
            e += fun(n/self.n)
            
        return -e
    
    def rnd(self, x, n):
        return x

    def dist(self, s1, s2):
        if s1 == "?" or s2 == "?":
            return 1
        elif s1 == s2:
            return 0
        else:
            return 1