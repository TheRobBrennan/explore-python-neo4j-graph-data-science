from graphdatascience import GraphDataScience

# Connect to the database (ex. Neo4j Desktop on macOS)
# Please see https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/ for a quick visual guide on installing the Neo4j Graph Database Science plug-in to your database
host = "bolt://localhost:7687"
user = "neo4j"
password = "yoloyolo"

gds = GraphDataScience(host, auth=(user, password), database="neo4j")

# By default, Neo4j restricts which directories are allowed to contain data to be imported
# Please refer to the Neo4j documentation at https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/#load-csv-import-data-from-a-remote-csv-file for changes to be made to your database configuration file
#   -> See the comments identified as `# 2023.09.03 => ` in `neo4j/neo4j.conf` for changes I made to work with my local environment

# LOAD CSV Cypher documentation - https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/

# Load stations as nodes
gds.run_cypher(
    """
    LOAD CSV WITH HEADERS FROM 'file:///Users/rob/repos/explore-python-neo4j-graph-data-science/data/nr-stations-all.csv' AS station
    MERGE (:Station {name: station.name, crs: station.crs})
    """
)

# Load tracks between stations as relationships
gds.run_cypher(
    """
  LOAD CSV WITH HEADERS FROM 'file:///Users/rob/repos/explore-python-neo4j-graph-data-science/data/nr-station-links.csv' AS track
  MATCH (from:Station {crs: track.from})
  MATCH (to:Station {crs: track.to})
  MERGE (from)-[:TRACK {distance: round( toFloat(track.distance), 2)}]->(to)
  """
)

gds.close()
