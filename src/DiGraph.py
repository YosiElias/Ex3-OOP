from src.Egde import Edge
from src.Node import Node
from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):

    def __init__(self):
        self._Nodes = {}
        self._Edges = {}
        self.edges_from = {}
        self.edges_to = {}
        self.num_of_edges = 0
        self.MC = 0

    def __repr__(self):
        # ans = 'Nodes: '
        # for n in self._Nodes.values():
        #     ans = ans + str(n)+', '
        # ans = ans + '\nEdges: '
        # for e in self._Edges.values():
        #     ans = ans + str(e)+', '
        return '|V|={}, |E|={}'.format(len(self._Nodes), self.num_of_edges)


    def getNode(self, node_id: int) -> Node:
        return self._Nodes.get(node_id)

    def getN(self):
        return self._Nodes

    def getEdge(self, id1, id2):
        try:
            return self._Edges.get(str(id1) + "-" + str(id2))
        except:
            return None

    def get_all_v(self) -> dict:
        return self._Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        return self.edges_to[id1]


    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
       """
        return self.edges_from[id1]


    def v_size(self) -> int:
        return len(self._Nodes)

    def e_size(self) -> int:
        return self.num_of_edges

    def get_mc(self) -> int:
        return  self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        try:
            if ((id1)) in self._Nodes and ((id2)) in self._Nodes and not ((id2)) in self.edges_from[id1]:
                s1 = str(id1)
                s2 = str(id2)
                self._Edges[str(s1 + "-" + s2)] = Edge(id1, id2, weight)
                self.edges_from[id1][id2] = weight
                self.edges_to[id2][id1] = weight
                self.num_of_edges = self.num_of_edges + 1
                self.MC = self.MC + 1
                return True
            else:
                return False
        except:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        try:
            if not (node_id) in self._Nodes.keys():
                self._Nodes[(node_id)] = Node(node_id, pos)
                self.edges_from[node_id] = {}
                self.edges_to[node_id] = {}
                self.MC = self.MC + 1
                return True
            else:
                return False
        except:
            return False

    def getNeighboursDict(self, key: int) -> dict:
        return self.edges_from[key]

    def remove_node(self, node_id: int) -> bool:
        try:
            if (node_id) in self._Nodes.keys():
                for id_dest in self.edges_from[(node_id)].keys():
                    del self.edges_to[(id_dest)][(node_id)] # delete the edge from dict of 'edges_to'
                for id_src in self.edges_to[(node_id)].keys():
                    del self.edges_from[(id_src)][(node_id)] # delete the edge from dict of 'edges_to'
                del self.edges_from[(node_id)]# delete the dict of edges from dict of 'edges_from'
                del self.edges_to[(node_id)]# delete the dict of edges of 'edges_to'
                del self._Nodes[(node_id)]
                return True
            else:
                return False
        except:
            return False


    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        try:
            if (node_id2) in self.edges_from[(node_id1)]:
                s1 = str(node_id1)
                s2 = str(node_id2)
                del self._Edges[str(s1 + "-" + s2)]
                del self.edges_from[(node_id1)][(node_id2)]
                del self.edges_to[(node_id2)][(node_id1)]
                self.num_of_edges =  self.num_of_edges -1
                return True
            else:
                return False
        except:
            return False

    def getN(self):
        return self._Nodes


if __name__ == '__main__':
    g = DiGraph()
