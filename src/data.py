from row import ROW
from cols import COLS
import copy
import utils
import math
import the

class DATA:
    def __init__(self, src) -> None:
        self.rows = []
        self.cols = None

        self.total_values = 0


        if type(src) == str:
            self.from_csv(src)
        else:
            self.from_list(src)
    
    def add(self, t) -> None:
        if self.cols :
            # if t.cells != None :
            t = ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)
    
    def clone(self, init):
        return copy.deepcopy(self)

    def stats(self, what, cols, nPlaces):
        ret = dict()
        if cols == None:
            cols = self.cols.y

        if what == "mid":
            for col in cols :
                ret[col.txt] = col.rnd(col.mid(), nPlaces)
            return ret
        else:
            for col in cols :
                ret[col.txt] = col.rnd(col.div(), nPlaces)
            return ret

    def from_csv(self, src):
        path = src
        with open(path, "r") as csv:
            lines = csv.readlines()
            for line in lines:
                split_line = line.split(",")
                split_line = [utils.coerce(i) for i in split_line]
                self.add(split_line)
                self.total_values += len(split_line)


    
    def from_list(self, lines):
        if self.src == None:
            src = []
        
        for line in lines:
            self.add(line)

    
    def better(self, row1, row2)->bool:
        s1,s2,ys,x,y = 0, 0, self.cols.y, None, None
        num_ys = len(ys)
        for col in ys:
            x  = col.norm( row1.cells[col.at] )
            y  = col.norm( row2.cells[col.at] )
            s1 = s1 - math.exp(col.w * (x-y)/num_ys)
            s2 = s2 - math.exp(col.w * (y-x)/num_ys)
        
        return s1/num_ys < s2/num_ys

    def dist(self, row1, row2, cols = None)->float:
        n, d, ys = 0, 0, None
        
        if cols == None:
            ys = self.cols.x
        else:
            ys = cols
        
        for col in ys:
            n += 1
            d += col.dist(row1.cells[col.at], row2.cells[col.at]) ** the.p
        
        return (d/n)**(1/the.p)

    def around(self, row1, rows = None, cols = None):
        ys = rows if rows != None else self.rows
        processed_ys = []
        for y in ys:
            processed_ys.append((y, self.dist(row1, y, cols)))
        processed_ys.sort(key = lambda x:x[1])
        return processed_ys
    
    def half(self, rows = None, cols = None, above = None):
        
        def dist(row1, row2, cols):
            return self.dist(row1, row2, cols)

        def project(row, A, B, c, cols):
            return (row, utils.cosine(dist(row,A,cols), dist(row,B,cols), c))
        
        rows = rows if rows != None else self.rows
        some = utils.many(rows, the.Sample)
        A = above if above != None else utils.any(some)
        B = self.around(A, some)[int(the.Far * len(rows))][0]
        c = dist(A, B, cols)
        left, right, mid = [], [], None
        
        processed_rows = []
        for row in rows:
            processed_rows.append(project(row, A, B, c, cols))
        
        processed_rows.sort(key = lambda x:x[1])

        for n,temp in enumerate(processed_rows) :
            if n <= len(processed_rows)//2 :
                left.append(temp[0])
                mid = temp[0]
            else:
                right.append(temp[0])
        
        return left, right, A, B, mid, c

    def cluster(self, rows = None, min = None, cols = None, above = None):
        rows = rows if rows != None else self.rows
        min = min if min != None else len(rows) ** the.min
        cols = cols if cols != None else self.cols.x
        node = {"data" : self.clone(rows)}
        if len(rows) > 2*min:
            left, right, node["A"], node["B"], node["mid"], node["c"] = self.half(rows,cols,above)
            node["left"]  = self.cluster(left,  min, cols, node["A"])
            node["right"] = self.cluster(right, min, cols, node["B"])
        return node
    
    def sway(self, rows = None, min = None, cols = None, above = None):
        rows = rows if rows != None else self.rows
        min = min if min != None else len(rows) ** the.min
        cols = cols if cols != None else self.cols.x
        node = {"data" : self.clone(rows)}
        if len(rows) > 2*min:
            left, right, node["A"], node["B"], node["mid"], node["c"] = self.half(rows,cols,above)
            if self.better(node["B"], node["A"]):
                left,right,node["A"],node["B"] = right,left,node["B"],node["A"]
            node["left"]  = self.sway(left,  min, cols, node["A"])
        return node

    

