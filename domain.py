import numpy as np
from random import random
import pickle

from constants import *

class DroneMap:
    def __init__(self, n=ROWS, m=COLUMNS):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n,self.m))

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
    
    def set_random_map(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random() <= fill:
                    self.surface[i][j]=1
    
    def drone_fits(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m and self.surface[x][y] == 0
    
    def save_map(self, file_name="test.map"):
        with open(file_name,'wb') as f:
            pickle.dump(self,f)
            f.close()
    
    def load_map(self,file_name):
        with open(file_name, 'rb') as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()
            
class Drone:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def move(self, x, y):
        self.x = x
        self.y = y
        
        
class Node:
    
    def __init__(self,pos:(),parent:()):
        self.pos = pos
        self.parent = parent
        self.g = 0  #distance to start
        self.h = 0  #distance to goal
        self.f = 0  #total cost
        
    # Compare nodes
    def __eq__(self, other):
        return self.pos == other.pos
    # Sort nodes
    def __lt__(self, other):
        return self.f < other.f
    # Print node
    def __repr__(self):
        return ('({0},{1})'.format(self.pos, self.f))