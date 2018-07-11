import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random, math

class node:
    def __init__(self,ID):
        self.ID = ID
        self.channels = []
        self.channelcount = 0
    def create_channel(self,partner_ID):
        self.channels.append(partner_ID)
        self.channelcount+=1
        return ('Successfully established channel to ',partner_ID)
    def pop_channel(self,partner_ID):
        '''
        Accpets a partner ID as int and deletes any existing chanel to that partner.
        ATTENTION! Make sure, also the partner deletes that chane
        '''
        if partner_ID in channels:
            del channels[partner_ID]
            return ('Succssfully canceled channel to ',partner_ID)
        else:
            return ('Found no existing channel to ',partner_ID)
    def get_channelcount(self):
        return self.channelcount
    def get_all_channels(self):
        return self.channels
    def get_ID(self):
        return self.ID

#max_node_space = 2**256 #just fills the screen with numbers, can also use lower search space
max_node_space = 10**9
simulated_nodes = 10
chanels_per_node = 2 #Each node makes two connection requests to random other nodes, also each node accepts all incomming conneciton requests from other nodes

#Pick nodes at random out of node space and put them in the list nodes
nodes = []
all_nodes_IDs = []
candidate = random.randint(0,max_node_space)
for x in range(simulated_nodes):
    while candidate in all_nodes_IDs:
        candidate = random.randint(0,max_node_space)
    nodes.append(node(int(candidate)))
    all_nodes_IDs.append(int(candidate))

print(all_nodes_IDs)

connections = []

for x in range(simulated_nodes):
    node_a_pos = x
    node_b_pos = node_a_pos
    while nodes[x].get_channelcount < chanels_per_node:
        while node_b_pos == node_a_pos:
            node_b_pos = random.choice(len(all_nodes_IDs))
        candidate =(node_a_pos,node_b_pos)
        if not candidate in connections:
            connections.append(candidate)
            nodes[x].create_channel(nodes[node_b_pos].get_ID)

print('Done')


'''
#Make connections between nodes so that each node has the specified amount of channels to other nodes
connections = []

G = nx.Graph()
G.add_edges_from(connections)

val_map = {'A': 1.0,
           'D': 0.5714285714285714,
           'H': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

nx.draw(G, cmap = plt.get_cmap('jet'), node_color = values)
plt.show()
'''