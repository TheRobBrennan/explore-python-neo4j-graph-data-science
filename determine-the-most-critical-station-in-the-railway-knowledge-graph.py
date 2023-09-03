from graphdatascience import GraphDataScience

# Connect to the database (ex. Neo4j Desktop on macOS)
host = "bolt://localhost:7687"
user = "neo4j"
password = "yoloyolo"

# Authenticate to our knowledge graph
gds = GraphDataScience(host, auth=(user, password), database="neo4j")

graph = gds.graph.get("trains")
result = gds.betweenness.stream(graph)
highest_score = (
    result.sort_values(by="score", ascending=False).iloc[0:1]["nodeId"].iloc[0]
)

n = gds.run_cypher(
    f"MATCH (s:Station) WHERE ID(s) = {int(highest_score)} RETURN s.name"
)

print(
    f"\nThe most critical station in our railway knowledge graph (based on the highest centrality) is: {n['s.name'][0]} (score: {result})\n"
)

gds.close()
