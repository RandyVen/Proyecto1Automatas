import re
from os import remove
import Nodos
import subprocess

def validadExpresion(expresion):
    try:
        re.compile(expresion)
        esValido = True
    except re.error:
        esValido = False
    return esValido

def procesandoAlfabeto(expresion,alfabeto, metaCaracteres):
    alfabeto = list(set(expresion))
    #print("su alfabeto con todos los simbolos unicos de la expresion son los siguiente: " + str(alfabeto))
    #con la siguiente linea eliminamso todos los metaCaracteres y dejamos solo los simbolos de la expresion regular
    alfabeto = [e for e in alfabeto if e not in metaCaracteres]
    if ("ε" not in alfabeto):
        alfabeto.insert(0,"ε")

    #vamos a añadir el operador de concatenacion
    tamaño = len(expresion) * 2
    for y in range(0, tamaño):
        try:
            if((expresion[y] in alfabeto or expresion[y] == "+" or expresion[y] == "*" or expresion[y] == "?" or expresion[y] == ")") and (expresion[y+1] in alfabeto or expresion[y+1] == "(")):
                parte1 = expresion[:y+1]
                parte2 = expresion[y+1:]
                expresion = parte1 + "ʚ" +parte2
                
                #print(demo)
        except:
            pass

    return alfabeto, expresion

def Transformplus(expresion, alfabeto):
    '''Este while existe para que se revise la cantidad de veces que sea necesaria la expresion y se resetee el tamaño
    del primer for'''
    while expresion.find("+") != -1:
        '''son las variables que serviran para tener las posiciones de corte de la expresion'''
        corte1 = 0
        corte2 = 0
        '''aqui empezamos a analizar del final al principio toda la expresion o desde al posicion que tenga que
        analisar segun la posicion por la variable control'''
        for pos in range (len(expresion)-1,0,-1):
            
            if str(expresion[pos]) == "+":
                #print('entre')
                corte1 = pos + 1
                stack = []
                #print(expresion[pos -1])
                for x in range(pos-1,-1,-1):
                    #print('entre x2')
                    if expresion[x] == "*" or expresion[x] == "+" or expresion[x] == "?" or expresion[x] == ")" or expresion[x] in alfabeto:
                        #print('entre x2')
                        stack.append(expresion[x])
                        #print(str(stack))
                    elif expresion[x] == "(":
                        stack.remove(")") 
                        #print(str(stack))
                    elif expresion[x] == "|" or expresion[x] == "ʚ":
                        if ")" not in stack:
                            corte2 = x
                            transform = expresion[corte2 +1: corte1 - 1]
                            expresion = expresion[:corte2 + 1] + transform + "ʚ" + transform + "*" + expresion[corte1:]
                            #print(str(expresion))
                            stack = []
                            break
                        else:
                            stack.insert(0,expresion[x])
                if len(stack) != 0:
                    transform = expresion[:corte1 -1]
                    expresion = transform + "ʚ" + transform + "*" + expresion[corte1:]
    return expresion
"""Esta es una funcion que sirve para poder mostrar una lista con todo su contenido concatenado"""
def printlist(expresion):
    regular = ""
    for item in expresion:
        regular += item
    print(regular)

def printVerticallyList(lista):
    for element in lista:
        print(str(element))

"""Código para expresiones regulare de Infija a Postfija"""
def infijoAPosfix(expresion,alfabeto):
    expresionPosfix = []
    pila = ['n']
    
    for i in expresion:
        if (i in alfabeto):
            expresionPosfix.append(i) 
        else:
            if (pila == [] or pila[-1] == "(" or i == "("):
                pila.append(i) 
            elif (i == "+" or i == "*" or i == "?"):
                if (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?"):
                    expresionPosfix.append(i)
                    #pila.append(i)
                else:
                    pila.append(i)
            elif i == "ʚ":
            #print "len(pila)"
            #print len(pila)
                while (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?") :
                    expresionPosfix.append(pila.pop())
                    #print len(pila)
                if (pila[-1] == "ʚ"):
                    expresionPosfix.append(i)
                else:
                    pila.append(i)
            elif(i == "|"):
                #print "len(pila)"
                #print len(pila)
                while (pila[-1] == "+" or pila[-1] == "*" or pila[-1] == "?" or pila[-1] == "ʚ"):
                    expresionPosfix.append(pila.pop())
                    #print len(pila)
                if (pila[-1] == "|"):
                    expresionPosfix.append(i)
                else:
                    pila.append(i)
            elif(i == ")"):
                while pila[-1] != "(":
                    expresionPosfix.append(pila.pop())
                pila.pop()
        #print(str(pila) + "   " + str(expresionPosfix))
    while len(pila) > 1:
        expresionPosfix.append(pila.pop())
    return expresionPosfix

def valsOfSimbols(expresionPosfix, alfabeto):
    cont = 1
    listOfVals = []
    for simbolo in expresionPosfix:
            if simbolo in alfabeto and simbolo != "ε":
                listOfVals.append(cont)
                cont += 1
    return listOfVals

def crearArbol(expresionPosfix, alfabeto, operadores, listOfVals):#https://www.delftstack.com/howto/python/trees-in-python/ 
    pila = []
    listConCat = []
    for i in expresionPosfix:
        #print(i)
        if (i in alfabeto):
            if i != "ε":
                leaf = Nodos.Node(i, listOfVals.pop(0))
            else:
                leaf = Nodos.Node(i)
            #print(i)
            pila.append(leaf)
        elif (i in operadores and i != "*" and i != "?"):
            leaf = Nodos.Node(i)
            L1 = pila.pop()
            L2 = pila.pop()
            leaf.insertLeft(L1)
            leaf.insertRight(L2)
            leaf.setfirstAndlast()
            if i == "ʚ":
                listConCat.append(leaf)
            # print("sim: " + L1.s  + " left: " + str(L1.firstPos()) + " right: " + str(L1.lastPos()))
            # print("sim: " + leaf.s  + " left: " + str(leaf.firstPos()) + " right: " + str(leaf.lastPos()))
            # print("sim: " + L2.s  + " left: " + str(L2.firstPos()) + " right: " + str(L2.lastPos()) + "\n")
            
            pila.append(leaf)
        elif( i == "*" or i == "?"):
            leaf = Nodos.Node(i)
            L1 = pila.pop()
            #print(L1.v)
            leaf.insertRight(L1)
            leaf.setfirstAndlast()
            pila.append(leaf)
    
    return pila.pop(), listConCat

def printTree(node, level=0):
    if node != None:
        #node.setfirstAndlast()
        printTree(node.getLeftNode(), level + 1)
        if node.v != None:
            print(' ' * 4 * level + '->', "sim: " + node.s + " val: " + str(node.v) + " left: " + str(node.firstPos()) + " right: " + str(node.lastPos()))
        else:
            print(' ' * 4 * level + '->', "sim: " + node.s + " left: " + str(node.firstPos()) + " right: " + str(node.lastPos()))
        printTree(node.getRightNode(), level + 1)

# def getFollowPosSet(posnode, ConCatList):
#     FollowPosList = []
#     return FollowPosList

def getFollowposList(ConCatList):
    FollowPosList = []
    posnode = 0
    while posnode < len(ConCatList):

        cantidadDeElementosFirst = 0
        cantidadDeElementosFirst = len(ConCatList[posnode].rightNode.lastPos())
                
        listToFollow = ConCatList[posnode].rightNode.lastPos()
        #print(str(node.rightNode.lastPos()) + " this is right(lastPos) y la cantidad de elementos es: " + str(cantidadDeElementosFirst))

        if ConCatList[posnode].rightNode.s == "*" or ConCatList[posnode].rightNode.s == "?" or ConCatList[posnode].rightNode.s == "|":
            listToFollow = listToFollow + ConCatList[posnode].leftNode.lastPos()
            #print(str(listToFollow))
        elif ConCatList[posnode].rightNode.s == "ʚ" and (ConCatList[posnode].leftNode.s == "*" or ConCatList[posnode].leftNode.s == "?" or ConCatList[posnode].leftNode.s == "|"):
            #print("cado concatenar y kleen")
            #print(str(ConCatList[posnode+1].leftNode.firstPos()))
            listToFollow =  ConCatList[posnode].leftNode.lastPos() + ConCatList[posnode+1].leftNode.firstPos()
            #print(str(listToFollow) + " this")
            cantidadDeElementosFirst = len(listToFollow)
            posnode += 1
            #print(str(cantidadDeElementosFirst) + "cantidad concat y kleen")
        else:
            listToFollow = ConCatList[posnode].leftNode.firstPos()
            #print(str(listToFollow))
            cantidadDeElementosFirst = len(listToFollow)
                    
        #print(ConCatList[posnode].getSimbol() + " with left: " + ConCatList[posnode].leftNode.getSimbol() + " and right: " + ConCatList[posnode].rightNode.getSimbol())

        #print(cantidadDeElementosFirst)
        #print("\n")
        for x in range(0, cantidadDeElementosFirst):
            #print(x)
            #print(str(listToFollow))
            
            FollowPosList.append(listToFollow)

            #print(listToFollow)

        #FollowPosList += getFollowPosSet(posnode, ConCatList)
        #print(FollowPosList)
        posnode +=1
    FollowPosList.append([])

    return FollowPosList

def followPos(item, listOfVals, FollowPosList):
    index = listOfVals.index(item)
    followposSet = FollowPosList[index]

    return followposSet

def getSimbols(estado, listOfVals, listOfsimbols):
    simbols = []
    for item in estado:
        #print(str(item))
        x = listOfVals.index(item)
        
        if listOfsimbols[x] not in simbols and listOfsimbols[x] != "#":
            #print(x)
            simbols.append(listOfsimbols[x])
    return simbols

def createDirectAFD(ConCatList, listOfVals, listOfsimbols, FollowPosList):
    Transiciones = {}
    Transiciones[str(ConCatList[-1].firstPos())] = {}
    #print(str(Transiciones))
    unMarkStack = []
    unMarkStack.append(ConCatList[-1].firstPos())

    while unMarkStack != []:
        #print(str(unMarkStack) + "unmark")
        estado = unMarkStack.pop(0)
            
        if len(estado) == 1:
            #print(str(estado) + "  dd")
            if estado != []:
                Transiciones[str(estado)] = {}
            index = listOfVals.index(estado[0])
            trans = listOfsimbols[index]
            #print(trans)
            xEstado = FollowPosList[index]
            #print(xEstado)
            unMarkStack.append(xEstado)
            Transiciones[str(estado)][trans] = str(xEstado)
            #print(str(Transiciones))

        else:
            if estado != []:
                Transiciones[str(estado)] = {}
            #print(str(listOfVals) + "error aqui")
            #print(str(estado))
            simbolos = getSimbols(estado, listOfVals, listOfsimbols)
            for sim in simbolos:
                #print(sim)
                estadoU = []
                for item in estado:

                    indexU = listOfVals.index(item)
                    if listOfsimbols[indexU] == sim:
                        #print("index: " + str(indexU))
                        #print("followlist: " + str(FollowPosList[indexU]))
                        #print(sim)
                            
                        estadoU += followPos(item,listOfVals, FollowPosList)
                        #print(str(estadoU))
                        #print(str(estadoU) not in Transiciones[str(estado)].values() and sim not in Transiciones[str(estado)] == None)
                        #print(str(Transiciones[str(estado)].values()))
                        #print(str(Transiciones[str(estado)].has_key(sim)))
                        #print(str(estadoU) not in Transiciones[str(estado)].values())
                        #print(sim not in Transiciones[str(estado)].keys())
                        #print(Transiciones[str(estado)].get(sim))
                        #if str(estadoU) not in Transiciones[str(estado)].values() and sim not in Transiciones[str(estado)] != None:
                if  Transiciones[str(estado)].get(sim) == None:
                    #print("True")
                    Transiciones[str(estado)][sim] = str(estadoU)
                    #print(str(estadoU))
                    #print(str(Transiciones.keys()))
                    if str(estadoU) not in Transiciones:
                        #print("si entre")
                        unMarkStack.append(estadoU)
                else:
                    #print("False")
                    pass
    
                    #print(str(estadoU))
    
    return Transiciones
                        


def printDirectTable(listSimbols, listPosition, listFollowPos):
    # print(len(listSimbols))
    # print(len(listPosition))
    # print(len(listFollowPos))

    for x in range(0,len(listFollowPos)):
        print(str(listSimbols[x] + "   " + str(listPosition[x]) + "   " + str(listFollowPos[x])))

def Thompson(expresionPosfix, alfabeto, cont = 0):
    stackTransiciones = []
    stackIniciales = []
    stackFinales = []
    automata = {}
    stackNewNodos = []
    #expresionPosfix = [e for e in expresionPosfix if e != "("]
    #expresionPosfix = [e for e in expresionPosfix if e != ")"]
    
    #print(str(expresionPosfix))
    for caracter in expresionPosfix:
        #print(caracter)
        if caracter in alfabeto:
            stackTransiciones.append(caracter)
            #print(len(stackTransiciones))
        else:
            #print(str(stackIniciales))
            #print(str(stackFinales))
            if caracter == "|":# El or siempre tiene 2 tipos de tranciciones
                if len(stackTransiciones) >= 2:
                    transicion1 = stackTransiciones.pop()
                    transicion2 = stackTransiciones.pop()

                    for x in range(cont, cont + 6):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1
                    automata[stackNewNodos[0]] = {"ε1": stackNewNodos[1], "ε2" : stackNewNodos[2]}# hoay dos epsilons porque porque hay dos nodos a los que hay que ir 
                    automata[stackNewNodos[1]] = {transicion1 : stackNewNodos[3]}
                    automata[stackNewNodos[2]] = {transicion2 : stackNewNodos[4]}
                    automata[stackNewNodos[3]] = {"ε1":stackNewNodos[5]}
                    automata[stackNewNodos[4]] = {"ε1":stackNewNodos[5]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 1 :
                    transicion1 = stackTransiciones.pop()
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1
                    
                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2" : stackNewNodos[1]}
                    automata[stackNewNodos[1]] = {transicion1 : stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1" : stackNewNodos[3]}
                    automata[final] = {"ε1":stackNewNodos[3]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                #elif len(stackTransiciones) == 0 and len(stackIniciales) > 1 and len(stackNewNodos) > 1:
                elif len(stackTransiciones) == 0:#Asume que existen 2 nodos iniciales y finales
                    inicial1 = stackIniciales.pop()
                    inicial2 = stackIniciales.pop()
                    final1 = stackFinales.pop()
                    final2 = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial2, "ε2" : inicial1}
                    automata[final1] = {"ε1":stackNewNodos[1]}
                    automata[final2] = {"ε1":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

            if caracter == "ʚ":
                if len(stackTransiciones) >= 2:
                    transicion1 = stackTransiciones.pop()
                    transicion2 = stackTransiciones.pop()

                    for x in range(cont, cont + 3):#Crea nuevos nodos 
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {transicion2: stackNewNodos[1]}#agarrar el nodo inicial y ponerle una transicion
                    automata[stackNewNodos[1]] = {transicion1: stackNewNodos[2]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 1:
                    transicion1 = stackTransiciones.pop()
                    final = stackFinales.pop()

                    stackNewNodos.append("q" + str(cont))
                    cont += 1

                    automata[final] = {transicion1: stackNewNodos[0]}
                    
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0:#Unirlos por medio de un epsilon 
                    #print(str(stackFinales))
                    #print(str(stackIniciales))
                    #print(str(stackTransiciones))
                    final = stackFinales.pop(-2)
                    inicial = stackIniciales.pop()

                    automata[final] = {"ε1": inicial}

            if caracter == "*":
                if len(stackTransiciones) >= 1:
                    transicion1 = stackTransiciones.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1":stackNewNodos[1], "ε2":stackNewNodos[3]}
                    automata[stackNewNodos[1]] = {transicion1 :stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1":stackNewNodos[3], "ε2":stackNewNodos[1]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0 and len(stackIniciales):
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2": stackNewNodos[1]}
                    automata[final] = {"ε1": inicial, "ε2":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

            if caracter == "?":
                if len(stackTransiciones) >= 1:
                    transicion1 = stackTransiciones.pop()

                    for x in range(cont, cont + 4):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1":stackNewNodos[1], "ε2":stackNewNodos[3]}
                    automata[stackNewNodos[1]] = {transicion1 :stackNewNodos[2]}
                    automata[stackNewNodos[2]] = {"ε1":stackNewNodos[3]}
                    
                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []

                elif len(stackTransiciones) == 0 :
                    inicial = stackIniciales.pop()
                    final = stackFinales.pop()

                    for x in range(cont, cont + 2):
                        stackNewNodos.append("q" + str(cont))
                        cont += 1

                    automata[stackNewNodos[0]] = {"ε1": inicial, "ε2":stackNewNodos[1]}
                    automata[final] = {"ε1":stackNewNodos[1]}

                    stackIniciales.append(stackNewNodos[0])
                    stackFinales.append(stackNewNodos[-1])
                    stackNewNodos = []
    #or str(expresionPosfix) == "['.', '(']"
    if str(expresionPosfix) == "['.', ')', '(', '(']" or str(expresionPosfix) == "['.', ')']":
        if str(expresionPosfix) == "['.', ')', '(', '(']":
            transicion1 = expresionPosfix.pop()
            expresionPosfix.pop()
            expresionPosfix.pop()
            transicion2 = expresionPosfix.pop()
        else:
            transicion1 = expresionPosfix.pop()
            transicion2 = expresionPosfix.pop()

        #print(transicion1)
        #print(transicion2)
        for x in range(cont, cont + 3):
            stackNewNodos.append("q" + str(cont))
            cont += 1

        automata[stackNewNodos[0]] = {transicion2: stackNewNodos[1]}
        automata[stackNewNodos[1]] = {transicion1: stackNewNodos[2]}

        
        stackIniciales.append(stackNewNodos[0])
        stackFinales.append(stackNewNodos[-1])
        

    #print(str(stackTransiciones))
    #print(str(stackFinales))
    #print(str(stackIniciales))
    #print(str(automata))
    return automata, stackFinales.pop(), stackIniciales.pop()


def crearGrafoDelAutomata(Transiciones, name,estadosFinales):
    Grafo = "digraph G{\n"
    #print(str(estadosFinales))
    for key in Transiciones:
        #print(key)
        #print(Transiciones[key])
        for innerKey in Transiciones[key]:
            graph = str(key) + " -> " + str(Transiciones[key][innerKey]) + " [label=" + '"' + str(innerKey) + '"'  + "]\n"
            
            if key in estadosFinales and str(name) == "AFD" and str(key) + " [ style=bold ]" not in Grafo:
                graph += str(key) + " [ style=bold ]\n"
            
            #print(innerKey)
            #print(Transiciones[key][innerKey])
            Grafo = str(Grafo) + str(graph)
    #print(str(name))
    if str(name) == "AFN":
        #print("aaaaaaaaaa")
        Grafo += str(estadosFinales) + " [ style=bold ]\n"
    Grafo = str(Grafo) + "}"
    #print(Grafo)
    createFile(name,Grafo, ".dot")
    return Grafo

def crearGrafoDFA(Transiciones, name,estadosFinales, traductor):
    Grafo = "digraph G{\n"
    #print(str(estadosFinales))
    for key in Transiciones:
        #print(key)
        #print(Transiciones[key])
        for innerKey in Transiciones[key]:
            graph = str(traductor[key]) + " -> " + str(traductor[Transiciones[key][innerKey]]) + " [label=" + '"' + str(innerKey) + '"'  + "]\n"
            
            if key in estadosFinales and str(name) == "AFD" and str(key) + " [ style=bold ]" not in Grafo:
                graph += str(traductor[key]) + " [ style=bold ]\n"
            
            #print(innerKey)
            #print(Transiciones[key][innerKey])
            Grafo = str(Grafo) + str(graph)
    #print(str(name))
    if str(name) == "AFN":
        #print("aaaaaaaaaa")
        Grafo += str(estadosFinales) + " [ style=bold ]\n"
    Grafo = str(Grafo) + "}"
    #print(Grafo)
    createFile(name,Grafo, ".dot")
    return Grafo

def createFile(name, text, extension):
    existe = False
    try:
        with open(str(name) + extension, 'r') as f:
            existe = True
    except FileNotFoundError as e:
        existe = False
    
    if existe == True:
        remove(str(name) + extension)
        f = open(str(name) + extension,'a', encoding='utf-8')
        f.write(str(text))
        f.close()
    else:
        f = open(str(name) + extension,'a', encoding='utf-8')
        f.write(str(text))
        f.close()

def getEstados(transiciones, estadoInicial):
    result = []
    for key in transiciones.keys():
        if key not in result:
            result.append(key)
    if result[0] != estadoInicial:
        ind = result.index(estadoInicial)
        #estadoNotinit = result[0]
        result[ind] = result[0]
        result[0] = estadoInicial
        #for i in range(1,ind):
            
    return result

def getkeys(dict):
    list = []
    #print("dict es: " + str(dict))
    for key in dict.keys():
        list.append(key)
    return list

def getvalues(dict):
    list = []
    for val in dict.values():
        list.append(val)
    return list

def SubconjuntosE(transiciones, estadoTrans):
    listEst = []
    listTrans = []
    conjunto = []
    find = False
    while(find == False):
        '''Ahora averiguaremos si el estado a revisar se encuentra dentro del automata '''
        if estadoTrans in transiciones:
            '''Si el estado esta dentro del automata, vamos a conseguir sus transiciones y sus estados a los que apunta dichas transiciones '''
            Estytrans = transiciones[estadoTrans]
            #print("====== fijate bien aqui con === " + str(Estytrans))
            '''Procedemos a guardar las transiciones y los estados en listas distintas '''
            lista = getkeys(Estytrans) 
            #print(lista)
            for i in range(0,len(lista)):
                listTrans.append(lista.pop(0))
            lista = getvalues(Estytrans)
            #print(lista)
            for i in range(0,len(lista)):
                listEst.append(lista.pop(0))
                    
        #print("la lista de transiciones es " + str(listTrans))
        #print("la lista de estados es " + str(listEst))
        '''Iniciaremos a revisar las transiciones no epsilon que posee el estado que estamos revisando;
        Para ello tambien necesitamos obtener el tamaño de las transiciones que hay '''
        size = len(listEst)-1
        for x in range(size,-1,-1):
            #print(str(x))
            #print("Estamos verificando la transicion " + str(listTrans[x]) + " y el estado " + str(listEst[x]))
            '''Aqui revisamos si la transicion que hay no es epsilon y la sacamos de la lista de transiciones '''
            if(str(listTrans[x][:1]) != "ε"):
                #print(str(listTrans[x]) + " es algo que no es epsilon")
                #print("conjuntos esta asi " + str(conjunto))
                listTrans.pop()
                listEst.pop()
                #print("la lista de transiciones es " + str(listTrans))
                #print("la lista de estados es " + str(listEst))
                #print(str(x))
                #print("antes de entrar listEst esta asi: " + str(listEst) + " y x es " + str(x))
                '''En caso de que si sea un epsilon, revisamos si el estado al que apunta ya se encuentra dentro de conjunto
                Hacemos esto, porque si el estado ya esta dentro de conjunto, entonces quiere decir que ya se reviso dicho estado,
                por ende, no vale la pena volver a revisarlo'''
            elif(listEst[x] in conjunto):
                #print(str(listEst[x]) + " ya se encuentra dentro de conjutnos")
                #print("conjuntos esta asi " + str(conjunto))
                listEst.pop()
                listTrans.pop()
                #print("la lista de transiciones es " + str(listTrans))
                #print("la lista de estados es " + str(listEst))
                pass
            
        if(len(listEst) != 0 and len(listTrans) != 0):
            testTrans = listTrans[-1]
            #print("transicion a testear es " + str(testTrans) + " hacia el estado " + str(listEst[-1]))
            if(testTrans[:1] == "ε"):
                #print("halle epsilon")
                #print("la lista de transiciones esta asi actualmente " + str(listTrans))
                #cont += 1
                estadoTrans = listEst.pop()
                conjunto.append(estadoTrans)
                listTrans.pop()
                #print("conjuntos esta asi " + str(conjunto))
                #print("la lista de transiciones es " + str(listTrans))
                #print("la lista de estados es " + str(listEst))
                #print("siguiente estado a revisar es "+ str(estadoTrans))
        else:
            find = True
            return conjunto
            #print("la lista de estados esta " + str(theStates))
            #print("los subconjuntos respectivo a su estado esta " + str(subconjuntos))

def clausuraE1(estados,transiciones):
    #theStates = []
    subconjuntos = []
    #print(str(estados))
    #print(str(transiciones))
    '''iniciamos tomando los estados, dentro de la lista de estados del automata y los revisamos todos '''
    for item in estados:
        '''decimos que estado trans sera igual al estado a revisar, se crea una varialbe para el conjunto de ese estado
        Tambien creamos una variable que detendra el while cuando termine de hacer su revision'''
        estadoTrans = item
        subconjuntos.append(SubconjuntosE(transiciones, estadoTrans))    
    return subconjuntos

def printSubSets(subconjuntos, estados):

    for y in range(0, len(subconjuntos)):
        print(str(estados[y]) + " U " + str(subconjuntos[y]))

def sortSubSets(subconjuntos):
    for set in range(0, len(subconjuntos)):
        subconjuntos[set].sort()
    return subconjuntos

def joinSets(conjunto1, conjunto2):

    for item in conjunto2:
        if item not in conjunto1:
            conjunto1.append(item)
    return conjunto1

def sortList(list):
    list.sort()
    return list

def invertList(list):
    newList = []
    for x in range(len(list)-1,-1,-1):
        newList.append(list[x])
    return newList

def removeEpsilon(alfabeto):
    for x in range(0,len(alfabeto)):
        pass

def clausuraE2(subconjuntos, alfabeto,estadoInicial, automata):
    alfabetoNoe = [e for e in alfabeto if e != "ε"]  
    subSets = []
    allSubSets = []
    cont = 0
    if subconjuntos[0] == []:
        list = [estadoInicial]
        subSets.append(list)
    else:
        subSets.append(subconjuntos[0])
    
    ''' Empezamos recorriendo todos los conjuntos en Subsets'''
    #while cont < sizeSubsets:
    for subSet in subSets:
        sizeSubsets = len(subSets)
    
        #cont += 1
        #subSet = subSets[cont]
        #print(str(subSets))
        #print("intento: " + str(cont) + " y el tamaño de subSets es: " + str(sizeSubsets))
        '''Haremos este proceso, la cantidad de letras dentro del alfabeto sin epsilon '''
        allSubSets.append(subSet)
        for letra in alfabetoNoe:
            conjunto = []
            listTransiciones = []
            listEstados = []
            '''revisaremos estado por estado '''
            for estado in subSet:
                
                find = False
                #print(estado)
                while(find == False):
                    
                    if estado in automata:
                        '''Si el estado esta dentro del automata, vamos a conseguir sus transiciones y sus estados a los que apunta dichas transiciones '''
                        Estados_y_transiciones = automata[estado]
                        #print(str(Estados_y_transiciones))
                        '''Procedemos a guardar las transiciones y los estados en listas distintas '''
                        lista = getkeys(Estados_y_transiciones) 
                        
                        for i in range(0,len(lista)):
                            listTransiciones.append(lista.pop(0))
                        lista = getvalues(Estados_y_transiciones)
                        
                        for i in range(0,len(lista)):
                            listEstados.append(lista.pop(0))

                    '''Iniciaremos a revisar las transiciones no epsilon que posee el estado que estamos revisando;
                    Para ello tambien necesitamos obtener el tamaño de las transiciones que hay '''
                    size = len(listEstados)-1
                    for x in range(size,-1,-1):
                        
                        '''Aqui revisamos si la transicion que hay no es epsilon y la sacamos de la lista de transiciones '''
                        if(str(listTransiciones[x]) != letra ):
                            
                            listTransiciones.pop()
                            listEstados.pop()
                            
                            '''En caso de que si sea un epsilon, revisamos si el estado al que apunta ya se encuentra dentro de conjunto
                            Hacemos esto, porque si el estado ya esta dentro de conjunto, entonces quiere decir que ya se reviso dicho estado,
                            por ende, no vale la pena volver a revisarlo'''
                        elif(listEstados[x] not in conjunto):
                            
                            conjunto.append(listEstados[x])
                    #print("lo que hay dentro de listEstados es: " + str(listEstados))
                    if(len(listEstados) != 0 and len(listTransiciones) != 0):
                        #print(str(len(listEstados)))
                        #theState = listEstados.pop()
                        conjuntoEpsilon = SubconjuntosE(automata, listEstados.pop())
                        conjunto = joinSets(conjunto, conjuntoEpsilon)
                        conjunto = sortList(conjunto)
                        listTransiciones.pop()
                        find = True
                    else:
                        find = True
                        #allSubSets.append([])
                
            allSubSets.append(conjunto)
            #print(str(allSubSets))
            if conjunto not in subSets and conjunto != []:
                subSets.append(conjunto)
                sizeSubsets += 1
        cont += 1
        
        
            
    return subSets, allSubSets, alfabetoNoe

def printTableOfSubSets(subSets,allSubSets, alfabetoNoe):
    TheStates = newStates(subSets)
    separacion = 0
    for cont in range(0,len(subSets)):
        if separacion == 0:
            separacion = len(subSets[0])
        elif len(subSets[cont]) > len(subSets[cont - 1]):
            separacion = len(subSets[cont])
    separacion *= 5
    columnas = "    Q " + (" " * separacion)
    for letra in alfabetoNoe:
        columnas = columnas + (" " * round(separacion/2)) + str(letra) + (" " * separacion)
    print(columnas)

    fila = ""
    cont = 0
    for state in TheStates:
        #print(str(state))
        if cont <= len(allSubSets)-1:
            fila = str(state) + "   "
        for unConjunto in range(0,len(alfabetoNoe)+1):
            #print(cont)
            #print(len(allSubSets))
            if cont % (len(alfabetoNoe)+1) == 0 and cont <= len(allSubSets)-1:
                fila += str(allSubSets[cont]) + (" " * separacion)
            elif cont <= len(allSubSets)-1:
                reference = columnas.index(alfabetoNoe[(cont % (len(alfabetoNoe)+1))-1])
                separacionL = len(fila) - reference

                if separacionL < 0:
                    fila = fila + (" " * (separacionL*-1))
                    fila += str(allSubSets[cont]) + (" " * separacion)
                else:
                    fila = fila[0: len(fila) - separacionL]
                    fila += str(allSubSets[cont]) + (" " * separacion)
            
            cont += 1
        fila += "\n"
        print(fila)
        fila = ""
'''En base al cont y la cantidad de Estados dentro de la lista de subconjuntos unicos creamos un array
con un valor correspondiente al subconjunto generado'''
def newStates(subSets, cont = 0):
    TheStates = []
    #print(str(cont))
    for con in range(cont,cont + len(subSets)):
        TheStates.append(str(con))
    #print(str(cont + len(subSets)))
    #print("Estos son los Estados nuevos para el AFD" + str(TheStates))
    #print(len(TheStates))
    return TheStates
'''Para esta funcion lo mejor sera el tener que recibir la lista de subconjuntos unicos y los nuevos estados creados.
Esto porque al usar un array de estados finales, podemos hacer dicho recorrido, pero si detectamos que en
cierta posicion tal conjunto si posee un estado final de la lista de estados finales, entonces añadimos su valor
correspondiente dentro de la lista de newStates. Esto porque en la misma posicion del newState, esta el subconjunto
que corresponde al subconjunto al cual posee algun estado Final. '''
def newFinalStates2(subSets, newStates, listEstadosFinales):
    #lista de lista correspondiente a cada token con su estado final.
    listFinalStates = []
    
    #tomamos un estado final de la lista de estados Finales
    for estadoFinal in listEstadosFinales:  
        listFinalStates.append(newFinalStates1(subSets,newStates,estadoFinal))
    return listFinalStates

def newFinalStates1(subSets, newStates, estadoFinal):
    theNewFinalStates = []
    #print(estadoFinal.type())

    cont = 0
    #tomamos conjunto por conjunto
    for conjunto in subSets:
        #se verifica si en dicho conjunto se encuentra cierto estado final
        if estadoFinal in conjunto:
            theNewFinalStates.append(newStates[cont])
        cont += 1
    return theNewFinalStates

def createFDA(subSets, alfabetoNoe, allSubSets, newStates):
    NStates = newStates
    newTransitions = {}
    cont1 = 0 + 1
    cont2 = 0
    #print(len(NStates))
    for uniConjunto in subSets:
        #print(str(cont2))
        newTransitions[NStates[cont2]] = {}
        for item in alfabetoNoe:
            if allSubSets[cont1] != []:
                newTransitions[NStates[cont2]][item] = subSets.index(allSubSets[cont1])
                
            cont1 += 1
        cont1 += 1    
        cont2 += 1
    return newTransitions


def Simulation(newEstadoInicial, newTransitions, cadena, newEstadosFinales):
    estado = newEstadoInicial
    #print(newTransitions)
    for item in cadena:
        print("El elemento que vamos a procesar de la cadena es " +str(item))
        #print(str(newTransitions.keys()))
        #print(Funciones.getkeys( newTransitions))
        #print(estado)
        if(item != ")" and item != "("):
            if str(estado) in getkeys(newTransitions):
                print(str(estado) + " posee estas transiciones " + str(newTransitions[str(estado)]))
                try:
                    #print("por lo que asignamos el estado " + str(newTransitions[str(estado)][item]))
                    estado = newTransitions[str(estado)][item]
                except:
                    #estado = "none"
                    pass
                #print(str(estado))
    #print(newEstadosFinales)
    if str(estado) in newEstadosFinales:
        return "La cadena ha sido aceptada\n"
    else:
        return "la cadena no fue aceptada\n"