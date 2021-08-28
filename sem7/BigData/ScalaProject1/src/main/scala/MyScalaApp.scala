
object MyScalaApp extends App {

  val test = sqlContext.read.format("csv").
    option("inferSchema", "true").
    option("header", "true").
    option("sep", "\t").
    load("/data/listings.tsv").
    select($"neighbourhood", $"neighbourhood_group").
    groupBy($"neighbourhood").
    count().
    cache()


}
