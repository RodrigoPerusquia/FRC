# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 17:24:40 2024

@author: rodri
"""

import math
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.stats as stats 

def append_value(dict_obj, key, value):                     # Función que sirve
    if key in dict_obj:                                     # para agregar una
        if not isinstance(dict_obj[key], list):             # entrada al
            dict_obj[key] = [dict_obj[key]]                 # diccionario de 
        dict_obj[key].append(value)                         # la población
    else:                                                   # (aristas
        dict_obj[key] = value                               # entre nodos i,j).


# Introducimos la función que mdoela el crecimiento de la población de gatos.
# Iteramos NS veces y, con ello, se recolectan los resultados de cada simulación. 

NS = 10
EV = np.zeros((NS, 52*10 + 1))

for T in range(NS):
# Diccionario que almacena la información característica de los nodos en la red.                                    
    graphM = {}                                         # Diccionario machos
    graphF = {}                                         # Diccionario hembras
    graphF[0] = {'G': 'M', 'A': 0, 'E': [], 'P': 21}    # Entrada auxiliar.
    graphM[0] = {'G': 'M', 'A': 0, 'E': [], 'P': 21}    # Entrada auxiliar.


    CI = 50                                     # Cantidad de nodos iniciales.
    FF = 0                                      # Cantidad de hembras
    MM = 0                                      # Cantidad de machos
    EP = 0                                      # Cantidad de hembras en celo
    DD = 0                                      # Cantidad de machos muy dominantes
    dd = 0                                      # Conteo de machos con dominancia positiva
    ep = 0                                      # Conteo de hembras en estro e interestro

    HS = 100                                     # Constante de saturación media

    si = 5                                      # Semana de inicio de iteración
    SI = si%52                                  # Ciclo anual de semanas
        
        
# Se procede a crear la condición inicial. Cada nodo contará con las características:
# Género (macho/hembra), edad (en meses), origen (condición inicial, intraespecífico,
# intersepecífico), aristas (encuentros sexuales).
# No hay gestaciones acumuladas.
     
    for l in range(1, CI + 1):
        a = random.randint(12, 36)                  # Edad entre 1 y 3 años (puede cambiar)
        g = random.choice(['M', 'F'])               # Género aleatorio
            
# Si es hembra, posee: Conteo de ciclo reproductivo (Diestro/Anestro (RC=0), Estro (RC=1),
# Interestro (RC=2)), Conteo de gestación(pseudo) + lactancia + destete (20(7) semanas),
# conteo de camadas producidas.  
        if g == 'F':
            if SI > 3 and SI < 44:                  # Etapa estacional de reproducción
                rc = random.randint(1, 2)
                ep = ep + 1
            else:                                   # Anestro: Nov-Dic-Ene
                rc = 0
            graphF[max(list(graphF)) + 1] = {'G': g, 'A': a, 'O': 'CI', 'E': [], 'RC': rc, 'P': 0, 'L': 0}
            FF = FF + 1
            if rc == 1:
                EP = EP + 1
                    
# Si es macho, posee: Valor de dominancia (crecimiento lineal de 8 meses a 2 años).
# Valor máximo de dominancia (1) constante a partir de los 2 años (nivel óptimo en gatos).
        else:
            d = min(1, (a - 8)/16)
            graphM[max(list(graphM)) + 1] = {'G': g, 'A': a, 'O': 'CI', 'E': [], 'D': d}
            dd = dd + 1
            MM = MM + 1
            if d > .74:                            # Dominancia alta (> 20 meses)
                DD = DD + 1
                    
    TP = [CI]
    Ff = [len(graphF) - 1]
    Mm = [len(graphM) - 1]

    P = np.array([])            # Almacenamiento de los nodos con gestación efectiva.
    nP = P                      # Almacenamiento de la suma de gestaciones efectivas por semana.

    PP = P                      # Almacenamiento de los nodos con pseudogestación.
    nPP = P                     # Almacenamiento de la suma de pseudogestaciones por semana.


# Se incluye un parámetro de adición de vértices de origen social.        
    ab = 1                      # Número de posibles "abandonos" supuestos por semana.


    for t in range(52*3*0 + 1, 52*3*10 + 1):        # Tiempo de iteración (10 años)
# Se hace un salto de tiempo de 1 semana por cada 3 tiempos de iteración.
    

        if t%3 == 1:
            for l in range(1, len(list(graphF))):        # Vaciado de aristas
                graphF[list(graphF)[l]]['E']=[]
            for l in range(1, len(list(graphM))):        # Vaciado de aristas
                graphM[list(graphM)[l]]['E']=[]
                
                
# Introducción de las crías a la red a la edad de 2.5 años: Suponiendo que la primera
# gestación ocurre en la primera semana, pasan 60 tiempos (20 semanas = getación (~9) +
# lactancia (~7) + destete (~4)) para que las primeras crías empiecen a ser
# parte de la dinámica.

            if t > 60:
                for l in range(int(nP[0])):
                    N = np.random.choice([3, 4, 5, 6], p = [.6, .25, .1, .05])
# Pesos elegidos para obtener una media de 3.2 crías por camada

                    if N==3:
                        N = N - np.random.choice([0, 1, 2, 3], p = [.2, .4, .3, .1])
                    elif(N==4):
                        N = N - np.random.choice([0, 1, 2, 3, 4], p = [.15, .3, .25, .2, .1])
                    elif(N==5):
                        N = N - np.random.choice([0, 1, 2, 3, 4], p = [.1, .2, .3, .25, .15])
                    else:
                        N = N - np.random.choice([1, 2, 3, 4, 5], p = [.15, .3, .25, .2, .1])
# Pesos de muerte elegidos para obtener una supervivencia del .55 de las crías
# en promedio al llegar a los 2.5 meses

                for n in range(N):
                    G = random.choice(['M', 'F'])       # Equiprobabilidad de género                   
                    if G == 'F':
                        graphF[max(list(graphF)) + 1] = {'G': G, 'A': 2.5, 'O': 'K', 'E': [], 'RC': 0, 'P': 0, 'L': 0}
                        FF = FF + 1
                    else:
                        graphM[max(list(graphM)) + 1] = {'G': G, 'A': 2.5, 'O': 'K', 'E': [], 'D': 0}
                        MM = MM + 1
 
                
# Simulación de las interacciones (sexuales) entre machos y hembras. Estos encuentros
# se denominan primarios.

            A = np.zeros((len(graphM) + ab, len(graphF) + ab))      # Matriz de adyacencia

# Cantidad de encuentros primarios tomada, acotada entre el mínimo y el máximo de
# la cantidad de machos con alta dominancia y la cantidad de hembras en estro.
            E = random.randint(min(DD, EP), max(DD, EP))
            
            #E = int(E/20)
        
            if DD > 3*EP:                                           # Ajuste de desproporcinalidad
                E = random.randint(EP, min(4*EP, DD))
           
            if EP > 2*DD:
                E = random.randint(DD, min(3*DD, EP))

            J = np.zeros(E)                                         # Vector para almacenar hembras con cruces


# Los encuentros sexuales ocurren cuando hay machos con dominancia positiva y
# hembras en etapa de celo latente. 
            if dd > 0 and ep > 0:
                for l in range(E):
                           
# Selección de un macho con peso en su dominancia. Restricción del macho en 
# la cantidad de encuentros con diferentes hembras que podría tener (3).
                    i = random.choices([list(graphM)[n] for n in range(1, len(list(graphM)))], weights = [graphM[list(graphM)[n]]['D'] for n in range(1, len(list(graphM)))], k=1)           
                    while len(graphM[i[0]]['E']) > 2:
                        i = random.choices([list(graphM)[n] for n in range(1, len(list(graphM)))], weights = [graphM[list(graphM)[n]]['D'] for n in range(1, len(list(graphM)))], k=1)                        
                                
# Selección de una hembra con peso en su periodo de celo (puede variar el peso
# propuesto). Restricción de la hembra en la cantidad de encuentros con diferentes
# machos que podría tener (4)
                    j = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = [abs(graphF[list(graphF)[n]]['RC'] - .2)*abs((1.8 - graphF[list(graphF)[n]]['RC'])) for n in range(1, len(list(graphF)))], k=1)
                    while len(graphF[j[0]]['E']) > 3:
                        j = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = [abs(graphF[list(graphF)[n]]['RC'] - .2)*abs((1.8 - graphF[list(graphF)[n]]['RC'])) for n in range(1, len(list(graphF)))], k=1)                        

                    J[l] = int(j[0])
                            
                    append_value(graphM[i[0]], 'E', int(j[0]))      # Información de cruce almacenada en
                    append_value(graphF[j[0]], 'E', int(i[0]))      # el diccionario para hembra y macho
                            
                    for m in range(1, len(list(graphM))):           # Información de cruce almacenada
                        if int(i[0]) == list(graphM)[m]:            # en la matriz de adyacencia
                            for f in range(1, len(list(graphF))):
                                if int(j[0]) == list(graphF)[f]:
                                    A[m][f] = 1
                                                
# Posterior a los primeros encuentros, se añaden los nodos de origen social
# (abandono, gatos perdidos, gatos domésticos con acceso al exterior)

            Ab = 0                                      # Contador de gatos añadidos.
            for l in range(ab):
                r = random.randint(0,1)                # Probabilidad de adición de vértices.
                if r == 1:
                    Ab = Ab + 1
                    am = 0                              # Contador de machos añadidos
                    af = 0                              # Contador de hembras añadidas

# Rango de edad contemplado por la baja supervivencia de gatos menor a 6 meses.
                    a = random.randint(6, 60)           
                    g = random.choice(['M', 'F'])       # Equiprobabilidad de género

# Llenado de datos para el vértice si es hembra (origen social = 'A').                  
                    if g == 'F':
                        af = af + 1
                        if a < 8:                       # Inicio de edad reproductiva (8 meses)
                            rc = 0
                        else:
                            if SI > 3 and SI < 44:      # Etapa estacional
                                rc = random.randint(1,2)
                                ep = ep + 1
                            else:
                                rc = 0
                        graphF[max(list(graphF)) + 1] = {'G': g, 'A': a, 'O': 'A', 'E': [], 'RC': rc, 'P': 0, 'L': 0}
                        FF = FF + 1
                        if rc == 1:
                            EP = EP + 1
                                
# Llenado de datos para el vértice si es macho (origen social = 'A').                   
                    else:
                        am = am + 1
                        if a < 8:                       # Inicio de edad reproductiva (8 meses)
                            d = 0
                        else:
                            d = min(1, (a - 8)/16)
                            dd = dd + 1
                        graphM[max(list(graphM)) + 1] = {'G': g, 'A': a, 'O': 'A', 'E': [], 'D': d}
                        MM = MM + 1
                        if d > .74:
                            DD = DD + 1

# Simulación de las interacciones (sexuales) entre machos y hembras. Estos encuentros
# se denominan secundarios. Reafirman que encuentros primarios hayan sido de 
# carácter sexual y fortalecen el argumento de que los gatos practican la poliginia.

        if t%3 == 2:

# Contador de hembras con primeros encuentros potenciales a entrar en gestación.
# Criterios: no en gestación y en estro.
            C = 0 
            for l in range(len(J)):
                if graphF[J[l]]['P'] == 0 and graphF[J[l]]['RC'] == 1:
                    C = C + 1

            if C > 0:
                    
# Cantidad de cruces secundarios propuesta (puede variar).
                EE = random.randint(max(int(C/3), 1), max(int(C/2), 1))     
                    
                for l in range(EE):   
                        
# Selección del macho. Ya no se establece peso en la dominancia para dar oportunidad
# a otros machos a tener cruces sexuales. Basta con que tenga dominancia positiva.       
                    i = random.choice([list(graphM)[n] for n in range(1, len(list(graphM)))])
                    while graphM[i]['A'] < 8:
                        i = random.choice([list(graphM)[n] for n in range(1, len(list(graphM)))])
                           
# Selección de la hembra entre las identificadas con primeros encuentros y que
# tengan posibilidad de entrar en gestación. 
                    j = random.choice([J[n] for n in range(len(J))])
                    while graphF[j]['P'] > 0 or graphF[j]['RC'] != 1:
                        j = random.choice([J[n] for n in range(len(J))])
                        
                    append_value(graphM[i], 'E', int(j))            # Información de cruce almacenada en
                    append_value(graphF[j], 'E', int(i))            # el diccionario para hembra y macho.
                            
                    for m in range(1, len(list(graphM))):           # Información de cruce almacenada
                        if int(i) == list(graphM)[m]:               # en la matriz de adyacencia
                            for f in range(1, len(list(graphF))):
                                if int(j) == list(graphF)[f]:
                                    A[m][f] = 1
                        
# Se junta la información de los dos diccionarios en uno solo para construir una 
# matriz de adyacencia cuadrada.
            graph = {}
            graph[0] = {'G': 'M', 'A': 0, 'E': [], 'P': 21}
            for l in range(1, len(graphM)):
                graph[max(list(graph)) + 1] = graphM[list(graphM)[l]]
            for l in range(1, len(graphF)):
                graph[max(list(graph)) + 1] = graphF[list(graphF)[l]]
                                
            AM = np.zeros((len(graph), len(graph)))
            for l in range(1, len(graphM)):
                for n in range (1, len(graphF)):
                    AM[l][len(graphM) -1 + n] = A[l][n]
                    AM[len(graphM) -1 + n][l] = A[l][n]


# Conteo del origen de los nodos en la dinámica.
            AA = 0
            IC = 0
            II = 0
            for l in range(1, len(list(graph))):
                if graph[list(graph)[l]]['O'] == 'CI':
                    IC = IC + 1
                elif(graph[list(graph)[l]]['O'] == 'A'):
                    AA = AA + 1
                else:
                    II = II + 1
                
# 3. Crecimiento de la población.

# Gráfica que muestra el crecimiento de la población total, la población de
# hembras y la población de machos.

            # tt = np.arange(0, t + 4, 3)/3        
            TP = np.append(TP, len(graph) - 1)
            # Ff = np.append(Ff, len(graphF) - 1)
            # Mm = np.append(Mm, len(graphM) - 1)
            # plt.plot(tt, TP, color='blue', linewidth=1)
            # plt.plot(tt, Ff, color='red', linewidth=1)
            # plt.plot(tt, Mm, color='green', linewidth=1)
            # plt.xlabel('Tiempo')
            # plt.ylabel('Población Total')
            # plt.show()


# En el tiempo 3 se realiza una actualización de datos de cada nodo.

        if t%3 == 0:
                
            i = 0                               # Contador de hembras en gestación
            I = 0                               # Contador de hembras en pseudogestación
                
# Se establecen criterios para determinar si una hembra entra en gestación o pseudogestación                
            for l in range(1, len(list(graphF))):
                if len(graphF[list(graphF)[l]]['E']) > 0:       # Que tenga al menos un encuentro
                    if graphF[list(graphF)[l]]['RC'] == 1:      # Que esté en estro
                        h = len(graphF[list(graphF)[l]]['E'])           

                
# Dependiendo de la cantidad de cruces obtenidos se asignan probabilidades de que
# ocurra ovulación y que la gestación sea efectiva, en virtud de que las hembras poseen
# ovulación inducida y que, entre más encuentros sexuales tengan, mayor la posibilidad
# de que entren en gestación.                             
                        if h == 1:
                            # Probabilidad de ovulación inducida
                            O = random.choices([0, 1], weights =(.28, .72), k = 1)
                            if O[0] == 1:
                                # Probabilidad de concepción
                                Pp = random.choices([0, 1], weights =(.63, .37), k = 1)
                            else:
                                Pp = [0]
                                    
                        if h > 1:
                            # Probabilidad de ovulación inducida
                            O = random.choices([0, 1], weights =(.15, .85), k = 1)
                            if O[0] == 1:
                                # Probabilidad de concepción
                                Pp = random.choices([0, 1], weights =(.07, .93), k = 1)
                            else:
                                Pp = [0]
                                
# En caso de haber gestación efectiva, se añade la hembra al vector de gestantes.
                        if Pp[0] == 1:
                            P = np.append(P,list(graphF)[l])
                            i = i + 1
                            graphF[list(graphF)[l]]['RC'] = 0       # Diestro
                                
# En caso de no haber gestación efectiva, se añade la hembra al vector de pseudogestantes.
                        if Pp[0] == 0:
                            PP = np.append(PP, list(graphF)[l])
                            I = I + 1
                            graphF[list(graphF)[l]]['RC'] = 0       # Diestro
                                    
                           
            nP = np.append(nP,i)        # Añadimos la cantidad de hembras en gestación.
            nPP = np.append(nPP,I)      # Añadimos la cantidad de hembras en pseudogestación.
                
            if i == 0:
                P = np.append(P,0)      # Se actualiza vector de gestantes si no hay en una semana
                                            
            if I == 0:                  # Se actualiza vector de pseudogestantes si no hay en una semana
                PP = np.append(PP,0)


            for n in range(len(P)):                     # Actualizamos semanas de gestación.
# Descartamos entrada auxiliar del diccionario en caso de que no haya gestaciones en alguna semana.
                if graphF[P[n]]['G'] == 'F':
# 20 semanas es la duración de inicio de gestación a aparición de camada en la red.
# 9 semanas es la duración de inicio de gestación a fin de gestación.
                    graphF[P[n]]['P'] = (graphF[P[n]]['P'] + 1)%21
                    if graphF[P[n]]['P'] == 10:         # Actualizamos contador de camada
                        graphF[P[n]]['L'] = graphF[P[n]]['L'] + 1
# Aunque las camadas aparezcan a las 10 semanas, no se incluyen dentro de la red hasta
# que cumplan 2.5 meses. Suponemos que si la madre fallece, la camada también por su
# casi nula supervivencia.                            
                            

            for n in range(len(PP)):                     # Actualizamos semanas de pseudogestación.
# Descartamos entrada auxiliar del diccionario en caso de que no haya pseudogestaciones en alguna semana.
                if graphF[PP[n]]['G'] == 'F':
# 6 semanas es la duración de inicio de pseudogestación a fin de pseudogestación
                    graphF[PP[n]]['P'] = (graphF[PP[n]]['P'] + 1)%7
                            
# Eliminamos las entradas de P y nP semana a semana cuando no hay gestaciones.
# Tomamos a partir de len(P) = 2 por si en la primera semana no hubo gestaciones.
            if len(P) > 1:
                if graphF[P[0]]['P'] == 21:
                    P = np.delete(P, 0)
                    nP = np.delete(nP, 0)

# Eliminamos las entradas de PP y nPP semana a semana cuando no hay pseudogestaciones.
# Tomamos a partir de len(PP) = 2 por si en la primera semana no hubo pseudogestaciones.
            if len(PP) > 1:                              
                if graphF[PP[0]]['P'] == 21:
                    PP = np.delete(PP, 0)
                    nPP = np.delete(nPP, 0)     
                
# Eliminamos las entradas de P y nP semana a semana cuando concluye el proceso de
# gestación + lactancia + destete.
            if graphF[P[0]]['P'] == 0:
                while graphF[P[0]]['P'] == 0:
                    P = np.delete(P, 0)
                nP = np.delete(nP,0)
                
# Eliminamos las entradas de PP y nPP semana a semana cuando concluye el proceso de
# pseudogestación.               
            if graphF[PP[0]]['P'] == 0:
                while graphF[PP[0]]['P'] == 0:
                    PP = np.delete(PP, 0)
                nPP = np.delete(nPP,0)

# Establecemos una tasa de recuperación para los vértices de origen social
# con una probabilidad establecida de acuerdo a los casos favorables y desfavorables.
# Casos favorables (3): Un gato con acceso al exterior entró a la dinámica y regresó
# a su hogar; Un gato fue abandonado, entró en la dinámica y no sobrevivió/lo recuperaron.
# Caso desfavorable (1): Un gato fue abandonado, entró en la dinámica y sobrevivió.

# Se elige el género de manera equiprobable y se actualizan los diccionarios
# así como los contadores de gatos machos y hembras abandonados.
            for l in range(Ab):
                r = random.choices([0, 1], weights = (.25, .75), k = 1)
                if r[0] == 1:
                    AM = am
                    AF = af
                    if am > 0:
                        if af > 0:
                            g = random.choice(['M', 'F'])
                            if g == 'M':
                                R = random.randint(max(list(graphM)) - am + 1, max(list(graphM)))
                                am = am - 1
                                MM = MM - 1
                                del graphM[R]
                            else:
                                R = random.randint(max(list(graphF)) - af + 1, max(list(graphF)))
                                af = af - 1
                                FF = FF - 1
                                del graphF[R]
                        if AF == 0:
                            R = random.randint(max(list(graphM)) - am + 1, max(list(graphM)))
                            am = am - 1
                            MM = MM - 1
                            del graphM[R]
                                    
                    if AM == 0:
                        R = random.randint(max(list(graphF)) - af + 1, max(list(graphF)))
                        af = af - 1
                        FF = FF - 1
                        del graphF[R]


# Actualización de datos característicos en los machos.
            v = np.array([])          
            DD = 0
            dd = 0
            KK = 0
            JJ = 0
                
# En los machos se actualiza la edad y la dominancia.
            for l in range(1, len(list(graphM))):
                graphM[list(graphM)[l]]['A'] = graphM[list(graphM)[l]]['A'] + .25
                        
                if graphM[list(graphM)[l]]['A'] > 8:
                    dd = dd + 1
                    graphM[list(graphM)[l]]['D'] = min(1, (graphM[list(graphM)[l]]['A'] - 8)/16)
                    if graphM[list(graphM)[l]]['D'] > .74:
                        DD = DD + 1
  
# Actualización de rol social en gatos de origen intraespecífico.
                    if graphM[list(graphM)[l]]['O'] == 'K':     
                        graphM[list(graphM)[l]]['O'] = 'J'
                  
# Conteo de gatos menores a 6 meses
                if graphM[list(graphM)[l]]['A'] < 6.1:
                    KK = KK + 1
                if graphM[list(graphM)[l]]['A'] > 6:
                    JJ = JJ + 1
                                
# Remoción de machos con edad > 6 años.
                if graphM[list(graphM)[l]]['A'] > 71.9:           
                    MM = MM - 1
                    DD = DD - 1
                    dd = dd - 1
                    JJ = JJ - 1
                    v = np.append(v, list(graphM)[l])
                        
            for l in range(len(v)):
                del graphM[int(v[l])]


            EP = 0
            ep = 0
            V = np.array([])
                
# Actualización de edad para hembras.
            for l in range(1, len(list(graphF))):
                    
                graphF[list(graphF)[l]]['A'] = graphF[list(graphF)[l]]['A'] + .25
                  
# Actualización de ciclo reproductivo dependiendo de la semana del año.
                if SI > 4 and SI < 44:
                    if graphF[list(graphF)[l]]['A'] == 8:
                        graphF[list(graphF)[l]]['RC'] = 1
                        EP = EP + 1
                        ep = ep + 1
                        
                    if graphF[list(graphF)[l]]['A'] > 8:
                        if list(graphF)[l] not in P:
                            if list(graphF)[l] not in PP:
                                ep = ep + 1
                                graphF[list(graphF)[l]]['RC'] = (graphF[list(graphF)[l]]['RC'] + 1)%3
                                if graphF[list(graphF)[l]]['RC'] == 1:
                                    EP = EP + 1
                                if graphF[list(graphF)[l]]['RC'] == 0:
                                    graphF[list(graphF)[l]]['RC'] = 1
                                    EP = EP + 1

                elif (SI > 43 or SI < 4):
                    graphF[list(graphF)[l]]['RC'] = 0
                             
                elif (SI == 4):
                    if graphF[list(graphF)[l]]['A'] > 7.9:
                        if list(graphF)[l] not in P:
                            rc = random.randint(1, 2)
                            ep = ep + 1
                            graphF[list(graphF)[l]]['RC'] = rc
                            if rc == 1:
                                EP = EP + 1
       
# Actualización de rol social en gatas de origen intraespecífico.
                if graphF[list(graphF)[l]]['A'] > 7.9:
                    if graphF[list(graphF)[l]]['O'] == 'K':
                        graphF[list(graphF)[l]]['O'] = 'J'
       
# Conteo de gatas menores a 6 meses.      
                if graphF[list(graphF)[l]]['A'] < 6.1:
                    KK = KK + 1        
                if graphF[list(graphF)[l]]['A'] > 6:
                    JJ = JJ + 1
                    
# Remoción de hembras con edad > 6 años
                if graphF[list(graphF)[l]]['A'] > 71.9:
                    FF = FF - 1
                    JJ = JJ - 1
                    if graphF[list(graphF)[l]]['RC'] > 0:
                        if graphF[list(graphF)[l]]['RC'] == 1:
                            EP = EP - 1
                        ep = ep - 1
# Vector de almacenamiento por si la gata removida está embarazada. Se
# actualizan los datos pertinentes antes de remover del diccionario.
                    V = np.append(V, list(graphF)[l])


# Remoción por muerte natural sujeta a capacidad de carga de la población y
# a supervivencias de cada individuo por edad.

            D = max(1, int((MM + FF)/(HS/2)))                   # Tasa de muerte propuesta (se puede ajustar)
                
# Se propone una cota de supervivencia de todos los individuos de la red con los 
# datos hallados en la literatura.
            s = .9991 - ((.9991-.99804)*JJ  + (.9991-.99233)*KK)/HS

            for l in range(D):
                r = random.choices([0, 1], weights = (math.pow(s, 7*(MM+FF)), 1 - math.pow(s, 7*(MM+FF))), k = 1)
                #r = random.choices([0, 1], weights = (min(.75, 1 - (MM + FF)/100), max(.25, (MM + FF)/100 )), k = 1)                          
                    
# En caso de ocurrir muerte, el género se elige equiprobablemente y se propone 
# una tasa de supervivencia por edad mediante una distribución gama(5, 1/2).
                if r[0] == 1:
                    mm = MM
                    ff = FF
                    if MM > 0:
                        if FF > 0:
                            g = random.choice(['M', 'F'])
                            if g == 'M':
                                m = random.choices([list(graphM)[n] for n in range(1, len(list(graphM)))], weights = (1 - stats.gamma.pdf(graphM[list(graphM)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphM)))), k = 1)    
                                MM = MM - 1
                                if graphM[m[0]]['D'] > 0:
                                    dd = dd - 1
                                if graphM[m[0]]['D'] > .74:
                                    DD = DD - 1
                                del graphM[m[0]]
                            else:
                                m = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = (1 - stats.gamma.pdf(graphF[list(graphF)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphF)))), k = 1)    
                                while m[0] in V:
                                    m = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = (1 - stats.gamma.pdf(graphF[list(graphF)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphF)))), k = 1)    
                                FF = FF - 1
                                if graphF[m[0]]['RC'] == 1:
                                    EP = EP - 1
                                if graphF[m[0]]['RC'] > 0:
                                    ep = ep - 1
                                V = np.append(V, m[0])


                        if ff == 0:
                            m = random.choices([list(graphM)[n] for n in range(1, len(list(graphM)))], weights = (1 - stats.gamma.pdf(graphM[list(graphM)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphM)))), k = 1)    
                            MM = MM - 1
                            if graphM[m[0]]['D'] > 0:
                                dd = dd - 1
                            if graphM[m[0]]['D'] > .74:
                                DD = DD - 1
                            del graphM[m[0]]
                                               
                    if mm == 0:
                        m = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = (1 - stats.gamma.pdf(graphF[list(graphF)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphF)))), k = 1)    
                        while m[0] in V:
                                m = random.choices([list(graphF)[n] for n in range(1, len(list(graphF)))], weights = (1 - stats.gamma.pdf(graphF[list(graphF)[n]]['A']/12, a = 5, scale = 1/2) for n in range(1, len(list(graphF)))), k = 1)    
                        FF = FF - 1
                        if graphF[m[0]]['RC'] == 1:
                            EP = EP - 1
                        if graphF[m[0]]['RC'] > 0:
                            ep = ep - 1
                        V = np.append(V, m[0])

# Las hembras que fueron seleccionadas y que se almacenaron en el vector V
# son removidas de la red. Se actualizan los datos necesarios en caso de que
# alguna hembra se encuentre en gestación o en pseudogestación.
            for l in range(len(V)):
                if int(V[l]) in P:
                    i = 0
                    j = 0
                
# Inicia el proceso de ubicación de la hembra en el vector de gestantes a partir
# de su semana de gestación.
                    while graphF[P[i]]['P'] > graphF[int(V[l])]['P']:
                        i = i + 1
                        j = j + 1
                    k = 0
                    h = 0
                
# Continua el proceso de ubicación de la hembra pero ahora en el vector de 
# número de gestantes por semana. Se actualiza contemplando la remoción del nodo.
                    while k < j:
                        if nP[h] == 0:
                            k = k + 1
                            h = h + 1
                        else:    
                            k = k + nP[h]
                            h = h + 1          
                    nP[h] = nP[h] - 1
                            
# Si el número de gestantes por semana sigue siendo positivo, sólo borramos a
# la hembra del vector de gestantes.
                    if nP[h] > 0:
                        p = 0
                        while (int(V[l]) == P[p]) == False:
                            p = p + 1
                        P = np.delete(P,p)
                    
# Si el número de gestantes por semana es cero, reemplazamos a la hembra
# del vector de gestantes por una entrada 0 con el fin de emparejar el vector
# de gestantes con el vector del número de gestantes por semana.
                    if nP[h] == 0:
                        p = 0
                        while (int(V[l]) == P[p]) == False:
                            p = p + 1
                        P[p] = 0
                          
# Se realiza el mismo procedimiento en el caso de que la hembra por remover 
# pertenezca al vector de pesudogestantes.
                if int(V[l]) in PP:
                    i = 0
                    j = 0
                    while graphF[PP[i]]['P'] > graphF[int(V[l])]['P']:
                        i = i + 1
                        j = j + 1
                    k = 0
                    h = 0
                    while k < j:
                        if nPP[h] == 0:
                            k = k + 1
                            h = h + 1
                        else:    
                            k = k + nPP[h]
                            h = h + 1          
                    nPP[h] = nPP[h] - 1
                            
                    if nPP[h] > 0:
                        p = 0
                        while (int(V[l]) == PP[p]) == False:
                            p = p + 1
                        PP = np.delete(PP,p)
                    if nPP[h] == 0:
                        p = 0
                        while (int(V[l]) == PP[p]) == False:
                            p = p + 1
                        PP[p] = 0
                               
# Una vez actualizados los vectores correspondientes a las gestantes y las
# pseudogestantes, procedemos a borrar el nodo del diccionario.
                del graphF[int(V[l])]
                           
# En el caso de que la especie se extinga, se detiene el programa.  
            if len(graphM) == 1 and len(graphF)==1:
                print('Extinción en semana', si)
                break

# Para finalizar, se actualiza el contador de semanas y el contador de semana
# simulada.

            SI = (SI + 1)%52
            si = si + 1

    EV[T] = TP
    
for l in range(NS):
    tt = np.arange(0, t + 3, 3)/3
    plt.plot(tt, EV[l], color='blue', linewidth=1)
    plt.show()

ev = []
for l in range(NS):
    ev.append(EV[l])

Ev = np.mean(ev, axis=0)
tt = np.arange(0, t + 3, 3)/3
plt.plot(tt, Ev, color='red', linewidth=1)
plt.show()

# 52 104 156 208 260 312 364 416 468 520
