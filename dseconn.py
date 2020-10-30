from cassandra.cluster import Cluster, EXEC_PROFILE_GRAPH_DEFAULT
from cassandra.datastax.graph import GraphProtocol
from cassandra.datastax.graph.fluent import DseGraph


host = '10.101.33.239'

# Create an execution profile, using GraphSON3 for Core graphs
ep = DseGraph.create_execution_profile(
	'gquotes',
	graph_protocol=GraphProtocol.GRAPHSON_3_0)

cluster = Cluster(execution_profiles={EXEC_PROFILE_GRAPH_DEFAULT: ep}, contact_points=[host])
session = cluster.connect()

g = DseGraph.traversal_source(session=session)


traversal1 = g.V().has('person', 'name', 'Chet Kapoor').next()
#traversal1.iterate()

print(traversal1)
