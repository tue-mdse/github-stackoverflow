"""Copyright 2012-2013
Eindhoven University of Technology
Bogdan Vasilescu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUD ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import pydot
import os

from pygraph.classes.digraph import digraph
from pygraph.algorithms.critical import transitive_edges

'''Output path'''
dataPath = os.path.abspath("../../data/figures")


def tldGraph(edgeList, fileName):
    imgPath = os.path.join(dataPath, "%s.pdf" % fileName)
#    imgPath2 = os.path.join(dataPath, "%s.png" % fileName)

    '''Graph creation'''
    gr = digraph()
    
    '''Compute nodes from list of edges'''
    nodes = set()
    for edge in edgeList:
        nodes.add(edge[0])
        nodes.add(edge[1])
    
    '''Add nodes to graph'''
    gr.add_nodes(list(nodes))    
    
    '''Add edges to graph'''
    for edge in edgeList:
        gr.add_edge(edge)
    
    '''Compute transitive edges'''
    tr = transitive_edges(gr)
    
    '''Only display non-transitive edges'''
    ntrEdges = set(list(edgeList)).difference(set(tr))
    
    '''Visualization'''
    dgr = pydot.Dot(graph_type='digraph')
    #dgr.set_ranksep(0.2)
    #dgr.set_nodesep(0.05)
    #dgr.set_ratio(2)
    dgr.set_margin(0)
    dgr.set_node_defaults(fontname="Arial")
#    dgr.set_ordering('in')
    
    for edge in ntrEdges:
        dgr.add_edge(pydot.Edge(edge[0], edge[1]))
    
    '''Draw as PDF'''
    dgr.write_pdf(imgPath)
#    dgr.write_png(imgPath2)
    


'''Are top committers heavy SO askers?'''
edgeList = [("D 3", "D 1"), ("D 4", "D 1"), ("D 5", "D 1"), ("D 6", "D 1"), ("D 7", "D 1"), \
            ("D 8", "D 1"), ("D 9", "D 1"), ("D10", "D 1")]
tldGraph(edgeList, 'topC-Q')

edgeList = [("Q2", "Q1"), ("Q3", "Q1"), ("Q4", "Q1")]
tldGraph(edgeList, 'top4C-Q')

'''Are top committers heavy SO answerers?'''
edgeList = [("D 1", "D 2"), ("D 1", "D 3"), ("D 1", "D 4"), ("D 1", "D 5"), ("D 1", "D 6"), \
            ("D 1", "D 7"), ("D 1", "D 8"), ("D 1", "D 9"), ("D 1", "D10"), ("D 2", "D 4"), \
            ("D 2", "D 5"), ("D 2", "D 6"), ("D 2", "D 7"), ("D 2", "D 8"), ("D 2", "D 9"), \
            ("D 2", "D10"), ("D 3", "D 5"), ("D 3", "D 6"), ("D 3", "D 7"), ("D 3", "D 8"), \
            ("D 3", "D 9"), ("D 3", "D10"), ("D 4", "D 6"), ("D 4", "D 7"), ("D 4", "D 8"), \
            ("D 4", "D 9"), ("D 4", "D10"), ("D 5", "D 9"), ("D 5", "D10")]
tldGraph(edgeList, 'topC-A')

edgeList = [("Q1", "Q2"), ("Q1", "Q3"), ("Q1", "Q4"), ("Q2", "Q3"), ("Q2", "Q4"), ("Q3", "Q4")]
tldGraph(edgeList, 'top4C-A')


'''Are top SO askers heavy committers?'''
edgeList = [("D 1", "D 5"), ("D 1", "D 6"), ("D 9", "D 2"), ("D10", "D 2"), ("D 8", "D 3"), \
            ("D 9", "D 3"), ("D10", "D 3"), ("D 8", "D 4"), ("D 9", "D 4"), ("D10", "D 4"), \
            ("D 8", "D 5"), ("D 9", "D 5"), ("D10", "D 5"), ("D 8", "D 6"), ("D 9", "D 6"), \
            ("D10", "D 6"), ("D 9", "D 7"), ("D10", "D 7")]
tldGraph(edgeList, 'topQ-C')

edgeList = [("Q1", "Q2"), ("Q4", "Q1"), ("Q4", "Q2"), ("Q4", "Q3")]
tldGraph(edgeList, 'top4Q-C')


'''Are top SO answerers heavy committers?'''
edgeList = [("D 1", "D 2"), ("D 1", "D 3"), ("D 1", "D 4"), ("D 1", "D 5"), ("D 1", "D 6"), \
            ("D 1", "D 7"), ("D 1", "D 8"), ("D 1", "D 9"), ("D 1", "D10"), ("D 2", "D 5"), \
            ("D 2", "D 6"), ("D 2", "D 7"), ("D 2", "D 8"), ("D 2", "D 9"), ("D 2", "D10"), \
            ("D 3", "D 6"), ("D 3", "D 8"), ("D 3", "D 9"), ("D 3", "D10"), ("D 4", "D 6"), \
            ("D 4", "D 8"), ("D 4", "D 9"), ("D 4", "D10"), ("D 5", "D 8"), ("D 5", "D 9"), \
            ("D 5", "D10"), ("D 6", "D 9"), ("D 6", "D10"), ("D 7", "D 8"), ("D 7", "D 9"), \
            ("D 7", "D10"), ("D 8", "D10")]
tldGraph(edgeList, 'topA-C')

edgeList = [("Q1", "Q2"), ("Q1", "Q3"), ("Q1", "Q4"), ("Q2", "Q3"), ("Q2", "Q4"), ("Q3", "Q4")]
tldGraph(edgeList, 'top4A-C')


'''Eval latencies - asking questions'''
edgeList = [("sim_0", "real"), ("sim_1", "real"), ("sim_2", "real"), ("sim_3", "real"), \
            ("sim_4", "real")]
tldGraph(edgeList, 'eval-Q')

'''Resp latencies - asking questions'''
edgeList = [("sim_1", "sim_2"), ("sim_0", "real"), ("sim_1", "real"), ("sim_2", "real"), \
            ("sim_3", "real"), ("sim_4", "real"), ("sim_3", "sim_2")]
tldGraph(edgeList, 'resp-Q')

'''Eval latencies - answering questions'''
edgeList = [] # empty
#tldGraph(edgeList, 'eval-A')

'''Resp latencies - answering questions'''
edgeList = [("sim_0", "real"), ("sim_1", "real"), ("sim_2", "real"), ("sim_3", "real"), \
            ("sim_4", "real")]
tldGraph(edgeList, 'resp-A')

'''Eval latencies - accepted answers'''
edgeList = [("sim_0", "real"), ("sim_1", "real"), ("sim_2", "real"), ("sim_3", "real"), \
            ("sim_4", "real")]
tldGraph(edgeList, 'eval-Z')

'''Resp latencies - accepted answers'''
edgeList = [("sim_0", "real"), ("sim_1", "real"), ("sim_2", "real"), ("sim_3", "real"), \
            ("sim_4", "real")]
tldGraph(edgeList, 'resp-Z')


