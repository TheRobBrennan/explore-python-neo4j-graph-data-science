from graphdatascience import GraphDataScience

# Connect to the database (ex. Neo4j Desktop on macOS)
host = "bolt://localhost:7687"
user = "neo4j"
password = "yoloyolo"

# Authenticate to our knowledge graph
gds = GraphDataScience(host, auth=(user, password), database="neo4j")

graph = gds.graph.get("trains")
result = gds.betweenness.write(graph, writeProperty="betweenness")

total_stations = gds.run_cypher("MATCH (s:Station) RETURN count(s) AS total_stations")
print(f"\nTotal number of stations: {total_stations.iloc[0, 0]}")

processed_stations = gds.run_cypher(
    """
  MATCH (s:Station)
  WHERE s.betweenness IS NOT NULL
  RETURN count(s) AS stations_processed
  """
)
print(f"Number of stations with betweenness score: {processed_stations.iloc[0, 0]}\n")

gds.close()
