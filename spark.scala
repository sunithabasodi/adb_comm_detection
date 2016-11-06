val FB_DATA="Dataset/facebook/"
val TW_DATA="Dataset/twitter/"
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD
import scala.math.abs
import breeze.linalg.SparseVector
import org.graphstream.graph.{Graph => GraphStream}
object FacebookEgoGraph {
  def main(args: Array[String]) {
    val sc = new SparkContext("local", "Facebook ego net on graphx")
    val graph = GraphLoader.edgeListFile(sc,FB_DATA+"facebook_combined.txt", numEdgePartitions = 4)
    graph.vertices.foreach(v => println(v))
    println("Number of vertices : " + graph.vertices.count())
    println("Number of edges : " + graph.edges.count())
    println("Triangle counts :" + graph.connectedComponents.triangleCount().vertices.collect().mkString("\n"));
  }
}
