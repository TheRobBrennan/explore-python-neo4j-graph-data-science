from graphdatascience import GraphDataScience

# Connect to the database (ex. Neo4j Desktop on macOS)
# Please see https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/ for a quick visual guide on installing the Neo4j Graph Database Science plug-in to your database
host = "bolt://localhost:7687"
user = "neo4j"
password = "yoloyolo"

# Authenticate to our knowledge graph
gds = GraphDataScience(host, auth=(user, password), database="neo4j")

bham = gds.find_node_id(["Station"], {"name": "Birmingham New Street"})
eboro = gds.find_node_id(["Station"], {"name": "Edinburgh"})

shortest_path = gds.shortestPath.dijkstra.stream(
    gds.graph.get("trains"),
    sourceNode=bham,
    targetNode=eboro,
    relationshipWeightProperty="distance",
)

# Cypher query to display the details of the shortest path between two stations using our "trains" graph projection:
#   stations - An array of station names along the route
#   costs - An array containing the accumulating cost of the route based on the distance value between each segment
# -------------------------------------------------------------------------------------------------------------------
# MATCH (bham:Station {name: 'Birmingham New Street'}), (eboro:Station {name: 'Edinburgh'})
# CALL gds.shortestPath.dijkstra.stream('trains', {
#   sourceNode: id(bham),
#   targetNode: id(eboro),
#   relationshipWeightProperty: 'distance'
# })
# YIELD nodeIds, costs
# RETURN [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS stations, costs

print("Shortest distance: %s" % shortest_path.get("costs").get(0)[-1])

gds.close()
