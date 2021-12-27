from unittest import TestCase
from src.DiGraph import DiGraph


class TestDiGraph(TestCase):
    def test_graph(self):
        g = DiGraph()  # creates an empty directed graph
        for n in range(4):
            g.add_node(n)
        g.add_node(4, (1, 2))
        self.assertTrue(g.add_edge(0, 1, 1))
        self.assertTrue(g.add_edge(1, 0, 1.1))
        self.assertTrue(g.add_edge(1, 2, 1.3))
        self.assertTrue(g.add_edge(2, 3, 1.1))
        self.assertTrue(g.add_edge(1, 3, 1.9))

        self.assertFalse(g.add_node(0))  # need to be False
        self.assertTrue(g.add_node(5, (0, 0)))  # need to be True
        self.assertFalse(g.add_edge(1, 3, 1))  # need to be False
        self.assertEqual(g.get_all_v()[4].get_location(), (1, 2))
        self.assertTrue(g.all_in_edges_of_node(0) != None)
        self.assertTrue(g.all_out_edges_of_node(0) != None)
        self.assertTrue(g.remove_node(0))  # need to be True
        try:
            g.all_in_edges_of_node(0)
            self.assertTrue(False)  # if get to here it is error
        except:
            self.assertTrue(True)
        try:
            g.all_out_edges_of_node(0)
            self.assertTrue(False)  # if get to here it is error
        except:
            self.assertTrue(True)
        print(g.get_all_v())  # prints a dict with all the graph's vertices.
        print(g.all_in_edges_of_node(1))
        print(g.all_out_edges_of_node(1))

