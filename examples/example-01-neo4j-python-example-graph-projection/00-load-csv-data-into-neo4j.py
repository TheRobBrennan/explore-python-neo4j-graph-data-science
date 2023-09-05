import config
from graphdatascience import GraphDataScience

gds = GraphDataScience(
    config.host, auth=(config.user, config.password), database="neo4j"
)

# By default, Neo4j restricts which directories are allowed to contain data to be imported
# Please refer to the Neo4j documentation at https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/#load-csv-import-data-from-a-remote-csv-file for changes to be made to your database configuration file
#   -> See the comments identified as `# 2023.09.03 => ` in `neo4j/neo4j.conf` for changes I made to work with my local environment

# LOAD CSV Cypher documentation - https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/

# Load stations as nodes
gds.run_cypher(
    """
    LOAD CSV WITH HEADERS FROM 'file:///Users/rob/repos/explore-python-neo4j-graph-data-science/examples/example-01-neo4j-python-example-graph-projection/data/nr-stations-all.csv' AS station
    MERGE (:Station {name: station.name, crs: station.crs})
    """
)

# Load tracks between stations as relationships
gds.run_cypher(
    """
  LOAD CSV WITH HEADERS FROM 'file:///Users/rob/repos/explore-python-neo4j-graph-data-science/examples/example-01-neo4j-python-example-graph-projection/data/nr-station-links.csv' AS track
  MATCH (from:Station {crs: track.from})
  MATCH (to:Station {crs: track.to})
  MERGE (from)-[:TRACK {distance: round( toFloat(track.distance), 2)}]->(to)
  """
)

gds.close()
