import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class Mesh(object):
    def __init__(self, cmin, cmax, d):
        self.cmin = cmin
        self.cmax = cmax
        self.d = d

    def show(self, figsize=(8, 10)):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_aspect('equal')
        
        x1 = self.cmin[0]
        y1 = self.cmin[1]
        z1 = self.cmin[2]

        x2 = self.cmax[0]
        y2 = self.cmax[1]
        z2 = self.cmax[2]

        xd = self.d[0] + x1
        yd = self.d[1] + y1
        zd = self.d[2] + z1

        # Plot atlas.
        ax.plot([x1, x2], [y1, y1], [z1, z1], 'b', linewidth=2)
        ax.plot([x1, x2], [y2, y2], [z1, z1], 'b', linewidth=2)
        ax.plot([x1, x2], [y1, y1], [z2, z2], 'b', linewidth=2)
        ax.plot([x1, x2], [y2, y2], [z2, z2], 'b', linewidth=2)

        ax.plot([x1, x1], [y1, y2], [z1, z1], 'b', linewidth=2)
        ax.plot([x2, x2], [y1, y2], [z1, z1], 'b', linewidth=2)
        ax.plot([x1, x1], [y1, y2], [z2, z2], 'b', linewidth=2)
        ax.plot([x2, x2], [y1, y2], [z2, z2], 'b', linewidth=2)

        ax.plot([x1, x1], [y1, y1], [z1, z2], 'b', linewidth=2)
        ax.plot([x2, x2], [y1, y1], [z1, z2], 'b', linewidth=2)
        ax.plot([x1, x1], [y2, y2], [z1, z2], 'b', linewidth=2)
        ax.plot([x2, x2], [y2, y2], [z1, z2], 'b', linewidth=2)

        # Plot cell.
        ax.plot([x1, xd], [y1, y1], [z1, z1], 'r', linewidth=2)
        ax.plot([x1, xd], [yd, yd], [z1, z1], 'r', linewidth=2)
        ax.plot([x1, xd], [y1, y1], [zd, zd], 'r', linewidth=2)
        ax.plot([x1, xd], [yd, yd], [zd, zd], 'r', linewidth=2)

        ax.plot([x1, x1], [y1, yd], [z1, z1], 'r', linewidth=2)
        ax.plot([xd, xd], [y1, yd], [z1, z1], 'r', linewidth=2)
        ax.plot([x1, x1], [y1, yd], [zd, zd], 'r', linewidth=2)
        ax.plot([xd, xd], [y1, yd], [zd, zd], 'r', linewidth=2)

        ax.plot([x1, x1], [y1, y1], [z1, zd], 'r', linewidth=2)
        ax.plot([xd, xd], [y1, y1], [z1, zd], 'r', linewidth=2)
        ax.plot([x1, x1], [yd, yd], [z1, zd], 'r', linewidth=2)
        ax.plot([xd, xd], [yd, yd], [z1, zd], 'r', linewidth=2)
        
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
