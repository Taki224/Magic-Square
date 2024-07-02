

# Adapted from: https://www.kodeclik.com/magic-square/

import random 
import numpy as np
import copy 

class MagicSquare():
    def __init__(self, dimension):
        
        self.dimension = dimension 
        self.number = random.randint(1,100) # random starting number 
        self. magic_square_solution = np.zeros([dimension, dimension], dtype = int)
        self.fill_checker = np.zeros([dimension, dimension])
        self.rounded = round (self.number) 
        if (self.rounded == self.number):
          self.number = round(self.number)
          np.int_(self.magic_square_solution)
        # place the first number in the top row, middle column
        self.right = int((self.dimension-1)/2)
        self.up = 0
        self.magic_square_solution[self.up][self.right] = self.number
        self.fill_checker[self.up][self.right] = 1 
        # fill the numbers 
        self.__solution()
        
        self.magic_square_puzzle= copy.deepcopy (self.magic_square_solution) 
        self.__puzzle()
        
        self.check_sum = sum (self.magic_square_solution[0]) 
        
       
                
    # the below function will take the current position
    # i.e., num in position (x,y) and 
    # will determine where to place num+1
    def find_next_pos (self, x,y,num):
    
          if (x + 1 > self.dimension - 1 and y - 1 < 0):
                #check if the position is going off 
                #both the row and column ranges
                #in which case we simply place the 
                #next number in the cell below
    
                self.magic_square_solution[y+1][x] = num + 1
                self.fill_checker[y+1][x] = 1
                self.up = y + 1
                self.right = x
                self.number += 1
    
          elif (x + 1 > self.dimension - 1):
                #check if you are going off the column range
    
                self.magic_square_solution[y-1][x - (self.dimension - 1)] = num + 1
                self.fill_checker[y-1][x - (self.dimension - 1)] = 1
                self.up = y - 1
                self.right = x - (self.dimension - 1)
                self.number += 1
    
          elif (y - 1 < 0):
                #check if you are going off the row range
    
                self.magic_square_solution[y+self.dimension-1][x+1] = num + 1
                self.fill_checker[y+self.dimension-1][x+1] = 1
                self.up = y + self.dimension-1
                self.right = x + 1
                self.number += 1
    
          else:
            #we are now within the square and not going out
    
                if (self.fill_checker[y-1][x+1] == 0):  
                  #check if you can go normal diagonal into an empty cell
    
                  self.magic_square_solution[y-1][x+1] = num + 1
                  self.fill_checker[y-1][x+1] = 1
                  self.up = y-1
                  self.right = x + 1
                  self.number += 1
    
                else:
                  #this situation means that the diagonal 
                  #position is occupied
    
                  self.magic_square_solution[y+1][x] = num + 1
                  self.fill_checker[y+1][x] = 1
                  self.up = y + 1
                  self.right = x
                  self.number += 1  
                  
                  
    def solution (self): 
        return self.magic_square_solution
    
    def magic_constant (self): 
        return self.check_sum
    
    def puzzle (self): 
        return self.magic_square_puzzle
              
    def save (self, filename): 
        
        
        with open (filename, "w") as f:
            f.write (str(self.solution())) 
            
        with open (filename, "a") as f:
            f.write (str(self)) 
            

            
    def __puzzle (self):
        for x in range (self.dimension) : 
            for y in range (self.dimension): 
                if random.random()>0.5: 
                    self.magic_square_puzzle[x][y] = "0"
        

    def __solution (self):
        # we now are ready to call the above 
        # function to populate the full magic square
        for i in range(1,self.dimension*self.dimension):
              self.find_next_pos(self.right, self.up, self.number)

    def __str__(self):
        # Now we are ready to pretty print the full array
        s = "\n"+"-"*(self.dimension*(len(str(self.number))+1)+1) + "\n"
        
        spacing = '{:'+ str(len(str(self.number))) + '}'
        
        for i in range(len(self.magic_square_puzzle)) : 
              s+=("|")
              for j in range(len(self.magic_square_puzzle[i])) :
                  s+= spacing.format(self.magic_square_puzzle[i][j])
                  s+="|"
              s+="\n"
        
        s+= "-"*(self.dimension*(len(str(self.number))+1)+1) + "\n"
        
        return s 
        
        




