from Conexiones import *
from icecream import ic
import pydot
from PIL import Image
from io import BytesIO
import easygui as eg
import cv2

graph = pydot.Dot(graph_type='graph', strict=True)


#initialState = 'Arad'
goalState = 'Bucharest'

estadoI = eg.enterbox(msg='\nTodos los estados que se pueden elegir:\n\nArad\nCraiova\nDobreta\nEfoire\nFagaras\nGiurgiu\nHirsova\nIasi\nLugoj\nMehadia\nNeamt\nOradea\nPitesti\nRimnicu Vilcea\nSibiu\nTimisoara\nUrziceni\nVaslui\nZerind\n\nIngrese el estado inicial:',
                                title='Búsqueda A*',
                                default='arad', strip=True,
                                image=None).title()


if (estadoI == "Arad" or estadoI == "Craiova" or estadoI == "Dobreta" or estadoI == "Efoire" or estadoI == "Fagaras" or estadoI == "Giurgiu" or estadoI == "Hirsova" or estadoI == "Iasi" or estadoI == "Lugoj" or estadoI == "Mehadia" or estadoI == "Neamt" or estadoI == "Oradea" or estadoI == "Pitesti" or estadoI == "Rimnicu Vilcea" or estadoI == "Sibiu" or estadoI == "Timisoara" or estadoI == "Urziceni" or estadoI == "Vaslui" or estadoI == "Zerind"):

  initialState=estadoI

else:
  eg.msgbox(msg='EL ESTADO INGRESADO NO EXISTE, VUELVA A EJECUTAR EL PROGRAMA Y SELECCIONE UN ESTADO VALIDO',
          title='Búsqueda A*', 
          ok_button='Aceptar',
          image=None)  
  exit()

path = []
totalCost = []
heuristicCost = []
ca=[]
camino=[]

n = initialState

for edge in weightedEdges:
      if edge[0] == n:
        graph.add_edge(pydot.Edge(edge[0],edge[1],label=str(edge[2])))
        graph.add_node(pydot.Node(edge[1],color='black',style="filled", fillcolor="white"))
        ca.append(edge)


while n != goalState:
    neighbours = [edge for edge in weightedEdges if edge[0] == n] ##vecinos
    newNeighbours = [[edge[0],edge[1],edge[2] + totalCost[-1]] if n != initialState else edge for edge in neighbours] ##nuevos vecinos
    neighboursPlusHeuristic = [[edge[0],edge[1],edge[2],edge[2] + costToReachN[edge[1]]] for edge in newNeighbours]
    minNeighbour = [edge for edge in neighboursPlusHeuristic if edge[3] == min([ edge[3] for edge in neighboursPlusHeuristic ])][0]
    n = minNeighbour[1]
    
    for edge in weightedEdges:
      if edge[0] == n and n != goalState:
         graph.add_edge(pydot.Edge(edge[0],edge[1],label=str(edge[2]),group=1))
         graph.add_node(pydot.Node(edge[1],color='black',style="filled", fillcolor="white"))
         ca.append(edge)
              
    path.append(n)
    totalCost.append(minNeighbour[2])
    heuristicCost.append(minNeighbour[3])
    
    print(f"Next Node is {n} at min cost: {minNeighbour[3]}")


graph.add_node(pydot.Node(initialState,color='black',style="filled", fillcolor="skyblue"))       

for j in path:
  graph.add_node(pydot.Node(j,color='black',style="filled", fillcolor="skyblue"))

if goalState == n:
  graph.add_node(pydot.Node(n,color='black',style="filled", fillcolor="palegreen"))

p=1;
for n in ca:
  for m in ca:
    if m[0] == n[1] and n[0] == m[1] and p == 1:
     n[0]=" "+n[0]
     graph.add_edge(pydot.Edge(m[0],n[0],label=str(n[2])))
     graph.add_node(pydot.Node(n[0],color='black',style="filled", fillcolor="white"))
     p=p+1
    else:
     p=1

cont=1
aux=str(cont)+". "+initialState
camino.append(aux)

cont=2
for m in path:
  m=str(cont)+". "+m
  camino.append(m)
  cont=cont+1

i=0
while i<len(path):
  graph.add_edge(pydot.Edge(camino[i],camino[i+1]))
  graph.add_node(pydot.Node(camino[i],color='black',style="filled", fillcolor="skyblue",fontsize="13"))
  graph.add_node(pydot.Node(camino[i+1],color='black',style="filled", fillcolor="skyblue",fontsize="13"))
  i=i+1

print(f"{'-'*20}\nEl camino de la meta es: {initialState,path}  \nCon un costo total de: {sum(totalCost)} \nTeniendo un costo de la ruta de: {totalCost} \nCosto Heurístico de: {sum(heuristicCost)} \nCosto de ruta heurístico de: {heuristicCost}")

graph.set_bgcolor("gainsboro")
graph.write_png("arbol.png")
#Image.open(BytesIO(graph.create_png())).show()

#im = Image.open('out.png')
#im.show()

imagen = cv2.imread('arbol.png') 
cv2.imshow('Logo OpenCV',imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()


eg.msgbox(msg=f"\nEl estado inicial: {initialState}\nEl estado meta (definido por defecto): {goalState}\n\nEl camino de la meta es: {initialState,path}  \nCon un costo total de: {sum(totalCost)} \nTeniendo un costo de la ruta de: {totalCost} \nCosto Heurístico de: {sum(heuristicCost)} \nCosto de ruta heurístico de: {heuristicCost}",
          title='Búsqueda A*', 
          ok_button='Aceptar',
          image=None)





