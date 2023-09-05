import config
from graphdatascience import GraphDataScience

gds = GraphDataScience(
    config.host, auth=(config.user, config.password), database="neo4j"
)

graph = gds.graph.get("trains")
result = gds.betweenness.stream(graph)
highest_score = (
    result.sort_values(by="score", ascending=False).iloc[0:1]["nodeId"].iloc[0]
)

n = gds.run_cypher(
    f"MATCH (s:Station) WHERE ID(s) = {int(highest_score)} RETURN s.name"
)

print(
    f"\nThe most critical station in our railway knowledge graph (based on the highest Betweenness Centrality) is: {n['s.name'][0]}\n"
)

"""
// VERIFY: Cypher code using Betweenness Centrality to determine the most critical station in the physical rail network
// The Betweenness Centrality example answers the question: "Which train station acts as the most significant bridge or intermediary for the shortest routes between other train stations?"
// A station with a high betweenness centrality score in a train network might indicate a critical hub or transfer point. If such a station were to be removed or if it became inoperative, it could significantly disrupt the efficiency of the network, as many shortest paths would need to be rerouted.

CALL gds.betweenness.stream('trains')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS stationName, score
ORDER BY score DESC
"""

"""
// VERIFY: Cypher code using Degree Centrality (i.e. the Station connected to the most other Stations)
// The Degree Centrality example answers the question: "Which train station is directly connected to the most other train stations?"
// A station with a high degree centrality in a train network indicates that it has many direct routes to other stations. Such a station might be a busy hub where many routes converge, making it a potential hotspot for passenger transfers or a strategic location for scheduling and operations.

CALL gds.degree.stream('trains')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS stationName, score
ORDER BY score DESC
"""

gds.close()
