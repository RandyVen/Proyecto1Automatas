from abc import get_cache_token
from re import sub
import Funciones 
import Nodos

estadoDelWhile = True
print("Menu:\n")
while estadoDelWhile:
    alfabetoNoe = []
    operadores = ["*","|","?","ʚ"]
    alfabeto = []
    metaCaracteres = ["*","(",")","|","?","ʚ"]
    print("1. Usar Thompson y Subconjuntos para formar el AFN y AFD \n2. Salir del programa")
    opcion = input("elija una opcion: ")
    print("procederemos a comprobar si la sintaxis de la expresion regular es correcta")
    if opcion == "2":

        estadoDelWhile = False
    else:

        expresion = input("ingrese la expresion regular que usara: ")
        print("Se ha leido la expresion satisfactoriamente")
        print("Se obtendran los caracteres unicos")
        alfabeto, expresion = Funciones.procesandoAlfabeto(expresion,alfabeto, metaCaracteres)
        print("sus MetaCaracteres(operadores) son: " + str(operadores))
        #print("vamos a añadir el operador de concatenacion")
        print("la expresion regular con su operador de concatenacion queda asi: " + expresion)
        #print("realizaremos un proceso extra para trabajar el operador +, en caso se encuentre dentro de la expresion")
        expresionPosfix = Funciones.infijoAPosfix(expresion,alfabeto)
        print ("Notacion posfija: " + str(expresionPosfix))
        print("su alfabeto es el siguiente: " + str(alfabeto))
      
        if(opcion == "1"):
        
        
            transiciones, estadoFinal, estadoInicial = Funciones.Thompson(expresionPosfix, alfabeto)
            
            estados = Funciones.getEstados(transiciones, estadoInicial)
            estados.append(estadoFinal)
            #print("los estados son: " + str(estados))
            #print("estado inicial es " + str(estadoInicial))
            #print("estado Final es " + str(estadoFinal))
            #print(str(transiciones))
            AFN = Nodos.Automata(estadoInicial, estadoFinal, estados, alfabeto, transiciones)
            Grafo = Funciones.crearGrafoDelAutomata(AFN.transiciones, "AFN", estadoFinal)
            
            subconjuntos = Funciones.clausuraE1(estados,AFN.transiciones)
            subconjuntos = Funciones.sortSubSets(subconjuntos)
            #print("estos son lo subconjuntos despues de ClausuraE1: " + str(subconjuntos))
            #Funciones.printSubSets(subconjuntos, estados)
            
            subSets, allSubSets, alfabetoNoe = Funciones.clausuraE2(subconjuntos, alfabeto,estadoInicial, transiciones)   
            #print("estos son los subconjuntos unicos, luego de ClausuraE2" + str(subSets))
            #print("estos son todos los subconjuntos para la tabla" + str(allSubSets))

            
            Funciones.printTableOfSubSets(subSets,allSubSets, alfabetoNoe)
            
            newStates = Funciones.newStates(subSets)
            newEstadoInicial = "0"
            newEstadosFinales = Funciones.newFinalStates1(subSets, newStates, estadoFinal)
            newTransitions = Funciones.createFDA(subSets, alfabetoNoe, allSubSets, newStates)
            print(str(newEstadoInicial))
            print(str(newStates))
            print(str(newEstadosFinales))
            AFD = Nodos.Automata(newEstadoInicial, newEstadosFinales, newStates, alfabetoNoe, newTransitions)
            
            Grafo2 = Funciones.crearGrafoDelAutomata(AFD.transiciones, "AFD", newEstadosFinales)
            #print("El grafo generado del AFD fue hecho en base a esta estructura: \n" + str(Grafo2))
        
            print("Ahora que ya tenemos el automata, podemos probar si funciona alguna cadena que ingresemos")
            cadena = input("ingrese su cadena a procesar: ")
            print(Funciones.Simulation(newEstadoInicial, newTransitions, cadena, newEstadosFinales))           
        else:
            print("Ingreso una opcion incorrecta, vuelva a intentarlo")

'''
    #ctrl + shift + v
    
    (ε|b|c|d)*abb(a|b|c|d)* 
    (a|b|c|d)*abb(a|b|c|d)*
    ba(a|b)*ab
    (a|b)*abb 
    (ab)*|(c*)b
    (a|b)*abb(a|b)*
    (a*|b*)*
    ((ε|a)b*)*
    '''