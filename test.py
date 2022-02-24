from contextlib import contextmanager

import networkx as nx

class Flow:
    def __init__(self, graph=None):
        self._graph = graph if graph else nx.DiGraph()
        self._current_node = None
        self._next_edge = None

    def make_node(self, obj):
        next_node = self._graph.number_of_nodes()
        self._graph.add_node(next_node, object=obj)
        if self._current_node is not None:
            self._graph.add_edge(self._current_node, next_node, object=self._next_edge)
        self._current_node = next_node
        self._next_edge = None

    def node(self):
        self.make_node("node")

    def make_edge(self, obj):
        self._next_edge = obj
        return self._cm()

    @contextmanager
    def _cm(self):
        current_node = self._current_node
        try:
            copy = self.copy()
            yield copy
        finally:
            self._next_edge = None
            self._current_node = current_node

    def wait(self, timeval):
        return self.make_edge(("wait", timeval))

    @property
    def graph(self):
        return self._graph.copy()

    def copy(self):
        f = Flow(self._graph)
        f._current_node = self._current_node
        f._next_edge = self._next_edge

        return f
        

def my_flow(f):
    f.node() # 0
    f.node() # 1
    f.wait(10) # (1,2)
    f.node() # 2
    with f.wait(15) as g: # (2,3)
        g.node() # 3
        g.node() # 4
    with f.wait(100) as h: # (2,5)
        h.node() # 5
        h.node() # 6
    with f.wait(1000) as i: # Does noting
        pass

    f.node() # 7 (connected to 2) - not desired

    h.node() # 8 (connected to 6) - not desired

    with f.wait(1337)as g: # (7,9)
        g.node() # 9
    f.wait(123) # (7,10) alternative to with for the last split
    f.node() # 10



def main():
    f = Flow()
    my_flow(f)

    print(f"Nodes: {f.graph.nodes.data()}")
    print(f"Edges: {f.graph.edges.data()}")

if __name__ == "__main__":
    main()
