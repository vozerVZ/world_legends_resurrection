class Node:
    def __init__(self, _x, _y, _id, _r_n, _l_n, _u_n, _d_n):
        self.x = _x
        self.y = _y
        self.id = _id
        self.path = [[_x, _y]]
        self.path_len = -1
        self.r_n = _r_n
        self.l_n = _l_n
        self.u_n = _u_n
        self.d_n = _d_n
        self.done = False

    def set_path(self, _path_len, _path):
        self.path_len = _path_len
        copy_arr = _path.copy()
        self.path.clear()
        self.path = copy_arr.copy()

    def get_neighbours(self):
        neighs = []
        if self.r_n != -1: neighs.append(self.r_n)
        if self.l_n != -1: neighs.append(self.l_n)
        if self.u_n != -1: neighs.append(self.u_n)
        if self.d_n != -1: neighs.append(self.d_n)
        return neighs
