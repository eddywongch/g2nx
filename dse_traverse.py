
from cassandra.cluster import Cluster, EXEC_PROFILE_GRAPH_DEFAULT
from cassandra.datastax.graph import GraphProtocol
from cassandra.datastax.graph.fluent import DseGraph

class DseLoader:
    def __init__(self, name):
        self.name = name

    def initialize(self):
         print("Initialize")

    def connect(self, ip):
         # Not blank
        if ip and ip.strip():
            self.ip = ip
        else:
            self.ip = '10.101.33.239' # default

        # Create an execution profile, using GraphSON3 for Core graphs
        self.ep = DseGraph.create_execution_profile(
            'gquotes',
            graph_protocol=GraphProtocol.GRAPHSON_3_0)

        self.cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: self.ep}, contact_points=[self.ip])
        self.session = self.cluster.connect()

        self.g = DseGraph.traversal_source(session=self.session)


    def traverse(self):
        g = self.g

        traversal1 = g.V().has('person', 'name', 'Chet Kapoor').next()
    

        #for v in verts:
        #    print(v)

        #for e in g.E():
        #    print(e)

        # Vertices
        verts = g.V()
        for v in verts:
            print("***", v.id )
            #for p in g.V(v).properties():
                #name = p.properties('name').value()
            #    print("key:",p.label, "| value: " ,p.value)

        # Edges
        edges = g.E()
        for e in edges:
            print("***", e.id, '\n' , DseLoader.parseEdgeId(e.id) )
            #for p in g.E(e).properties():
            #    print("key:",e.label, "| value: " ,e.value)

        return g

    ##################################################################
    # DSE Graph 6.8.x encodes vertex and edge ids in a particular way
    # 

    #############################################
    # Parses a DSE edge id string into its components
    # Example:
    # dseg:/person-mentioned-quote/bf720fd3069c1704fd25359e1ebb77e531c4949a/069ae73d2bc4f54419a6c3fc56a0723c1b041740
    # Returns:
    # A dict with the following:
    # source_label: person
    # dest_label: quote
    # edge_label: mentioned
    # source_id: bf720fd3069c1704fd25359e1ebb77e531c4949a
    # dest_id: 069ae73d2bc4f54419a6c3fc56a0723c1b041740

    def parseEdgeId(str):
        result = {}

        str_list = str.split('/')
        edge_str = str_list[1]
        edge_list = edge_str.split('-')
        
        result['source_label'] = edge_list[0]
        result['dest_label'] = edge_list[2]
        result['edge_label'] = edge_list[1]
        result['source_id'] = str_list[2]
        result['dest_id'] = str_list[3]

        return result

    #############################################
    # Parses a DSE vertex id string into its components
    # Example:
    # dseg:/person/bf720fd3069c1704fd25359e1ebb77e531c4949a
    # Returns:
    # A dict with the following:
    # vertex_label: person
    # vertex_id: bf720fd3069c1704fd25359e1ebb77e531c4949a


    def parseVertexId(str):
        result = {}

        str_list = str.split('/')    
        result['vertex_label'] = str_list[1]
        result['vertex_id'] = str_list[2]
    

        return result

    ####################################
    # Convert Gremlin edges to Nx edges
    # returns a Networkx graph
    def convertG2NxEdges(g):
        import networkx as nx
        GG = nx.Graph()
        
        # Edges
        edges = g.E()
        for e in edges:
            es = DseLoader.parseEdgeId(e.id)
            print("*** Edges", e.id , es)
            GG.add_edge(es['source_id'], es['dest_id'], edge_label=es['edge_label'], \
                        source_label=es['source_label'], dest_label=es['dest_label'])
            #for p in g.E(e).properties():
            #    print("key:",e.label, "| value: " ,e.value)

        # Vertices
        verts = g.V()
        for v in verts:
            print("*** Verts", v.id , DseLoader.parseVertexId(v.id))
            for p in g.V(v).properties():
                print("key:",p.label, "| value: " ,p.value)
                #G.nodes['Chet Kapoor']['title']='CEO'

        return GG



if __name__ == '__main__':
    dl = DseLoader("ql1")         # Constructor
    dl.initialize()                 # Init
    dl.connect('10.101.33.239')     # Connect


    g = dl.traverse()
    gg = DseLoader.convertG2NxEdges(g)

    ##print( list(gg.adjacency()) )
    