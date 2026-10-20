import networkx as nx
import matplotlib.pyplot as plt

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Node:

    def __init__(self,variable,states,parents=None,children=None,cpt=None):
        self.variable = variable
        self.states = states
        self.parents = parents if parents is not None else []
        self.children = children if children is not None else []
        self.cpt = cpt if cpt is not None else {}

    def is_root(self):
        return len(self.parents) == 0

    def is_leaf(self):
        return len(self.children) == 0
        
class BayesianNetwork:
    def __init__(self):
        self.nodes_list = {}

    def add_node(self, node):
        """Adds a Node object to the Bayesian Network."""
        if node.variable not in self.nodes_list:
            self.nodes_list[node.variable] = node
        else:
            raise ValueError("The node is already in the Bayesian Network.")
        
    def add_edge(self,parent_name=None,child_name=None):

        #Ensure that the node that are in add_edge are in the bayesian Netowrk

        if parent_name not in self.nodes_list:
            raise ValueError("The parents node hasn't been added to Bayesian Network")
        if child_name not in self.nodes_list:
            raise ValueError("The child node hasn't been added to Bayesian Network")

        #Ensure that duplicate edges are not added
        if child_name in self.nodes_list[parent_name].children:
            raise ValueError("This edge already exists.")

        #Ensure that the edges doesn't form a cycle using DFS
        if parent_name == child_name:
            raise ValueError("Self loop is not allowed")

        visited = set()
        queue = Stack()
        queue.push(child_name)

        while not queue.isEmpty():
            current = queue.pop()
            if current == parent_name:
                raise ValueError("Adding edge create a cyclic graph")

            if current not in visited:
                visited.add(current)
                # Add all children of the current node to the search queue
                for next_child in self.nodes_list[current].children:
                    if next_child not in visited:
                        queue.push(next_child)
                
            

        #Add the child information to the node for parent node
        self.nodes_list[parent_name].children.append(child_name)
        #Add the parent information to the 
        self.nodes_list[child_name].parents.append(parent_name)

    def add_cpt(self, node_name, cpt):
        if node_name in self.nodes_list:
            self.nodes_list[node_name].cpt = cpt
        else:
            raise ValueError("The node hasn't been added to the Bayesian Network.")
        
    def visualize(self):
        """Visualizes the Bayesian Network using NetworkX and Matplotlib."""
        # 1. Create a directed graph
        G = nx.DiGraph()

        # 2. Add nodes and edges f
        for node_name, node_obj in self.nodes_list.items():
            G.add_node(node_name)
            for child in node_obj.children:
                G.add_edge(node_name, child)

      
        plt.figure(figsize=(8, 6))

        pos = nx.spring_layout(G, seed=42) 

        # 4. Draw the graph components
        nx.draw_networkx_nodes(G, pos, node_size=3000, node_color='lightblue', edgecolors='black')
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='gray', width=2, arrows=True, arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif', font_weight='bold')

        # 5. Display the plot
        plt.title("Bayesian Network Structure", fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.show()


