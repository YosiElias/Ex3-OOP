# from src.GeoLocation import GeoLocation
#
#
# class Node:
#
#     def __init__(self, id:int, pos:tuple=None):
#         self._key = id
#         self._tag = -1
#         # self._location = pos
#         self._info = 99999
#         self._visited = False
#         self._maxDist = 1.7976931348623157E308
#
#
#     def get_location(self)->tuple:
#         return self._location
#     def get_id(self):
#         return self._key
#     def __repr__(self):
#         return "{}".format(self._location)
#
#     def get_tag(self):
#         return self._tag
#
#     def get_info(self):
#         return self._info
#
#     def set_info(self,s):
#         self._info = s
#
#     def set_tag(self,s):
#         self._tag = s
#
#     def get_visit(self):
#         return self._visited
#
#     def set_visit(self, b:bool):
#         self._visited = b
#
#     def get_maxDist(self):
#         return self._maxDist
#
#     def set_maxDist(self, n):
#         self._maxDist = n

import random


class Node:

    def __init__(self, id, pos:tuple=None):
        self._color = (245,255,250)
        self._key = id
        self._tag = -1
        self._info = float('inf')
        self._visited = False
        self._maxDist = 1.7976931348623157E308
        # self._location = pos
        if pos == None:
            self.set_location_random()
        else:
            if len(pos)==2:
                pos_new = float(pos[0]), float(pos[1])
            if len(pos)==3:
                pos_new = float(pos[0]), float(pos[1]), float(pos[2])
            self._location=pos_new
    def __repr__(self):
        return str(self._key)+': '#|edges_out| {} |edges in| {},'.format() Todo: complite

    def get_id(self):
        return self._key

    def get_tag(self):
        return self._tag

    def get_info(self):
        return self._info

    def set_info(self,s):
        self._info = s

    def set_tag(self,s):
        self._tag = s

    def get_visit(self):
        return self._visited

    def set_visit(self, b:bool):
        self._visited = b

    def get_maxDist(self):
        return self._maxDist

    def set_maxDist(self, n):
        self._maxDist = n

    def get_color(self):
        return self._color

    def set_color(self, color:tuple):
        self._color = color

    def get_location(self) -> tuple:
        return self._location

    def set_location_random(self):
        (x, y) =random.uniform(0,100),random.uniform(0,100)
        self._location = (x, y)