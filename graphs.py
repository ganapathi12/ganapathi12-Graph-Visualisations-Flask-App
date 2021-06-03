import networkx as nx
import matplotlib.pyplot as plt
import json  
 
class Graph:
    def __init__(self,numvertex):
        self.adjMatrix = [[0]*numvertex for x in range(numvertex)]
        self.numvertex = numvertex
        self.vertices = {}
        self.verticeslist =[0]*numvertex

    def set_vertex(self,vtx):
        id=vtx
        if 0<=vtx<=self.numvertex:
            self.vertices[id] = vtx
            self.verticeslist[vtx] = id

    def set_edge(self,frm,to,cost=0):
        frm = self.vertices[frm]
        to = self.vertices[to]
        self.adjMatrix[frm][to] = cost
        #for directed graph do not add this
        #self.adjMatrix[to][frm] = cost

    def get_vertex(self):
        return self.verticeslist

    def get_edges(self):
        edges=[]
        for i in range (self.numvertex):
            for j in range (self.numvertex):
                if (self.adjMatrix[i][j]!=0):
                    edges.append((self.verticeslist[i],self.verticeslist[j],self.adjMatrix[i][j]))
        return edges
        
    def get_matrix(self):
        return self.adjMatrix

#utility fucntion used by DFS which does recursive depth first search 
def DFSUtil(G, v, visited, sl): #goes to the node and iteratively checks if it is visited or not
    visited[v] = True
    sl.append(v) 
    for i in G[v]:
        if visited[i] == False:
            DFSUtil(G, i, visited, sl)
    return sl
 


#DFS traversal 
def DFS(G, source): 
    visited = [False]*(len(G.nodes()))
    sl = []		#a list that stores dfs forest starting with source node
    dfs_stk = [] #A nested list that stores all the DFS Forest's
    dfs_stk.append(DFSUtil(G, source, visited, sl))
    for i in range(len(G.nodes())):
        if visited[i] == False:
            sl = []
            dfs_stk.append(DFSUtil(G, i, visited, sl))
    return dfs_stk


adjacencylist1=[]
#takes input from the file and creates a weighted graph
def CreateGraph():
    G = nx.DiGraph()
    f = open('input.txt')
    n = int(f.readline())
    wtMatrix = []
    for i in range(n):
        list1 = list(map(int, (f.readline()).split()))
        wtMatrix.append(list1)
    source = int(f.readline()) #source vertex from where DFS has to start
    #Adds egdes along with their weights to the graph 
    global adjacencylist1
    adjacencylist1=[]
    for i in range(n):
        lis=[]
        for j in range(n):
            if wtMatrix[i][j] > 0:
                lis.append(j)
                G.add_edge(i, j, length = wtMatrix[i][j])
        adjacencylist1.append(lis)
    return G,source

def adjacencylist2display():
    global adjacencylist1
    return adjacencylist1
    

imagesbfs=[]

#BFS traversal 
def BFS(G, source, pos):
#     plt.clf()
    imagesbfs.clear()
    visited = [False]*(len(G.nodes()))
    queue = [] #a queue for BFS traversal
    queue.append(source)
    visited[source] = True
    while queue:
        curr_node = queue.pop(0)
        for i in G[curr_node]:  #iterates through all the possible vertices adjacent to the curr_node
            if visited[i] == False:
                queue.append(i)
                visited[i] = True
                nx.draw_networkx_edges(G, pos, edgelist = [(curr_node,i)], width = 2.5, alpha = 0.6, edge_color = 'r')
                plt.savefig("bfs.png")
                imagesbfs.append(imageio.imread("bfs.png"))
                
    imageio.mimsave("originalbfs.gif",imagesbfs)
    gif=imageio.mimread("originalbfs.gif")
    imageio.mimsave("slowbfs.gif",gif,fps=1)
    return
def DrawGraphbfs(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)  #with_labels=true is to show the node number in the output graph
    edge_labels = dict([((u,v,), d['length']) for u, v, d in G.edges(data = True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, label_pos = 0.3, font_size = 11) #prints weight on all the edges
    return pos

def bfsprintgraph():
    plt.clf()
    G, source = CreateGraph()
    pos = DrawGraphbfs(G)
    BFS(G, source, pos)
    plt.savefig("userbfs.png")

adj=[]
def userbfsdraw(nodeb,edgesb,srcb):
    plt.clf()
    node=int(nodeb)
    source=int(srcb)
    Gbfs=Graph(node)
    
    for n in range(0,node):
        Gbfs.set_vertex(n)
    #edgeslist=str(input("enter [[1, 2, 3], [2, 3, 4]] format"))
    
    finallist=json.loads(edgesb)
    for x in finallist:
        Gbfs.set_edge(*x)
        
    usergraph=CreateGraph2(node,finallist)
    plt.clf()
    pos = DrawGraphbfs(usergraph)
    BFS(usergraph, source, pos)
    plt.savefig("userbfs.png")
    
    global adj
    adj=Gbfs.get_matrix()



import imageio
images=[]
#marks all edges traversed through DFS with red
def DrawDFSPath(G, dfs_stk):
    plt.clf()
    images.clear()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)  #with_labels=true is to show the node number in the output graph
    edge_labels = dict([((u,v,), d['length']) for u, v, d in G.edges(data = True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, label_pos = 0.3, font_size = 11) #prints weight on all the edges
    for i in dfs_stk:    
        #if there is more than one node in the dfs-forest, then print the corresponding edges
        if len(i) > 1:
            for j in i[ :(len(i)-1)]:
                if i[i.index(j)+1] in G[j]:
                    nx.draw_networkx_edges(G, pos, edgelist = [(j,i[i.index(j)+1])], width = 2.5, alpha = 0.6, edge_color = 'r')
                    plt.savefig("orig.png")
                    images.append(imageio.imread("orig.png"))
                else:
                    #if in case the path was reversed because all the possible neighbours were visited, we need to find the adj node to it.
                    for k in i[1::-1]: 
                        if k in G[j]:
                            nx.draw_networkx_edges(G, pos, edgelist = [(j,k)], width = 2.5, alpha = 0.6, edge_color = 'r')
                            plt.savefig("orig.png")
                            images.append(imageio.imread("orig.png"))
                            break
    #print([type(i ) for  i in images])
    imageio.mimsave("originalgif.gif",images)
    gif=imageio.mimread("originalgif.gif")
    imageio.mimsave("slowgif.gif",gif,fps=1)

# import matplotlib.animation
# ani = matplotlib.animation.FuncAnimation(G, DrawDFSPath, frames=6, interval=1000, repeat=True)



def showgraph():
    plt.clf()
    G1, source1 = CreateGraph()
    nx.draw(G1, with_labels=True, font_weight='bold')
    plt.savefig("graphfinal.png")

#main function
def printgraph():
    G, source = CreateGraph()
    dfs_stk = DFS(G, source)
    DrawDFSPath(G, dfs_stk)
    plt.savefig("orig.png")

def CreateGraph2(node,finallist):
    plt.clf()
    G = nx.Graph() #create a graph
    for x in range(0,node):
        G.add_node(x)
    for x in finallist:
        print(*x)
        G.add_edge(x[0],x[1],length =x[2])
        
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.savefig("usergraph.png")
    return G
    

adj=[]
adjlist=[]
def adjacency(nodeb,edgesb,srcb):
    plt.clf()
    #node=int(input("No. of nodes"))
    node=int(nodeb)
    source=int(srcb)
    G=Graph(node)
    
    for n in range(0,node):
        G.set_vertex(n)
    #edgeslist=str(input("enter [[1, 2, 3], [2, 3, 4]] format"))
    
    finallist=json.loads(edgesb)
    global adjlist
    adjlist=finallist
    for x in finallist:
        G.set_edge(*x)
    
    usergraph=CreateGraph2(node,finallist)
    plt.clf()
    dfs_stk = DFS(usergraph, source)
    print(dfs_stk)
    DrawDFSPath(usergraph, dfs_stk)
    plt.savefig("userdfs.png")
    

    print(G.get_matrix())
    print(G.get_edges())
    print(G.get_vertex())
    
    #bfs
    
    
    global adj
    adj=G.get_matrix()

def adjacencylist():
    global adjlist
    return adjlist
    
def useradj():
    global adj
    return adj