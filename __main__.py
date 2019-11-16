import numpy as np
import sys 
import random
import copy

class nPuzzle:

    def __init__(self, g, i):

        self.g_st = g 
        self.i_st = i

        self.explored = []
        self.frontier = [self.i_st.tolist()]
        self.level = 0
    
    # accepts a list and returns a rearranged list in ascending
    def arrange(self, arr_ls):
        
        arr_ls_ = []
        for idx in range(len(arr_ls)):
            min_idx = 0
            min_val = 99999
            j = 0
            for i in arr_ls:
                if self.manhattancost(np.asarray(i)) < min_val:
                    min_idx = j
                    min_val = self.manhattancost(np.array(i))
                j += 1
            arr_ls_.append(arr_ls[min_idx])
            del arr_ls[min_idx]
        
        return arr_ls_

    # accepts a numpy array and returns a list
    def expand(self, state):
        
        prospect = []
        [r],[c] = [i.tolist() for i in list(np.where(state == 0))]

        try:
            if r != 0:
                up = copy.deepcopy(state)
                up[r][c] = up[r-1][c]
                up[r-1][c] = 0
                prospect.append(up.tolist())
        except:
            pass

        try:
            down = copy.deepcopy(state)
            down[r][c] = down[r+1][c]
            down[r+1][c] = 0
            prospect.append(down.tolist())
        except:
            pass
        
        try:
            if c != 0:
                left = copy.deepcopy(state)
                left[r][c] = left[r][c-1]
                left[r][c-1] = 0
                prospect.append(left.tolist())
        except:
            pass

        try:
            right = copy.deepcopy(state)
            right[r][c] = right[r][c+1]
            right[r][c+1] = 0
            prospect.append(right.tolist())
        except:
            pass

        return prospect
    
    # accepts a numpy array and returns integer
    def manhattancost(self, state):
        
        (r,c) = state.shape
        cost = 0
        for i in range(r):
            for j in range(c):
                t = state[i][j]
                r_t = t/r
                c_t = t%r
                cost += abs(r_t - i) + abs(c_t - j)
        return cost

if __name__ == '__main__':

    N = sys.argv[1]
    #goal node
    lsg = range(int(N))

    #initial node 
    ls = range(int(N))
    random.shuffle(ls)

    r = c = int(np.sqrt(int(N)))
    lsg = np.reshape(lsg,(r,c))
    lsi = np.reshape(ls,(r,c))

    obj = nPuzzle(lsg, lsi)

    while True:
        if len(obj.frontier)== 0:
            print('There is no solution')
            break
        #choose a leaf node and remove if from the frontier
        leaf = obj.frontier[0]
        del obj.frontier[0]
        
        if obj.manhattancost(np.asarray(leaf)) == 0:
            print obj.explored
            break
    
        # adding the node to the explored list
        if leaf not in obj.explored:
            obj.explored.append(leaf)

            # expand the chosen leaf node and add the resultant to the frontier 
            ex = obj.expand(np.asarray(leaf))
            idx = 0
            for i in ex:
                if i in obj.explored:
                    del ex[idx]
                idx += 1

            ex = obj.arrange(ex)
            obj.frontier = ex + obj.frontier
