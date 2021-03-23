import math
import numpy as np
import random
from queue import PriorityQueue
#from stack import stack
import networkx as nx
from constants import DIRECTIONS
from domain import Node


class Service:
    def __init__(self, drone_map, drone, initial_x, initial_y, final_x, final_y,mode):
        self.drone_map = drone_map
        self.drone = drone
        print(mode)
        self.initial_x = initial_x
        self.initial_y = initial_y
        self.final_x = final_x
        self.final_y = final_y
        self.path = self.greedy()
        # if mode == 0:
        #     self.path = self.greedy()
        # elif mode == 1:
        #     self.path = self.greedy()
        self.iterator = iter(self.path)
        self.incomplete_path = [next(self.iterator)]
        self.finished_simulation = False
        
    def runSearch(self, mode):
        if mode == 0:
            self.path = self.greedy()
        elif mode == 1:
            self.path = self.aStar()
        
    def aStar(self):
        x = self.initial_x
        y = self.initial_y
        found = False
        visited = []
        inQ = [(x,y)]
        while inQ and not found:
            if len(inQ) < 1:
                return []
            pos = inQ.pop()
            visited.append(pos)
            if pos[0] == self.final_x and pos[1] == self.final_y:
                found = True
            else:
                aux = []
                for dir in DIRECTIONS:
                    sumX = dir[0] + pos[0]
                    sumY = dir[1] + pos[1]
                    if 0 <= sumX < 20 and 0 <= sumY < 20 and self.drone_map.surface[sumX][sumY] != 1 and (sumX,sumY) not in visited:
                        aux.append((sumX,sumY))
                #print(aux)
                aux = sorted(aux,key=lambda x: self.euclid((self.final_x,self.final_y),x) + len(visited) -1,reverse = True)
                #print(aux)
                inQ = inQ + aux
        if not found:
            return []
        else:
            return visited

        
    #euclidian distance
    @staticmethod
    def euclid(p1,p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        
    def greedy(self):
        x = self.initial_x
        y = self.initial_y
        found = False#checks if we got a path yes
        visited = []#visited squared
        inQ = [(x,y)]#squares to visit
        while inQ and not found:
            if len(inQ) < 1:
                return []
            pos = inQ.pop()#get the next pos to visit
            visited.append(pos)#add the current pos as visited
            if pos[0] == self.final_x and pos[1] == self.final_y:
                found = True#means we got where we had to
            else:
                aux = []
                for dir in DIRECTIONS:
                    sumX = dir[0] + pos[0]
                    sumY = dir[1] + pos[1]
                    if 0 <= sumX < 20 and 0 <= sumY < 20 and self.drone_map.surface[sumX][sumY] != 1 and (sumX,sumY) not in visited:
                        aux.append((sumX,sumY))
                #print(aux)
                aux = sorted(aux,key=lambda x: self.euclid((self.final_x,self.final_y),x),reverse = True)
                inQ = inQ + aux
        if not found:
            return []
        else: 
            return visited

    # def best_first_search(self, f):
    #     inf = self.drone_map.n + self.drone_map.m
    #     distances = [[inf for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
    #     value = [[0 for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
    #     prev = [[(i, j) for j in range(self.drone_map.m)] for i in range(self.drone_map.n)]
    #     visited = [[False for _ in range(self.drone_map.m)] for _ in range(self.drone_map.n)]
    #     distances[self.initial_x][self.initial_y] = 0
    #     visited[self.initial_x][self.initial_y] = True
    #     pq = PriorityQueue()
    #     pq.put((0, (self.initial_x, self.initial_y)))
    #     while not pq.empty():
    #         item = pq.get()
    #         print(item)
    #         if value[item[1][0]][item[1][1]] != item[0]:
    #             continue
    #         if item == (self.final_x, self.final_y):
    #             break
    #         for direction in DIRECTIONS:
    #             #print(distances)
    #             neighbour = (item[1][0] + direction[0], item[1][1] + direction[1])
    #             #print(neighbour)
    #             if self.drone_map.drone_fits(neighbour[0],neighbour[1]) and not visited[neighbour[0]][neighbour[1]]:
    #                 prev[neighbour[0]][neighbour[1]] = item[1]
    #                 visited[neighbour[0]][neighbour[1]] = True
    #                 distances[neighbour[0]][neighbour[1]] = distances[item[1][0]][item[1][1]] + 1
    #                 value[neighbour[0]][neighbour[1]] = f(neighbour, distances, self.final_x, self.final_y)
    #                 pq.put((f(neighbour, distances, self.final_x, self.final_y), neighbour))
    #     if prev[self.final_x][self.final_y] == (self.final_x, self.final_y):
    #         return []
    #     path = []
    #     now = self.final_x, self.final_y
    #     while now != (self.initial_x, self.initial_y):
    #         path.append(now)
    #         now = prev[now[0]][now[1]]
    #         print(now)
    #     path.append(now)
    #     return list(reversed(path))

    # def search_a_star(self):
    #     return self.best_first_search(lambda neighbour, distances, fx, fy: distances[neighbour[0]][neighbour[1]] +
    #                                   self.__dist((fx, fy), neighbour))

    # def search_greedy(self):
    #     return self.best_first_search(
    #         lambda neighbour, distances, fx, fy: self.__dist((fx, fy), neighbour))

    @staticmethod
    def __dist(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    
    def drone_next_move(self):
        try:
            self.incomplete_path.append(new_pos := next(self.iterator))
            self.drone.move(*new_pos)
        except StopIteration:
            self.finished_simulation = True
            
    #def move(self, drone):