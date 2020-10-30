# g2nx
Conversion routines from Gremlin to NetworkX. These routines started as an effort to make NetworkX (on Jupiter Notebook) and Gremlin (DSE Graph) "talk" to each. For the moment, it is specific to DSE Graph. The main file is `dse_traverse.py`.

The conversion function goes from Gremlin to NetworkX. It should work generically for any graph.



#### Requirements

- Python 3.5+
- DSE Graph 6.8.4
- Cassandra-driver 3.24
- NetworkX 2.4



#### Python Installation

###### General Python:

```sh
pip3 install --upgrade pip

pip3 install setuptools

sudo apt-get install python3 python3-pip ipython3 build-essential python-dev python3-dev
```



###### NetworkX:

```sh
pip3 install networkx

pip3 install matplotlib

sudo apt install graphviz

pip3 install pydot
```



###### DSE Graph:

This is for the driver. You will need a DSE Graph 6.8.4 backend.

```sh
pip3 install cassandra-driver[graph]
```

