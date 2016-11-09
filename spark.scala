val FB_DATA="Dataset/facebook/"
val TW_DATA="Dataset/twitter/"

import org.apache.spark.SparkContext._
import org.apache.spark.graphx._
import org.apache.spark.rdd._
import scala.io.Source
import scala.math.abs
import org.graphstream.graph.{Graph => GraphStream}
import org.graphstream.graph.implementations._
import org.jfree.chart.axis.ValueAxis
import breeze.linalg._
import breeze.plot._
import breeze.linalg.SparseVector

//egoNetwork Edge loader

val FacebookEgoGraph = GraphLoader.edgeListFile(sc,FB_DATA+"facebook_combined.txt", numEdgePartitions = 32)

println("FacebookEgoGraph Loaded")
println("Number of vertices : " + FacebookEgoGraph.vertices.count())
println("Number of edges : " + FacebookEgoGraph.edges.count())
println("Triangle counts :" + FacebookEgoGraph.connectedComponents.triangleCount().vertices.collect().mkString("\n"));

val TwitterEgoGraph = GraphLoader.edgeListFile(sc,TW_DATA+"twitter_combined.txt", numEdgePartitions = 32)

println("TwitterEgoGraph Loaded")
println("Number of vertices : " + TwitterEgoGraph.vertices.count())
println("Number of edges : " + TwitterEgoGraph.edges.count())
println("Triangle counts :" + TwitterEgoGraph.connectedComponents.triangleCount().vertices.collect().mkString("\n"));


//FacebookEgoGraph Visualisation

val fbgraphStream: SingleGraph = new SingleGraph("EgoSocial")
fbgraphStream.addAttribute ("ui.stylesheet","url(file://./style/graphStyleSheet.css)")
fbgraphStream.addAttribute("ui.quality")
fbgraphStream.addAttribute("ui.antialias")


for ((id,_) <- FacebookEgoGraph.vertices.collect()) {
  val node = graphStream.addNode(id.toString).asInstanceOf[SingleNode]
}
for (Edge(x,y,_) <- FacebookEgoGraph.edges.collect()) {
  val edge = graphStream.addEdge(x.toString ++ y.toString,
  x.toString, y.toString,
  true).
  asInstanceOf[AbstractEdge]
}
fbgraphStream.display()


//TwitterEgoGraph Visualisation


val fbgraphStream: SingleGraph = new SingleGraph("EgoSocial")
twgraphStream.addAttribute ("ui.stylesheet","url(file://./style/graphStyleSheet.css)")
twgraphStream.addAttribute("ui.quality")
twgraphStream.addAttribute("ui.antialias")

for ((id,_) <- TwitterEgoGraph.vertices.collect()) {
  val node = graphStream.addNode(id.toString).asInstanceOf[SingleNode]
}
for (Edge(x,y,_) <- TwitterEgoGraph.edges.collect()) {
  val edge = graphStream.addEdge(x.toString ++ y.toString,
  x.toString, y.toString,
  true).
  asInstanceOf[AbstractEdge]
}
twgraphStream.display()




// Load Vertice Data -- Incomplete Parser


FacebookEgoGraph.vertices.foreach(v => println(v))

FacebookEgoGraph.degrees.
map(t=> (t._2,t._1)).
groupByKey.map(t =>(t._1,t._2.size)).
sortBy(_._1).collect()

type Feature = breeze.linalg.SparseVector[Int]

//Only loads one ego network

val featureMap: Map[Long, Feature] =
Source.fromFile(FB_DATA+"0.feat").
getLines().
map{line =>
  val row = line split ' '
  val key = abs(row.head.hashCode.toLong)
  val feat = SparseVector(row.tail.map(_.toInt))
  (key, feat)
}.toMap

val edges: RDD[Edge[Int]] =
sc.textFile(FB_DATA+"0.edges").
map {line =>
val row = line split ' '
val srcId = abs(row(0).hashCode.toLong)
val dstId = abs(row(1).hashCode.toLong)
val srcFeat = featureMap(srcId)
val dstFeat = featureMap(dstId)
val numCommonFeats = srcFeat dot dstFeat
  Edge(srcId, dstId, numCommonFeats)
}

val vertices:  RDD[(VertexId, Feature)] =
	sc.textFile(FB_DATA+"0.edges").
		map{line =>
			val key = abs(line.hashCode.toLong)
			(key, featureMap(key))
}


val egoNetwork: Graph[Int,Int] = Graph.fromEdges(edges, 1)

egoNetwork.edges.filter(_.attr == 3).count()
egoNetwork.edges.filter(_.attr == 2).count()
egoNetwork.edges.filter(_.attr == 1).count()



		// Function for computing degree distribution


    val nn = FacebookEgoGraph.numVertices
    val egoDegreeDistribution = degreeHistogram(FacebookEgoGraph).map({case
      (d,n) => (d,n.toDouble/nn)})
    val f = Figure()
    val p1 = f.subplot(2,1,0)
    val x = new DenseVector(egoDegreeDistribution map (_._1.toDouble))
    val y = new DenseVector(egoDegreeDistribution map (_._2))

    p1.xlabel = "Degrees"
    p1.ylabel = "Distribution"
    p1 += plot(x, y)
    p1.title = "Degree distribution of social ego network"
    val p2 = f.subplot(2,1,1)
    val egoDegrees = FacebookEgoGraph.degrees.map(_._2).collect()
    p1.xlabel = "Degrees"
    p1.ylabel = "Histogram of node degrees"
    p2 += hist(egoDegrees, 10)


def degreeHistogram(net: Graph[Int, Int]): Array[(Int, Int)] =
	FacebookEgoGraph.degrees.map(t => (t._2,t._1)).
		  groupByKey.map(t => (t._1,t._2.size)).
		  sortBy(_._1).collect()



println("Number of vertices : " + FacebookEgoGraph.vertices.count())
println("Number of edges : " + FacebookEgoGraph.edges.count())
println("Triangle counts :" + FacebookEgoGraph.connectedComponents.triangleCount().vertices.collect().mkString("\n"));
