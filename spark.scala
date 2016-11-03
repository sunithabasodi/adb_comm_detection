import org.apache.spark.graphx._
import org.apache.spark.rdd.RDD
val fb_dir="Dataset\facebook"
val circles = sc.textFile(fb_dir+"\\"+"0"+".circles")
val circlesRDD

case class spark.pycircles(circleID: String, nodeIDs: Seq[Int])
case class edges(to: Int, from: Int)
case class feat(nodeID: Int, features: Seq[Int])
case class egofeat(egoID: Int, features: Seq[Int])
case class featnames(featureID: Int, features_names:Seq[String])

case class egoNet [egoNetID, circles:circles,edges:edges,feat:feat,egofeat:egofeat,featnames:featnames]
