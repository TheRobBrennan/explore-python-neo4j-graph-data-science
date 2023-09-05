import config
from graphdatascience import GraphDataScience

gds = GraphDataScience(
    config.host, auth=(config.user, config.password), database="neo4j"
)

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

"""
// VERIFY: Cypher code to calculate the Betweenness Centrality score for nodes in the `trains` projected graph and write it back to the Station nodes as a new `betweenness` property
CALL gds.betweenness.write('trains', {
  writeProperty: 'betweenness'
})
"""

"""
// DELETE the betweenness property from all Station nodes
MATCH (s:Station)
REMOVE s.betweenness
RETURN count(s) as nodesUpdated
"""

gds.close()
