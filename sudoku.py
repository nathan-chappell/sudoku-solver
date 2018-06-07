def is_valid(vals):
    """ no repetition of digits 1-9 """
    for tv in [vals.count(x) <= 1 for x in vals if x != 0]:
        if not tv: return False
    return True

def to_index(x,y):
    """ convert to array index """
    return (x-1)*9 + y-1

def from_index(i):
    """ convert from array index """
    return (i//9+1, i%9+1)

def in_square(x,y, u,v):
    """ determine if the indices lie in the same square """
    return (x-1)//3 == (u-1)//3 and (y-1)//3 == (v-1)//3

class Sudoku:
    def __init__(self):
        #self.table = [(x,y,-1) for x in range(1,10) for y in range(1,10)]
        self.table = []
        self.stack = []

    def set_val(self, x,y,v):
        self.table[to_index(x,y)] = (x,y,v)

    def get_val(self, x,y):
        return self.table[to_index(x,y)]

    def verify_row(self, row):
        return is_valid([v for (x,y,v) in self.table if x == row])

    def verify_col(self, col):
        return is_valid([v for (x,y,v) in self.table if y == col])

    def verify_square(self, x,y):
        return is_valid([val for (u,v,val) in self.table if in_square(x,y,u,v)])

    def verify_entry(self, x,y):
        """ to be used after updating an entry to make sure
            the table is still valid """
        return self.verify_row(x) and self.verify_row(y) and self.verify_square(x,y)

    def verify_table(self):
        for x in range(1,10):
            if not self.verify_row(x): return False
            if not self.verify_col(x): return False
        for (x,y) in [(u,v) for u in range(1,10,3) for v in range(1,10,3)]:
            if not self.verify_square(x,y): return False
        return True

    def read_table(self, fname):
        self.table = []
        with open(fname) as f:
            vals = [val for line in f.readlines() for val in line.split()]
            i = 0
            for v in vals:
                (x,y) = from_index(i)
                i += 1
                self.table.append((x,y,int(v)))

    def print_table(self):
        for x in range(1,10):
            line = ""
            for y in range(1,10):
                (cx,cy,v) = self.get_val(x,y)
                line += str(v) + " "
                if y % 3 == 0: line += " "
            print(line)
            if x % 3 == 0: print("")
        print("--------------------")


    def init_stack(self):
        for (x,y,v) in self.table:
            if v == 0: self.stack = [(x,y,v)]; break

    def is_complete(self):
        for (x,y,v) in self.table:
            if v == 0: return False
        return self.verify_table()

    def advance(self):
        """ tries to advance the solution progress by incrementing the
            value on the index at the top of the stack until a valid
            table is created.  If that can't be done, then the top is
            just popped off (i.e. goes back a node in a dfs)."""
        (x,y,v) = self.stack.pop()
        good_choice = False
        while not good_choice and v < 10:
            v += 1
            self.set_val(x,y,v % 10) #resets to 0 when v is 10
            good_choice = self.verify_table()
        if (v <= 9): 
            self.stack.append((x,y,v))
            return True
        else: return False

    def push_next_cell(self):
        if not self.stack: i = 0
        else:
            (x,y,v) = self.stack[-1]
            i = to_index(x,y)
        while i < 81:
            (x,y) = from_index(i)
            (x,y,v) = self.get_val(x,y)
            #print("i=", i, ", (x,y,v)=", (x,y,v))
            if v == 0: self.stack.append((x,y,v)); return
            else: i += 1
        print("reached the end of push function...")

    def solve_puzzle(self, filename=""):
        if filename != "": self.read_table(filename)
        #self.init_stack()
        while not self.is_complete():
            self.push_next_cell()
            advanced = False
            while not advanced:
                advanced = self.advance()
                if not self.stack: return False
                #else: print(self.stack)
            #self.print_table()
            #x = input("press enter to continue")

def test(fname='puzzle'):
    s = Sudoku()
    s.read_table(fname)
    s.solve_puzzle()
    if s.is_complete():
        print("finished:")
        s.print_table()
    else: print("failed to complete!")

if __name__ == '__main__':
    fname = input('enter filename: ')
    test(fname)

'''
    basic idea:

    do_work()
        init_stack
        while not complete:
            advance
            if stack_empty: quit

    advance()
        (x,y,v) = top of stack
        while not valid and v <= 9
            increment v
        else: return
        if valid: push_next
        else pop_stack
'''

