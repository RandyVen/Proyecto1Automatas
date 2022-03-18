import re


class Node:
    def __init__(self, sim, val = None):
        self.leftNode = None
        self.rightNode = None
        self.leftList = []
        self.rightList = []
        self.s = sim
        self.v = val
        self.setLists()
        
    def insertVal(self, val):
        self.v = val

    def getLeftNode(self):
        return self.leftNode

    def getRightNode(self):
        return self.rightNode

    def getSimbol(self):
        return self.s
    
    def getVal(self):
        return self.v
    
    def firstPos(self):
        return self.leftList

    def lastPos(self):
        return self.rightList

    def insertParent(self, p):
        self.parent = p
    
    def insertLeft(self,n):
        self.leftNode = n

    def insertRight(self,n):
        self.rightNode = n
        
    def nullable(self, simbol):
        if simbol == "ε" or simbol == "*" or simbol == "?":
            return True
        else:
            return False
    
    def setLists(self):
        if self.getVal() != None:
            self.leftList.append(self.getVal())
            self.rightList.append(self.getVal())

class Automata:
    def __init__(self, estIn, estFin, states, alfabeth, transitions, name = ""): #Se le da el nombre de automata a las transiciones al cual se le puede asignar cualquier letra
        self.estadoInicial = estIn
        self.estadosFinales = estFin
        self.estados = states
        self.alfabeto = alfabeth
        self.transiciones = transitions
        self.nombre = name

    

