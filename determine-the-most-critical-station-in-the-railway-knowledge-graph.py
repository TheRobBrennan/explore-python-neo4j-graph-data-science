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
    f"\nThe most critical station in our railway knowledge graph (based on the highest centrality) is: {n['s.name'][0]}\n"
)

gds.close()
