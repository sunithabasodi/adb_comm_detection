### We used Apache Spark for loading of the graphs and graph-parallel computation which iseventually stored on a HDFS using native Hadoop libraries and Hive for cluster distribution oftasks to worker nodes. Spark for graphs and graph-parallel computation GraphX extends theSparkRDDby introducing a newGraphabstraction including a growing collection of graphal-gorithmsandbuildersto simplify graph analytics tasks. To support graph computation Graphexposes a set of fundamental operators (e.g.,subgraph,joinVertices, and aggregateMessages).GraphStream is a Java library for the modeling and analysis of dynamic graphs.  We cangenerate, import, export, measure, layout and visualize them.  
## Dataset used SNAP Facebook ego-net & Twitter Ego-Net
## Community detection on complex graph networks using Apache Spark. 

* Available from: https://www.researchgate.net/publication/311645849_Community_detection_on_complex_graph_networks_using_Apache_Spark


# adb_community_detection
community detection in social networks using user and relationship attributes


# Running the viz app

spark-shell --jars ./lib/gs-core-1.3.jar,./lib/gs-algo-1.3.jar,./lib/gs-ui-1.3.jar,./lib/jfreechart-1.0.19-demo.jar spark.scala

## Installation

# Apache Spark

wget http://d3kbcqa49mib13.cloudfront.net/spark-2.0.1-bin-hadoop2.7.tgz

tar xvzf spark-2.0.1-bin-hadoop2.7.tgz

mv spark-2.0.1-bin-hadoop2.7/ spark/

'' Run commands from bin directly or update BIN path.
