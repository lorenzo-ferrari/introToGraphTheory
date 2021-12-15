"""
Draw a tree taken in input from "input.txt" and animate Breadth-First Search on it.
"""

from manim import *
from math import *
from collections import *
import random

class Node(VMobject):
    def __init__(self, label):
        super().__init__()
        self.body = Circle().set_stroke(color=WHITE).set_fill(color=BLACK, opacity=0.8)
        self.text = Text(label)

        self.add(self.body)
        self.add(self.text)

    def get_point(self, nodeB):
        """
        endpoint of the edge (self, nodeB)
        """
        dx = nodeB.get_x() - self.get_x()
        dy = nodeB.get_y() - self.get_y()

        if (dy == 0.0):
            y = 0
            x = 1
        else:
            r = abs(dx/dy)
            y = sqrt(1/(r*r+1))
            x = y*r

        if (dx < 0):
            x = -x
        if (dy < 0):
            y = -y

        x *= self.body.width/2
        y *= self.body.width/2
        return [self.get_x() + x, self.get_y() + y, 0]

class Edge(VMobject):
    def __init__(self, A, B):
        super().__init__()
        self.nodeA = A
        self.nodeB = B
        self.body = Line()

        self.add_updater(Edge.updater)
        self.add(self.body)
        self.update()

    def calcLenght(self):
        """
        edge's lenght based on position and dimension of nodes
        """
        x0 = self.nodeA.get_x()
        x1 = self.nodeB.get_x()
        dx = x1-x0

        y0 = self.nodeA.get_y()
        y1 = self.nodeB.get_y()
        dy = y1-y0

        r0 = self.nodeA.body.width / 2
        r1 = self.nodeB.body.width / 2

        d = sqrt(dx*dx + dy*dy)
        return d - (r0 + r1)

    def updater(self):
        """
        edge's position
        """
        if (self.calcLenght() > 0):
            p1 = self.nodeA.get_point(self.nodeB)
            p2 = self.nodeB.get_point(self.nodeA)
            self.body.become(Line(p1, p2, color=self.color)) #.add_tip(tip_lenght=0.2)
        else:
            self.body.become(Line([0,0,0], [0,0,0]))

    def animate_set_color(self, color):
        """
        change edge's color
        """
        self.remove_updater(Edge.updater)
        a = self.animate.set_color(color)
        self.add_updater(Edge.updater)
        return a

def makeTree(idx, xl=-5, xr=5, y=2, parent=None):
    """
    return list of animations for nodes in v's subtree
    """
    global nodes, graph
    x = (xl+xr)/2
    animations = [nodes[idx].animate.move_to([x, y, 0])]
    count = len(graph[idx])
    if parent != None:
        count -= 1
    if count != 0:
        size = (xr-xl)/count
        i = 0
        for nxt in graph[idx]:
            # for loops doesn't work by reference
            # use indexes to avoid slowing down
            if nxt != parent:
                animations += makeTree(nxt, xl + i*size, xl + (i+1)*size, y-1, idx)
                i += 1
    return animations

class Bfs(Scene):
    """
    main scene
    """
    def construct(self):
        global nodes, edges, graph
        nodes = []
        edges = []
        graph = []

        with open("input.txt", "r") as file:
            """
            take the graph in input
            """
            nm = file.readline()
            n = int(nm.split()[0])
            m = int(nm.split()[1])

            for i in range(n):
                x = random.randrange(-4, 4)
                y = random.randrange(-3, 3)
                nodes.append(Node(str(i)).shift([x, y, -1]).scale(0.4))
                graph.append([])

            for i in range (m):
                l = file.readline()
                a = int(l.split()[0])
                b = int(l.split()[1])
                edge = Edge(nodes[a], nodes[b])
                edges.append(edge)
                graph[a].append(b)
                graph[b].append(a)

        title = Title("BFS - Breadth First Search")
        self.add(title)

        for node in nodes:
            self.add(node)
        for edge in edges:
            self.add(edge)

        self.wait()
        self.play(*makeTree(0, -6, 6, 2))
        self.wait()

        for edge in edges:
            edge.remove_updater(Edge.updater)

        rect = SurroundingRectangle(nodes[0], buff=0.1, color=GREEN)
        self.play(Create(rect))

        self.bfs(rect)
        self.wait()

    def bfs(self, rect):
        global nodes, edges, graph
        Q = deque()
        visited = [False for _ in range(len(nodes))]
        Q.append(0)
        visited[0] = True
        nodes[0].set_fill(BLUE, opacity=1)
        nodes[0].text.set_color(BLACK)
        while len(Q) > 0:
            u = Q.popleft()
            newRect = SurroundingRectangle(nodes[u], buff=0.1, color=GREEN)
            self.play(rect.animate.become(newRect), run_time=1.0)
            nodes[u].set_fill(YELLOW, opacity=1)
            nodes[u].text.set_color(BLACK)
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    nodes[v].set_fill(BLUE, opacity=1)
                    nodes[v].text.set_color(BLACK)
                    Q.append(v);
