import numpy as np
import time

arr = np.array([[1,0,1,1,0,1,0,0],[1,0,1,1,1,0,0,1],[1,0,1,1,1,0,0,1],[1,1,1,1,0,0,1,1],[0,0,0,0,1,1,0,1],[1,1,1,0,0,1,0,1],[0,1,0,1,0,1,0,1]])
print arr
np.set_printoptions(threshold = np.nan)
r,c,l,h = 7,8,3,8

class cutSlice:
  def __init__(self, r,c,l,h,arr):
    self.r = r
    self.c = c
    self.l = l
    self.h = h
    self.arr = arr

    self.inputAnalyse()
    self.bubleSort(self.shapePos)
    self.scanArr()

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
    x_start = 0
    y_start = 0
    self.notFinised = 1 in self.arr or 0 in self.arr
    test = 0
    solution = []
    posShape = self.shapePos
    #myShape = self.shapePos # save sel.shapePos

    while self.notFinised:

      while len(posShape) == 0 and self.notFinised:

        self.draw(y_start,x_start,y_start, x_start)
        if x_start + 1 < self.c:
          x_start += 1
        else:
            maybeX_start, maybeY_start = self.find(y_start)
            if maybeX_start == -1 and self.notFinised:
              x_start, y_start, x_left, y_left = self.nextRow()
            else:
              x_start = maybeX_start
              y_start = maybeY_start
        x_left = self.amountLeft(y_start, x_start, "x")
        y_left = self.amountLeft(y_start, x_start, "y")
        posShape = self.shapePos
        posShape = self.scanShape(posShape,x_left, y_left)


      if not self.notFinised:
        break

      if self.checkMinIngre(x_start,y_start,posShape[test]):
        x_end, y_end = self.convert(posShape[test], x_start, y_start)
        x_end -= 1
        y_end -= 1

        solution.append((y_start,x_start,y_end,x_end))
        self.draw(y_start,x_start,y_end,x_end)

        x_left = self.amountLeft(y_start, x_end + 1, "x")

        if x_left <= 0:
          maybeX_start, maybeY_start = self.find(y_start)
          if maybeX_start == -1 and self.notFinised:
            x_start, y_start, x_left, y_left = self.nextRow()
          else:
            x_start = maybeX_start
            y_start = maybeY_start
            x_left = self.amountLeft(y_start, x_start, "x")
            y_left = self.amountLeft(y_start, x_start, "y")

        else:
          x_start = self.c - x_left

          y_left = self.amountLeft(0,x_start,"y")
          y_start = self.r - y_left

        posShape = self.shapePos
        posShape = self.scanShape(posShape,x_left, y_left)

      else:
        posShape = self.my_remove(posShape, posShape[0])
      print self.arr
      time.sleep(1)
    print solution


  def my_remove(self, my_list, word):
    new_list = []
    for element in my_list:
      if element != word:
        new_list.append(element)
    return new_list

  def find(self, row):
    for z in range(row + 1):
      for x in range(self.c):
        if self.arr[z, x] != 255:
          return x, z
    return -1, -1
  def nextRow(self):
    x_start = -1

    y_left = 0
    while y_left == 0:
      x_start += 1
      y_left = self.amountLeft(0,x_start,"y")
      y_start = self.r - y_left


    x_left = self.amountLeft(y_start,x_start,"x")

    return x_start, y_start, x_left, y_left

  def draw(self,ys,xs,ye,xe):
    self.arr[ys:ye + 1,xs:xe +1] = 255
    self.notFinised = 1 in self.arr or 0 in self.arr


  def amountLeft(self,row,column,dir):
    amount = 0

    if dir == "x":
      for x in range(column,self.c):
        if self.arr[row, x] != 255:
          amount += 1
        else:
          break

    if dir == "y":
      for y in range(row, self.r):
        if self.arr[y, column] != 255:
          amount += 1
        elif amount != 0:
          break
    return amount

  def scanShape(self, lst, xl, yl):
    new_list = []


    for ele in range(len(lst)):
      coord = lst[ele].split("*")
      a = int(coord[0])
      b = int(coord[1])

      if a <= yl and b <= xl:
        new_list.append(lst[ele])
    return new_list

  def checkMinIngre(self,x_start, y_start, shape):
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

cut = cutSlice(r,c,l,h,arr)






