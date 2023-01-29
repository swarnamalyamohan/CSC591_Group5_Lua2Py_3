import re
from num import NUM
from sym import SYM

class COLS:
    '''
    Factory for managing a set of NUMs or SYMs
    '''

    def __init__(self, t):
        '''
        Generate NUMs and SYMs from column names
        '''
        self.names = t
        self.all = []
        self.x = []
        self.y = []

        for n,s in enumerate(t):

            if re.search(r'^[A-Z]', s) :
                col=NUM(n,s)   
            else:
                col=SYM(n,s)    
        
            self.all.append(col)

            if s[-1]!='X':                            
                isY = re.search(r'[!+-]', s)
                if isY:
                    self.y.append(col)
                else:
                    self.x.append(col)
                
    def add(self,row):
        '''
        Update the (not skipped) columns with details from 'row'
        '''
        columns=self.x.copy()+self.y.copy()
        for col in columns:
            col.add(row.cells[col.at])