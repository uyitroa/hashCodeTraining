import numpy as np
import time
#np.set_printoptions(threshold=np.nan)


class ExtractInput:
  def __init__(self, fileName):
    self.fileName = fileName

  def input_file(self):
    my_file = open(self.fileName, "r")
    read_myfile = my_file.read()
    my_line = read_myfile.split('\n')

    my_info = my_line[0]
    my_info = my_info.split(" ")
    my_info = self.listStr_listInt(my_info)

    my_arr = self.extrct_Arr(my_info[0], my_info[1], my_line)
    return my_info[0], my_info[1], my_info[2], my_info[3], my_arr

  def listStr_listInt(self, lst):
    new_lst = []
    for my_str in lst:
      new_lst.append(int(my_str))
    return new_lst

  def extrct_Arr(self, row, column, lst):
    my_arr = np.zeros((row, column), dtype = np.uint8)
    for pos in range(row):
      line = lst[pos + 1]
      line = line.replace("T", "1")
      line = line.replace("M", "0")
      my_arr[pos] = self.listStr_listInt(list(line))
    return my_arr



class CutSlice:
  def __init__(self, r,c,l,h,arr, demo):
    # row , column, ingre min, size max, pizza
    self.r = r
    self.c = c
    self.l = l
    self.h = h
    self.arr = arr
    self.demo = demo

  def cut_myD(self): # main function
    self.inputAnalyse()
    self.bubleSort(self.shapePos)
    self.scanArr()

    return self.solution

  def inputAnalyse(self):
    self.shapePos = []

    totalCell = []
    for x in range(2 * self.l, self.h + 1):
      totalCell.append(x)

    for number in totalCell:
      for a in range(1, number / 2 + 2):
        if (number % a == 0) and (number / a <= self.c) and (a <= self.r):
          self.shapePos.append(str(a) + "*" + str(number / a))

  def bubleSort(self,lst):
    for passLeft in range(len(lst) - 1, 0, -1):
      for x in range(passLeft):
        if eval(lst[x]) < eval(lst[x + 1]):
          lst[x], lst[x + 1] = lst[x + 1], lst[x]

    return lst

  def scanArr(self):
    x_start = 0 # scan position
    y_start = 0
    self.notFinised = False # check if there's still "cell" unchecked
    test = 0 # nothing special tbh
    solution = []
    posShape = self.shapePos
    print self.arr

    while self.notFinised:
      self.solution = solution
      print "Scanning position : ", x_start, " ", y_start

      while len(posShape) == 0 and self.notFinised: # when no possiblity shape left

        self.draw(y_start,x_start,y_start, x_start)
        if x_start + 1 < self.c: # finished that line or not
          maybeY_start = -1
          while maybeY_start == -1 and x_start + 1 < self.c: # then next column
            x_start += 1
            maybeX_start, maybeY_start = self.where_y_start(x_start) # but we don't know which line
          x_left = self.amountLeft(y_start, x_start, "x") # calculate how many column left from our position
          y_left = self.amountLeft(y_start, x_start, "y")

        if x_start + 1 >= self.c: # if no column left, then next y
            maybeX_start, maybeY_start = self.find_with_Y(y_start) # again, we don't know if there's still column unchecked before that since the shape is irregular

            if maybeX_start == -1 and self.notFinised: # if all the column are checked
              x_start, y_start, x_left, y_left = self.nextRow() # then next line
            else:
              x_start = maybeX_start
              y_start = maybeY_start

              x_left = self.amountLeft(y_start, x_start, "x")
              y_left = self.amountLeft(y_start, x_start, "y")

        posShape = self.shapePos # we need to reset the shape possibility after a new x_start and y_start
        posShape = self.scanShape(posShape,x_left, y_left) # reduce shape possibility, delete all invalid shape


      if not self.notFinised:
        break

      if self.checkMinIngre(x_start,y_start,posShape[test]): # if it's a valid shape
        x_end, y_end = self.convert(posShape[test], x_start, y_start) # x_start -> x_ebd, obvious
        x_end -= 1
        y_end -= 1

        solution.append((y_start,x_start,y_end,x_end)) # add solution
        self.draw(y_start,x_start,y_end,x_end) # add 255 to arr, which means checked

        x_left = self.amountLeft(y_start, x_end + 1, "x")

        if x_left <= 0: # if finished a line
          maybeX_start, maybeY_start = self.find_with_Y(y_start) # recheck if unchecked cell left cuz of irregular shape
          if maybeX_start == -1 and self.notFinised: # checked all
            x_start, y_start, x_left, y_left = self.nextRow()
          else:
            x_start = maybeX_start
            y_start = maybeY_start
            x_left = self.amountLeft(y_start, x_start, "x")
            y_left = self.amountLeft(y_start, x_start, "y")

        else: # line not finised
          x_start = self.c - x_left # next line idfk why i do this

          y_left = self.amountLeft(0,x_start,"y") # maybe not same line as previous one because of irregular shape
          if y_left > 0:
            y_start = self.r - y_left
          else: # if there's no line left, but still unchecked cell left then recheck from begining
            x_start, y_start = self.find_with_Y(y_start)

        posShape = self.shapePos
        posShape = self.scanShape(posShape,x_left, y_left)

      else: # not a valid shape then remove
        posShape = self.my_remove(posShape, posShape[0])

      if self.demo:
        print self.arr
        time.sleep(0.1)
    #print solution
    self.solution = solution


  def my_remove(self, my_list, word):
    # idk why but python's remove command suck
    new_list = []
    for element in my_list:
      if element != word:
        new_list.append(element)
    return new_list

  def find_with_Y(self, row):
    # recheck from begining to specific row if there's unchecked cell
    for y in range(row + 1):
      for x in range(self.c):
        if self.arr[y, x] != 255:
          return x, y
    return -1, -1

  def where_y_start(self,column):
    # next column but we don't know which line to start (irregular shape)
    for y in range(self.r):
       if self.arr[y, column] != 255:
         return column, y
    return -1, -1

  def nextRow(self):
    # next line but maybe column 0 of the next line is already checked so we need to deal with
    x_start = -1

    y_left = 0
    while y_left == 0:
      x_start += 1
      y_left = self.amountLeft(0,x_start,"y")
      y_start = self.r - y_left


    x_left = self.amountLeft(y_start,x_start,"x")

    return x_start, y_start, x_left, y_left

  def draw(self,ys,xs,ye,xe):
    # mark checked cell
    self.arr[ys:ye + 1,xs:xe +1] = 255
    self.notFinised = 1 in self.arr or 0 in self.arr


  def amountLeft(self,row,column,dir):
    # count cell left (of line or column)
    amount = 0

    if dir == "x": # check from column 0 to column at specific line
      for x in range(column,self.c):
        #print row
        if self.arr[row, x] != 255:
          amount += 1
        else:
          break

    if dir == "y": # check from 0 to row at specific column
      for y in range(row, self.r):
        if self.arr[y, column] != 255:
          amount += 1
        elif amount != 0:
          break
    return amount

  def scanShape(self, lst, xl, yl):
    # remove invalid shape: width bigger than x_left and height bigger than y_left
    new_list = []


    for ele in range(len(lst)):
      coord = lst[ele].split("*")
      a = int(coord[0])
      b = int(coord[1])

      if a <= yl and b <= xl:
        new_list.append(lst[ele])
    return new_list

  def checkMinIngre(self,x_start, y_start, shape):
    # check valid shape: enough of ingredient
    x_end, y_end = self.convert(shape,x_start, y_start)
    tomatoes = 0
    mushroom = 0

    for y in range(y_start, y_end):
      for x in range(x_start, x_end):
        if self.arr[y,x] == 1:
          tomatoes += 1
        elif self.arr[y,x] == 0:
          mushroom += 1
    if tomatoes >= self.l and mushroom >= self.l and eval(shape) <= self.h and (not 255 in self.arr[y_start:y_end, x_start:x_end]):
      return True
    else:
      return False
  def convert(self,shape,x_start, y_start):
    # convert shape to x_end and y_end first
    coord = shape.split("*")
    x_end = int(coord[1]) + x_start
    y_end = int(coord[0]) + y_start
    return x_end, y_end


def calculatePoint(my_list):
  total = 0
  for x in range(len(my_list)):
    my_tuple = my_list[x]
    total += (my_tuple[2] - my_tuple[0] + 1) * (my_tuple[3] - my_tuple[1] + 1)
  return total

def fileOutput(lst):
  outputFile = open("submit.out", "w")
  myarray = ""
  for x in range(len(lst)):
    tup = lst[x]
    myarray += str(tup[0]) + " " + str(tup[2]) + " " + str(tup[1]) + " " + str(tup[3]) + "\n"
  submit = str(len(lst)) + "\n" + myarray
  outputFile.write(submit)
  return submit

fileName = raw_input("name of file: ")
demo = int(raw_input("Demonstration? (time.sleep each loop and print array to see what is happening in each loop) 0 or 1 : "))
fileput = ExtractInput(fileName)
r,c,l,h,arr = fileput.input_file()

slice = CutSlice(r,c,l,h,arr,demo)
cut = slice.cut_myD()
print fileOutput(cut)
print calculatePoint(cut), "points out of", r * c






