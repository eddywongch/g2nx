# Configure the environment so the Python Console can connect to
# a Gremlin Server using gremlin-python and a web socket connection.

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import *
import os

#server = os.environ["10.101.33.239"]
#port = os.environ["8182"]
server = "10.101.33.239"
port = "8182"

endpoint = 'ws://' + server + ':' + port + '/gremlin'
print(endpoint)

graph=Graph()
connection = DriverRemoteConnection(endpoint,'gquotes.g')
g = graph.traversal().withRemote(connection)

a = g.V().hasLabel('person').has('name','Chet Kapoor').next()

p = g.V(a).properties()
for pp in p:
        print(pp)
