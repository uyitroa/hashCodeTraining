import numpy as np
from collections import Counter

# cannot find an optimized algorithm for hash code qualification round 2015 without backtracking

class Fill:

    def __init__(self, row, column, slot_unv, amountPool, amountServer, unvaCoord, server):
        self.row = row
        self.column = column
        self.slot_unv = slot_unv
        self.amountPool = amountPool
        self.amountServer = amountServer
        self.unvaCoord = unvaCoord
        self.server = server

        self.my_arr = np.ones((self.row, self.column), dtype=np.uint8)
        self.combo = []
        self.solution = ["x"] * self.amountServer
        self.copyServer = self.server
        self.poolpos = 0


    def fill_insideMe(self):
        self.draw_unvail()
        myline = self.find_unvailable()

        myline = self.bubbleSort(myline, "(my_list[x][1] - my_list[x][0]) < (my_list[x + 1][1] - my_list[x + 1][0])")
        self.server = self.bubbleSort(self.server, "my_list[x][0] < my_list[x][1]")

        my_condition = "my_list[x][0] == my_list[x + 1][0] and my_list[x][1] < my_list[x + 1][1]"
        self.server = self.bubbleSort(self.server, my_condition)
    
        self.list_ofCombo = myline

        poolpos = 0
        for ele in range(len(myline)):
            element = myline[ele]
            size = element[1] - element[0] + 1
            if size > 20:
                self.subset_sum(self.server, size, len(self.server) - 5)
            else:
                self.subset_sum(self.server, size)

            condition = "self.my_sum(my_list[x],1) < self.my_sum(my_list[x + 1], 1)"

            my_choice = self.bubbleSort(self.combo, condition)

            self.list_ofCombo[ele] += (self.combo,)

            
        #self.convertForOutput(my_choice, poolpos, element)

        #if poolpos + 1 < self.amountPool:
        #    poolpos += 1
        #else:
        #    poolpos = 0
        self.privileges()
        

        return self.solution


    def convertForOutput(self, server_choice, pool_server, line):
        x_start = line[0]
        server_y = line[2]

        for coord in server_choice:

            indexServer = self.copyServer.index(coord)

            string_solution = " ".join(str(x_start) + str(server_y) + str(pool_server))
            self.solution[indexServer] = string_solution
            x_start += coord[0]
        #print self.solution

    def bubbleSort(self,my_list,condition):
        for passLeft in range(len(my_list) - 1, 0, -1):
            for x in range(passLeft):
                if eval(condition):
                    my_list[x], my_list[x + 1] = my_list[x + 1], my_list[x]
        return my_list

    def my_remove(self, lst):
        # [(slot,capacity),(slot2,capacity2)]
        for x in range(len(lst)):
            coord = lst[x]
            self.server.remove(coord)

    def find_unvailable(self):
        myline = []
        for l in range(self.row):
            line = list(self.my_arr[l])
            amount = Counter(line)
            amount = amount[0]  # element named 0, not 0 position cuz dictionary
            x_s = 0

            for a in range(amount):
                getx = line.index(0)
                if getx > 0:
                    myline.append((x_s, getx - 1,l))
                    line = line[getx + 1:]
                    x_s += getx - 1
                else:
                    line = line[1:]
                    x_s += 1
            if len(line) > 0:
                myline.append((x_s, self.column - 1,l))
        return myline

    def draw_unvail(self):
        for pos in range(self.slot_unv):
            my_coord = self.unvaCoord[pos]
            self.my_arr[my_coord[0], my_coord[1]] = 0
        print self.my_arr

    def subset_sum(self, numbers, target, kek = 0, partial = []):
        s = self.my_sum(partial)

        # check if the partial sum is equals to target
        if s == target:
            self.combo.append(partial)
        if s >= target:
            return  # if we reach the number why bother to continue

        for i in range(len(numbers) - kek):
            n = numbers[i]
            remaining = numbers[i + 1:]
            self.subset_sum(remaining, target, 0, partial + [n])

    def my_sum(self, my_listofTuple, my_index = 0):
        result = 0
        for x in my_listofTuple:
            number = x[my_index]
            result +=  number
        return result
        
    def privileges(self,my_list = self.list_ofCombo, my_range = 0):
        # 
        my_count = 0
        size_ofMyD = my_list[0][1] - my_list[0][0] + 1
        for x in range(len(my_list)):
            line = my_list[x]
            poss = line[3]
            size = line[1] - line[0] + 1
            if len(poss) == 0:
                my_range += 10
                self.subset_sum(self.server, size, len(self.server) - my_range)
                self.privileges([my_list[x]],my_range)
                self.combo = self.bubbleSort(self.combo,"self.my_sum(my_list[x],1) < self.my_sum(my_list[x + 1], 1)")
                
                my_list[x][3],self.list_ofCombo[x][3] = self.combo, self.combo
            
            if len(poss) == 1:
                self.convertForOutput(poss[0],self.poolpos,line)
                if self.poolpos + 1 < self.amountPool:
                    self.poolpos += 1
                else:
                    self.poolpos = 0
                self.server.my_remove(poss[0])
                self.list_ofCombo[x] = "x"

            if size_ofMyD != size:
                if my_count <= size_ofMyD:
                    for y in range(my_count - 1, 0, -1):
                        position = x - y
                        line = my_list[position]
                        poss = line[3]
                        size = line[1] - line[0] + 1
                        self.convertForOutput(poss[my_count - y], self.poolpos, line)
                        if self.poolpos + 1 < self.amountPool:
                            
                            self.poolpos += 1
                        else:
                            self.poolpos = 0
                        self.server.my_remove([poss[my_count - y])
                        self.list_ofCombo[x] = "x"
                # idfk what i am doing mate
            
        
#if __name__ == "__main__":
row, column, num_slot_un, num_pool, num_server = 2, 5, 1, 2, 5
un_info = [(0, 0)]
server_info = [(3, 10), (3, 10), (2, 5), (1, 5), (1, 1)]
test = Fill(row, column, num_slot_un, num_pool, num_server, un_info, server_info)
print test.fill_insideMe()
