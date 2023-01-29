import math

class NUM:
    '''
    Summarizes a stream of numbers
    '''

    def __init__(self,at,txt) -> None:
        self.n=0
        self.mu=0
        self.m2=0
        self.lo=math.inf
        self.hi=-math.inf

        if(at):
            self.at = at
        else:
            self.at=0

        if(txt):
            self.txt = txt
            if(self.txt[-1]=='-'):
                self.w=-1
            else:
                self.w=1
        else:
            self.txt= ""

        


    def add(self,n) -> None:
        '''
        Add 'n', update lo,hi and stuff needed for standard deviation
        '''
        # print("num being added : {} with type {}".format(n, type(n)))
        if(n!='?'):
            self.n=self.n+1
            d=n-self.mu
            self.mu=self.mu+d/self.n
            self.m2=self.m2+d*(n-self.mu)
            self.lo= min(n,self.lo)
            self.hi= max(n,self.hi)
        

    def mid(self) -> float:
        '''
        Return mean
        '''
        return self.mu

    def div(self) -> float:
        '''
        Return standard deviation using Welford's algorithm http://t.ly/nn_W
        '''
        if(self.m2<0 or self.n<2):
            return 0
        else:
            return (self.m2/(self.n-1))**0.5

    def rnd(self,x,n) -> float:
        if(x=='?'):
            return x
        else:
            return round(x,n)
    
    def norm(self,n) -> float:
        if(n=='?'):
            return n
        else:
            return (n-self.lo)/(self.hi - self.lo + math.exp(-32))

    def dist(self,n1,n2) ->float:
        if(n1=='?' and n2=='?'):
            return 1
        n1=self.norm(n1)
        n2=self.norm(n2)
        if(n1=='?'):
            if(n2<0.5):
                n1=1
            else:
                n1=0

        if(n2=='?'):
            if(n1<0.5):
                n2=1
            else:
                n2=0
        return abs(n1 - n2)
        