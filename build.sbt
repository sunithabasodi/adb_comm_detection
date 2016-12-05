name := "ADB Communit Detection in Apache Spark"

version := "1.0"

scalaVersion := "2.11.8"

libraryDependencies ++= Seq(
	"org.apache.spark" %% "spark-core" % "1.4.0",
  "org.apache.spark" %% "spark-graphx" % "1.4.0",
  "org.apache.spark" %% "spark-rdd" % "1.4.0",
  "breeze.linalg.{SparseVector, DenseVector}",
  "scala.io.Source",
  "scala.math.abs"

)

resolvers += "Akka Repository" at "http://repo.akka.io/releases/"
