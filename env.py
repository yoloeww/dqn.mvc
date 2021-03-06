
import numpy as np
import networkx as nx
# build env for MVC
class env():
    """
    The following methods are needed:
    - reset: regenerate a instance(graph) and initialize records
    - step : take action and return state_next, reward, done 
    """
    def __init__(self, graph_size):
        self.graph_size = graph_size
        self.name = "MVC"
        self.reset()

    def reset(self):
        self.edge_index, self.edge_w = self._BA(self.graph_size) 
        self.node_tag = np.zeros((self.graph_size, 1), dtype=np.float32)
        self.done     = self._done()
        self.cover    = self._cover()
        self.cost     = -sum(self.node_tag)
        self.mu       = np.zeros((self.graph_size, 3), dtype=np.float32)

        return self.mu, self.edge_index, self.edge_w, self.node_tag, self.done,self.cover

    def step(self, action):
        assert action[0] in range(self.graph_size)
        self.node_tag[action[0]] = 1
        #new_cover = self._cover()
        #reward    = float(new_cover - 1.0 - self.cover)
        #self.cover = new_cover
        new_cost = -sum(self.node_tag)
        reward     = new_cost - self.cost
        self.cost = new_cost
        self.done = self._done()

        return self.mu, self.edge_index, self.edge_w, reward, self.node_tag, self.done

    def _BA(self, size):
        G          = nx.random_graphs.barabasi_albert_graph(n=size, m=3)
        edge_index = np.array(G.edges(), dtype=np.long).T  #边和边关系
        edge_w     = np.ones((G.number_of_edges(), 1), dtype=np.float32) #边的数量
        """
        edge_index = np.load("edge_index.npy")
        edge_w = np.load("edge_w.npy")
        """
        return edge_index, edge_w

    def _cover(self):
        # count the number of edges covered by nodes_tag
        edge_end0 = np.array([1 if self.node_tag[node] == 1 else 0 for node in self.edge_index[0]])
        edge_end1 = np.array([1 if self.node_tag[node] == 1 else 0 for node in self.edge_index[1]])

        return len(np.nonzero(edge_end0 + edge_end1)[0])
        
    def _done(self):
        # check if all nodes are covered
        half_remain_edges = [False if self.node_tag[node] == 1 else True for node in self.edge_index[0]]
        remain_nodes = self.edge_index[1][half_remain_edges] 

        if self.node_tag[remain_nodes].sum() == len(remain_nodes):
            done_flag = [1.0] 
        else:
            done_flag = [0.0]
        return done_flag
     
