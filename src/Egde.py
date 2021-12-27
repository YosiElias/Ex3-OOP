class Edge:

    def __init__(self, src, dest, weight):
        self._src = src
        self._dest = dest
        self._weight = weight
        self._color = (255,52,179)

    def __repr__(self):
        return '('+str(self._src)+'->'+str(self._dest)+', w:'+str(self._weight)+')'

    def get_src(self):
        return self._src

    def get_dest(self):
        return self._dest

    def get_weight(self):
        return self._weight

    def get_color(self):
        return self._color

    def set_color(self, color:tuple):
        self._color = color