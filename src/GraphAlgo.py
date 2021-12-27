import json
import queue

# from sqlalchemy import null
from queue import PriorityQueue
from src.Egde import Edge
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.Node import Node
import GUI
from collections import deque
from decimal import Decimal
from typing import List
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from heapq import heappush, heappop  # Todo: !
from itertools import count




class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g:DiGraph=None):
        # self._graph = self.load_from_json(path)
        self._graph = g # Todo: change from None
        self.INF = float('inf')

    def get_graph(self):
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self._graph


    def load_from_json(self, file_name: str) -> bool:
        """
       Loads a graph from a json file.
       @param file_name: The path to the json file
       @returns True if the loading was successful, False o.w.
       """
        try:
            g = is_load(file_name)
            if g == None:
                return False
            else:
                self._graph = g
                return True
        except:
            return False


    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w') as f:
                dict_to_save = {}
                dict_to_save["Edges"] = self._graph._Edges
                for node in self._graph.getN().values():    # convert 'info' to str for legal json file
                    if node.get_info() == float('inf'):
                        node.set_info(str(node.get_info()))
                dict_to_save["Nodes"] = self._graph.getN()
                json.dump(dict_to_save, indent=2, fp=f, default=lambda a: a.__dict__)
                for node in self._graph.getN().values():  # convert 'info' back to float for the next use of this data
                    node.set_info(float(node.get_info()))
            return True
        except:
            return False


    def shortest_path(self, id1: int, id2: int):
        """
         Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        :param id1: The start node id
        :param id2: The end node id
        :return: The distance of the path, a list of the nodes ids that the path goes through
        """
        curr = self._graph.getNode((id1))
        dest = self._graph.getNode((id2))
        if curr is None or dest is None:
            return float(self.INF), []
        n_list = self._graph.getN()
        GraphAlgo.reset(self, n_list)
        curr.set_info(0)
        push = heappush # Todo: !
        pop = heappop
        c = count()
        heap = []
        push(heap, (0, next(c), curr))

        # pq = PriorityQueue()
        # pq.put((0,curr))
        curr.set_visit(True)

        # while not pq.empty():
        while heap: # !
            # (dist, cur_n) = pq.get()
            (dist, _, cur_n) = pop(heap)
            cur_key = cur_n.get_id()
            cur_n.set_visit(True)
            dic = DiGraph.getNeighboursDict(self._graph, cur_n.get_id())
            for neighbour in dic.keys():
                i = neighbour
                node = self._graph.getNode((i))
                if Node is not None and node.get_visit() is False:
                        edge = self._graph.getEdge(str(cur_key), str(node.get_id()))
                        new_tag = edge.get_weight() + cur_n.get_info()
                        if (new_tag < self.INF and node.get_info() == self.INF) or node.get_info() > new_tag:
                            node.set_tag(cur_key)
                            node.set_info(new_tag)
                            # if node.get_visit() is False:
                                # pq.put((new_tag, node))
                                # push(heap, (new_tag, next(c), node)) # !
                                # node.set_visit(True)
                else:
                    print("----------------------******************----------------")
        if dest.get_info() is self.INF:
            return float('inf'), []  #Todo: yossi change this from: 'return float(self.INF), []'
        path_list = GraphAlgo.find_path(self, id2, id1)
        return dest.get_info(), path_list


    def find_path(self, dest: int, src: int):
        curr = self._graph.getNode((dest))
        stack = deque()
        while curr.get_id() is not src:
            stack.append(curr)
            if curr.get_tag is self.INF:
                return []
            curr = self._graph.getNode((curr.get_tag()))
        stack.append(curr)

        counter = GraphAlgo.index_num(self, stack)
        list = []
        for i in range(counter):
            temp_n = stack.pop()
            list.append(temp_n.get_id())    #Todo: yossi change from: 'list.append(temp_n)'
        return list


    def index_num(self, stack: deque):
        cou = 0
        for i in stack:
            cou = cou+1
        return cou

    def reset(self, node_list: dict):
        for id in node_list:
            node: Node = node_list.get((id))
            node.set_tag(-1)
            node.set_info(self.INF)
            node.set_visit(False)

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        finalCost = 0
        path = []
        path.append(node_lst[0])
        tempPath = []

        for j in range(len(node_lst)): #loop on all the cities and search path from the city that my path get to NodeData
            src_id = path[len(path) - 1]   #take the last node in the path
            minCost = float('inf')
            # reset distances from 'src' node:
            if (j == 0 and len(node_lst) >= 2):  # if first loop AND have >= 2 node in cities:
                comparTo_id = node_lst[1]
            else:
                comparTo_id = node_lst[0]
            short_path =  self.shortest_path(src_id, comparTo_id)

            for i in range(len(node_lst)):
                dest:Node = self._graph.getNode(node_lst[i])
                if (not dest.get_id() == src_id and not dest.get_id() in path):
                    # not check path from node to itself AND search only for nodes that not in the path yet
                    cost = dest.get_info()
                    if (cost < minCost):
                        minPath = self.shortest_path(src_id, dest.get_id())[1] #Todo: check that the second play of 'shortest_path' is not arm the 'info' of dist of all nodes
                        del minPath[0]
                        minCost = cost
                        tempPath = minPath
            for i in range(len(tempPath)):
                # add the chosen path to cost and to path
                path.append(tempPath[i])
            tempPath = []
            if not minCost==float('inf'):
                finalCost =  finalCost + minCost

        return (path, finalCost)


    def centerPoint(self):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        n_list = self._graph.getN()
        # update the largest distance to every node - to be distance from every node to the his furthest other node
        for no in n_list:
            if no == str(len(n_list) -1):
                max_dist = -float('inf')
                cur_n = self._graph.getNode((no))
                n = int(no)
                self.shortest_path(n, n-1)
            else:
                max_dist = -float('inf')
                cur_n = self._graph.getNode((no))
                n = int(no)
                self.shortest_path(n,n+1)
            for node in n_list:
                if no is not node:
                    temp_n = self._graph.getNode((node))
                    dist = temp_n.get_info()
                    if dist is not self.INF:
                        if dist > max_dist:
                            max_dist = dist
            cur_n.set_maxDist(max_dist)
        min_node = None
        max_val = self.INF
        for n in n_list:
            # search for the smallest distance of maxDist of all nodes:
            cur_n = self._graph.getNode((n))
            dist = cur_n.get_maxDist()
            if dist < max_val:
                max_val = dist
                min_node = cur_n
        return min_node.get_id(), min_node.get_maxDist() #Todo": add return for case without center: (-1, 'inf')



    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        :return: None
        """
        GUI.main(alg=self)
        # for node in self._graph.getN().values():
        #     # plot Nodes:
        #     node:Node
        #     loc = node.get_location()
        #     if loc == None:
        #         node.set_location_random()  # placed in a uniform random
        #         x, y = node.get_location()
        #     else:
        #         x, y = loc[0], loc[1]
        #     plt.plot(x, y, markersize=4, marker='o', color='deepskyblue')
        #     plt.text(x, y, str(node.get_id()), color="navy", fontsize=9)
        #     for neibr_id, w in self._graph.getNeighboursDict(node.get_id()).items():
        #         # plot Edges:
        #         neibr = self._graph.getNode(neibr_id)
        #         loc_neibr = neibr.get_location()
        #         if loc_neibr == None:
        #             neibr.set_location_random()  # placed in a uniform random
        #             x_, y_ = neibr.get_location()
        #         else:
        #             x_, y_ = loc_neibr[0], loc_neibr[1]
        #         plt.annotate("", xy=(x, y), xytext=(x_, y_), arrowprops=dict(arrowstyle="<-"),color="tomato",)
        # plt.show()

    def _str_(self):
        return self._graph




def is_load(file_name: str):
    f = open(str(file_name))
    _g = DiGraph()
    data = json.load(f)

    Node_list = data['Nodes']
    for node in Node_list:
        # n = Node(id=node['id'], pos=node['pos'])
        # i = n.get_id()
        pos = node['pos'].split(",")
        _g.add_node(node_id=node['id'], pos=tuple(pos))

    Edge_list = data['Edges']
    for edge in Edge_list:
        e = Edge(src=edge['src'], dest=edge['dest'], weight=edge['w'])
        source = e.get_src()
        dest = e.get_dest()
        w = e.get_weight()
        _g.add_edge(source, dest, w)
    f.close()
    return _g

def plot_result(java_p, python_p, title, x_title)->None:
    data = ['Small-Graph', '1,000-Nodes', '10,000-Nodes', '100,000 Nodes', '1,000,000 Nodes']
    java_pref = java_p # [20, 34, 30, 35, 27] #
    python_pref = python_p # [10, 10, 0, 0, 0]#
    x = np.arange(len(data))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, java_pref, width, label='Java')
    rects2 = ax.bar(x + width / 2, python_pref, width, label='Python')
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(x_title)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(data, rotation=50, ha="right")
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    fig.tight_layout()
    plt.show()



#############################################################################
#
# pygame function to display
# the graph and algorithm
#
#############################################################################

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
# import GraphAlgo
# from src.DiGraph import DiGraph
# from src.Node import Node
import math
import tkinter as tk
from tkinter import filedialog
from tkinter import END
from tkinter import messagebox
import ctypes

import datetime
from random import randrange
from typing import List, Tuple, Optional

# Constants and global variables
COLOR_BACKGROUND = [128, 0, 128]
FPS = 60

user32 = ctypes.windll.user32
W_SIZE,H_SIZE  = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
# H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
# W_SIZE = 800  # Width of window size

surface: Optional['pygame.Surface'] = None
timer: Optional[List[float]] = None

pygame.font.init()
FONT=pygame.font.SysFont('comicsans',20)
FONT_w=pygame.font.SysFont('comicsans',42)

def mainmenu_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 0, 40))


def Load_graph() -> None:
    """
    Load graph.

    :return: None
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    global algo
    algo = GraphAlgo()
    algo.load_from_json(file_path)
    min_max()
    root.destroy()

def save_graph() -> None:
    """
    save graph.

    :return: None
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    algo.save_to_json(file_path)
    root.destroy()


def short_path()->None:
    my_w = tk.Tk()
    my_w.title('Short path')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w, text='Enter id of source and destination: \n*enter with \'space\' i.e. \'src dest\'', width=30, font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Play Algorithm', command=lambda: short_path_help(), width=20)
    b1.grid(row=4, column=1)

    def short_path_help():
        resert_color()
        my_str1 = t1.get("1.0", END)  # read from one text box t1
        print(my_str1)
        # my_w.destroy()
        arr = [int(s) for s in my_str1.split() if s.isdigit()]
        src, dest = arr[0], arr[1]
        # src, dest = my_str1.split(",")
        print(src,", ",dest)
        d, path = algo.shortest_path((src), (dest))
        func_resulte["short_path"] = path
        func_resulte["short_dist"] = d
        for i in range(len(path)-1):
            src_id = (path[i])
            dest_id = (path[i+1])
            e = algo.get_graph().getEdge(src_id, dest_id)
            e.set_color((127,255,0))
        messagebox.showinfo("Short Path", "The distance between the vertices is: \n{}\nThe shortest path is:\n->{}".format(d,path))
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()
    my_w.mainloop()  # Keep the window open

def center():
    resert_color()
    my_w = tk.Tk()
    c = algo.centerPoint()[0]
    messagebox.showinfo("Center Point","The center point is: \n{}\n".format(c))
    c_node = algo.get_graph().getNode(c)
    c_node.set_color((255,255,0))
    my_w.destroy()
    pygame.display.flip()

def tsp()->None:
    my_w = tk.Tk()
    my_w.title('TSP')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w, text='Enter id\'s for the TSP function: \n*enter with \'space\' i.e. \'2 1 8\'', width=30,
                  font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Play Algorithm', command=lambda: tsp_help(), width=20)
    b1.grid(row=4, column=1)

    def tsp_help():
        resert_color()
        my_str1 = t1.get("1.0", END)  # read from one text box t1
        print(my_str1)
        arr = [int(s) for s in my_str1.split() if s.isdigit()]
        # src, dest = my_str1.split(",")
        path, d = algo.TSP(arr)
        for i in range(len(path) - 1):
            src_id = (path[i])
            dest_id = (path[i + 1])
            e = algo.get_graph().getEdge(src_id, dest_id)
            e.set_color((127, 255, 0))
        messagebox.showinfo("TSP","The minimum path weight that passes between all selected points is:\n{}\nThe shortest path is:\n->{}".format(d, path))
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()

    my_w.mainloop()  # Keep the window open

def add_n():
    my_w = tk.Tk()
    my_w.title('Add Node')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w, text='Enter id and location for the new node: \n*enter with \'space\' i.e. \'id x y\'', width=30,
                  font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Add Node', command=lambda: add_n_help(), width=20)
    b1.grid(row=4, column=1)

    def add_n_help():
        try:
            resert_color()
            my_str1 = t1.get("1.0", END)  # read from one text box t1
            print(my_str1)
            arr = [float(s) for s in my_str1.split()]
            id, x, y = arr
            if algo.get_graph().add_node(int(id), (x, y, 0)):
              messagebox.showinfo("Add Node","Node successfully added :)")
              min_max()
            else:
                messagebox.showinfo("Add Node", "Error: Node not added, check input and try again! :(")
        except:
            messagebox.showinfo("Add Node", "Error:\nNode not added, check input and try again! :(")
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()
    my_w.mainloop()  # Keep the window open

def add_e():
    my_w = tk.Tk()
    my_w.title('Add Edge')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w, text='Enter id\'s of nodes to connect and wight for the new edge: \n*enter with \'space\' i.e. \'4 7 1.27\'', width=30,
                  font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Add Edge', command=lambda: add_e_help(), width=20)
    b1.grid(row=4, column=1)

    def add_e_help():
        try:
            resert_color()
            my_str1 = t1.get("1.0", END)  # read from one text box t1
            print(my_str1)
            arr = [float(s) for s in my_str1.split(' ')]
            src, dest, w = arr
            if algo.get_graph().add_edge(int(src), int(dest), w):
              messagebox.showinfo("Add Edge","Edge successfully added :)")
              min_max()
            else:
                messagebox.showinfo("Add Edge", "Error: Edge not added, check input and try again! :(")
        except:
            messagebox.showinfo("Add Node", "Error:\nEdge not added, check input and try again! :(")
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()
    my_w.mainloop()  # Keep the window open

def remove_n():
    my_w = tk.Tk()
    my_w.title('Remove Node')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w,
                  text='Enter id of node to remove:',
                  width=30,
                  font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Remove Node', command=lambda: remove_n_help(), width=20)
    b1.grid(row=4, column=1)

    def remove_n_help():
        try:
            resert_color()
            my_str1 = t1.get("1.0", END)  # read from one text box t1
            print(my_str1)
            arr = [int(s) for s in my_str1.split(' ')]
            id = arr[0]
            if algo.get_graph().remove_node(id):
                messagebox.showinfo("Remove Node", "Node successfully removed :)")
                min_max()
            else:
                messagebox.showinfo("Remove Node", "Error:\nNode not removed, check input and try again! :(")
        except:
            messagebox.showinfo("Remove Node", "Error:\nNode not removed,, check input and try again! :(")
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()

    my_w.mainloop()  # Keep the window open

def remove_e():
    my_w = tk.Tk()
    my_w.title('Remove Edge')
    my_font1 = ('times', 18, 'bold')
    l1 = tk.Label(my_w,
                  text='Enter id\'s of nodes to remove their edge:\n*enter with \'space\' i.e. \'4 7\'',
                  width=30,
                  font=my_font1)
    l1.grid(row=1, column=1)

    t1 = tk.Text(my_w, width=40, height=3)
    t1.grid(row=2, column=1)

    b1 = tk.Button(my_w, text='Remove Edge', command=lambda: remove_e_help(), width=20)
    b1.grid(row=4, column=1)

    def remove_e_help():
        try:
            resert_color()
            my_str1 = t1.get("1.0", END)  # read from one text box t1
            print(my_str1)
            arr = [int(s) for s in my_str1.split(' ')]
            src, dest = arr
            if algo.get_graph().remove_edge(src, dest):
                messagebox.showinfo("Remove Edge", "Node successfully removed :)")
                min_max()
            else:
                messagebox.showinfo("Remove Edge", "Error:\nEdge not removed, check input and try again! :(")
        except:
            messagebox.showinfo("Remove Edge", "Error:\nEdge not removed,, check input and try again! :(")
        my_w.destroy()
        pygame.display.flip()
        pygame.display.update()
    my_w.mainloop()  # Keep the window open

def resert_color()->None:
    """
    reset color of all edges
    :return: None
    """
    for e in algo.get_graph()._Edges.values():
        e.set_color((255,52,179))



class TestCallClassMethod(object):
    """
    Class call method.
    """

    @staticmethod
    def update_game_settings() -> None:
        """
        Class method.

        :return: None
        """
        print('Update game with new settings')


def change_color_bg(value: Tuple, c: Optional[Tuple] = None, **kwargs) -> None:
    """
    Change background color.

    :param value: Selected option (data, index)
    :param c: Color tuple
    :return: None
    """
    color, _ = value
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: {0} ({1},{2},{3})'.format(color[0], *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]

def main(test: bool = False, alg:GraphAlgo=None) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    # # Write help message on console
    # for m in HELP:
    #     print(m)

    # Create window
    global surface
    global func_resulte
    global algo
    algo = alg
    surface = create_example_window('MY GRAPH', (W_SIZE, H_SIZE))
    func_resulte = {}

    if algo != None:
        # scale all point:
        min_max()

    # clock = pygame.time.Clock()
    global timer
    # timer = [0]
    dt = 1.0 / FPS
    timer_font = pygame_menu.font.get_font(pygame_menu.font.FONT_NEVIS, 100)
    frame = 0

    # -------------------------------------------------------------------------
    # Create menus: File
    # -------------------------------------------------------------------------

    timer_theme = pygame_menu.themes.THEME_DARK.copy()  # Create a new copy
    timer_theme.background_color = (0, 0, 0, 180)  # Enable transparency

    # file
    file_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=timer_theme,
        title='File Menu',
        width=600
    )

    # Add widgets
    file_menu.add.button('Load New Graph', Load_graph)
    file_menu.add.button('Save Graph', save_graph)

    # Adds a selector (element that can handle functions)
    # file_menu.add.selector(
    #     title='Change color ',
    #     items=[('Random', (-1, -1, -1)),  # Values of selector, call to change_color_bg
    #            ('Default', (128, 0, 128)),
    #            ('Black', (0, 0, 0)),
    #            ('Blue', (12, 12, 200))],
    #     default=1,  # Optional parameter that sets default item of selector
    #     onchange=change_color_bg,  # Action when changing element with left/right
    #     onreturn=change_color_bg,  # Action when pressing return on an element
    #     # All the following kwargs are passed to change_color_bg function
    #     write_on_console=True
    # )
    # file_menu.add.button('Update game object', TestCallClassMethod().update_game_settings)
    file_menu.add.button('Return to Menu', pygame_menu.events.BACK)
    file_menu.add.button('Close Menu', pygame_menu.events.CLOSE)

    # -------------------------------------------------------------------------
    # Create menus: Function
    # -------------------------------------------------------------------------
    function_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=timer_theme,
        width=600,
        title='Function Menu',
    )
    # Add widgets
    function_menu.add.button('Short Path', short_path)
    function_menu.add.button('Center', center)
    function_menu.add.button('TSP', tsp)
    function_menu.add.button('Return to Menu', pygame_menu.events.BACK)


    # -------------------------------------------------------------------------
    # Create menus: Edit
    # -------------------------------------------------------------------------
    edit_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=timer_theme,
        width=600,
        title='Edit Menu',
    )
    # Add widgets
    edit_menu.add.button('Add Node', add_n)
    edit_menu.add.button('Add Edge', add_e)
    edit_menu.add.button('Remove Node', remove_n)
    edit_menu.add.button('Remove Edge', remove_e)
    edit_menu.add.button('Return to Menu', pygame_menu.events.BACK)


    # -------------------------------------------------------------------------
    # Create menus: About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_font = pygame_menu.font.FONT_NEVIS
    about_theme.title_font = pygame_menu.font.FONT_8BIT
    about_theme.title_offset = (5, -2)
    about_theme.widget_offset = (0, 0.14)

    about_menu = pygame_menu.Menu(
        center_content=False,
        height=400,
        # mouse_visible=False,
        theme=about_theme,
        title='About',
        width=600
    )
    m= "Assignment 3: Graphs\n" \
       "Authors: Roee Tal and Yossi Elias\n\n" \
      "We have created this interface\n in order to make the operation of the\n functions more accessible\n\n" \
       "We hope the use of this \ninterface is as intuitive and convenient \nas we tried to create it."

    about_menu.add.label(m, margin=(0, 0))
    # about_menu.add.label('')
    about_menu.add.button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu = pygame_menu.Menu(
        enabled=False,
        height=400,
        theme=pygame_menu.themes.THEME_DARK,
        title='Main Menu',
        width=600
    )

    main_menu.add.button(file_menu.get_title(), file_menu)  # Add submenu
    main_menu.add.button(function_menu.get_title(), function_menu)  # Add func submenu
    main_menu.add.button(edit_menu.get_title(), edit_menu)  # Add edit submenu
    main_menu.add.button(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add.button('Exit', pygame_menu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------

    time = pygame.time.get_ticks()
    while pygame.time.get_ticks()-time<950:
        frame += 1

        current_menu = main_menu.get_current()
        if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():
            welcome(False)
        else:
            # Background color if the menu is enabled and graph is hidden
            surface.fill((40, 0, 40))
        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and \
                        current_menu.get_title() == 'Main Menu':
                    main_menu.toggle()

        if main_menu.is_enabled():
            main_menu.draw(surface)
            main_menu.update(events)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test and frame == 2:
            break

    else:
        while True:


            frame += 1

            # Title is evaluated at current level as the title of the base pointer
            # object (main_menu) can change if user opens submenus
            current_menu = main_menu.get_current()
            if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():
                if algo != None:
                    # Draw
                    draw()
                else:
                    # surface.fill((0, 0, 0))
                    welcome(True)
            else:
                # Background color if the menu is enabled and graph is hidden
                surface.fill((40, 0, 40))

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and \
                            current_menu.get_title() == 'Main Menu':
                        main_menu.toggle()

            if main_menu.is_enabled():
                main_menu.draw(surface)
                main_menu.update(events)

            # Flip surface
            pygame.display.flip()

            # At first loop returns
            if test and frame == 2:
                break

def welcome(text:bool):
    image = pygame.image.load(r'C:\Users\Aviva\Desktop\Ex3\data\welcome.jpg')
    image = pygame.transform.scale(image, (W_SIZE, H_SIZE))
    # copying the image surface object to the display surface object at (0, 0) coordinate.
    surface.blit(image, (0, 0))
    if text:
        w_text = FONT_w.render("To load a graph please press esc->File Menu->Load Graph", True, (0,0,0))
        surface.blit(w_text, (105,45))

def draw(src_=-1):#algo:GraphAlgo=None,
    surface.fill((0,134,139))
    esc_text = FONT.render("To get to the Main-Menu please press->\'esc\'", True, (0, 0, 0))
    surface.blit(esc_text, (50, 45))
    for src in algo.get_graph().getN().values():
        # src = algo.get_graph().getNode(src_id)
        x=my_scale(src.get_location()[0],x=True)
        y = my_scale(src.get_location()[1], y=True)
        pygame.draw.circle(surface, src.get_color(),(x,y),radius=7)
        src_text = FONT.render(str(src.get_id()), True, src.get_color())
        surface.blit(src_text, (x,y))
        # node_screens.append(NodeScreen(pygame.Rect((x,y),(20,20)),src.get_id()))

        for dest in algo.get_graph().all_out_edges_of_node(src.get_id()):
            dest=algo.get_graph().getNode(dest)
            his_x=my_scale(dest.get_location()[0],x=True)
            his_y = my_scale(dest.get_location()[1], y=True)
            e = algo.get_graph().getEdge(src.get_id(), dest.get_id())
            # if (src.get_id(),dest.get_id()) in result:
            #     arrow((x,y), (his_x,his_y), 17, 7, color=(0,250,0))
            # else:
            arrow((x, y), (his_x, his_y), 17, 7, color=e.get_color())
            e_other = algo.get_graph().getEdge(dest.get_id(), src.get_id())
            if e_other != None and e_other.get_color() == (127, 255, 0):
                pygame.draw.line(surface, e_other.get_color(), start_pos=(x,y),end_pos=(his_x,his_y),width=3)
            else:
                pygame.draw.line(surface, e.get_color(), start_pos=(x,y),end_pos=(his_x,his_y),width=3)

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimensions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen
min_x=min_y=max_x=max_y=0
def min_max():
    global min_x,min_y,max_x,max_y
    min_x = min(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[0]).get_location()[0]
    min_y = min(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[1]).get_location()[1]
    max_x = max(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[0]).get_location()[0]
    max_y = max(list(algo.get_graph().getN().values()), key=lambda n: n.get_location()[1]).get_location()[1]
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, surface.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, surface.get_height() - 50, min_y, max_y)

def arrow(start, end, d, h, color):
    dx =(end[0] - start[0])
    dy =(end[1] - start[1])
    D = (math.sqrt(dx * dx + dy * dy))
    xm =(D - d)
    xn =(xm)
    ym =(h)
    yn = -h
    sin = dy / D
    cos = dx / D
    x = xm * cos - ym * sin + start[0]
    ym = xm * sin + ym * cos + start[1]
    xm = x
    x = xn * cos - yn * sin + start[0]
    yn = xn * sin + yn * cos + start[1]
    xn = x
    points = [(end[0], end[1]), (int(xm), int(ym)), (int(xn), int(yn))]

    # pygame.draw.line(surface, color, start, end, width=3)
    pygame.draw.polygon(surface, color, points)

def display():
    # button.func=algo.my_algo
    min_max(algo.graph)
    # run=True
    src=-1
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type\
                    ==pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.get_location()):
                    button.press()
                    if button.is_pressed:
                        on_click(button.func)
                    else:
                        result.clear()
                for n in node_screens:
                    if n.rect.collidepoint(event.get_location()):
                        src=n.get_id()

        surface.fill((250,250,250))
        draw(algo,src)
        pygame.display.update()











if __name__ == '__main__':
    jsonPath = 'A0.json'
    # file = "../../data/A0.json"
    # _graph = GraphAlgo(path=jsonPath)
    graph = GraphAlgo()
    graph.load_from_json(jsonPath)
    graph.plot_graph()
    # d = GraphAlgo.shortest_path(graph, 0, 1)
    # i = GraphAlgo.centerPoint(graph)
    # graph.get_graph().getNode(0).set_info(float('inf'))
    # graph.save_to_json('output.json')
    # _graph2 = getG.get_g('A0.json')
    # print(type(_graph2))
    # dic = Graph.getNeighboursDict(_graph2, 8)

    # _graph2.add_node(11)
    # n = _graph2.getNode(str(1))
    a = 3
    # _graph2.plot_graph()

    # _graph = GraphAlgo.get_g('A0.json')
    # _graph.plot_graph()


    # plot the resule:
    center_j = [0.111, 11.62, 2280, 0, 0]
    # short_j = [0.112, 0.309, 1.146, 0, 0]
    # tsp_j = [0.249, 1.205, 9.453, 0, 0]
    # tsp_j_W = [14.2329, 4316.4518, 4811.0436, 0, 0]
    #
    center_p = [1000, 100, 100, 1000, 1000] # Todo: update best result, tsp path for all: {1,3,5,7,9,0}
    # short_p = [1000, 100, 100, 1000, 1000]
    # tsp_p = [1000, 100, 100, 1000, 1000]
    # tsp_p_W = [1000, 100, 100, 1000, 1000]
    #
    plot_result(center_j, center_p, "Comparison of performance of function \'Center\'", 'Time in Seconds')
    # plot_result(short_j, short_p, "Comparison of performance of function \'Short-path\'", 'Time in Seconds')
    # plot_result(tsp_j, tsp_p, "Comparison of performance of function \'TSP\' - time", 'Time in Seconds')
    # plot_result(tsp_j_W, tsp_p_W, "Comparison of performance of function \'TSP\' - path weight", "Path Weight")






























