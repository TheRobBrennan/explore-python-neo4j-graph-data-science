import config
from graphdatascience import GraphDataScience

gds = GraphDataScience(
    config.host, auth=(config.user, config.password), database="neo4j"
)

bham = gds.find_node_id(["Station"], {"name": "Birmingham New Street"})
eboro = gds.find_node_id(["Station"], {"name": "Edinburgh"})

shortest_path = gds.shortestPath.dijkstra.stream(
    gds.graph.get("trains"),
    sourceNode=bham,
    targetNode=eboro,
    relationshipWeightProperty="distance",
)

# Extract nodeIds and costs from the shortest_path result
nodeIds = shortest_path.get("nodeIds").get(0)
costs = shortest_path.get("costs").get(0)

# Fetch station names and print stations and costs for each stop along the route
stations = [gds.util.asNode(nodeId).get("name") for nodeId in nodeIds]
for station, cost in zip(stations, costs):
    print(f"Station: {station} (Cost: {'{:.2f}'.format(cost)})")

# Print starting and ending stations
print("\nStarting Station:", stations[0])
print("Ending Station:", stations[-1])

print(
    "\nShortest distance from {} to {} involves visiting {} station(s) for a total distance of {}\n".format(
        stations[0], stations[-1], len(stations), "{:.2f}".format(costs[-1])
    )
)

"""
// VERIFY: Cypher code to display the shortest path between BHM and EDB

MATCH (bhm:Station {crs:"BHM"}), (edb:Station {crs:"EDB"})
CALL gds.shortestPath.dijkstra.stream('trains', {sourceNode:bhm, targetNode:edb, relationshipWeightProperty:'distance'})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
"""

gds.close()
