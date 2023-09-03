import config
from graphdatascience import GraphDataScience

gds = GraphDataScience(
    config.host, auth=(config.user, config.password), database="neo4j"
)

# Create a projection called "trains" that will be stored in the graph catalog for later use
# - The node_spec parameter is a MATCH clause that returns the node IDs of all stations
# - The relationship_spec parameter is a MATCH clause that returns the node IDs of source and target stations ALONG WITH a distance property for the TRACK relationships that will connect stations in the projection
#
# Once executed the projection is stored in the graph catalog and ready for experimentation
gds.graph.project.cypher(
    graph_name="trains",
    node_spec="MATCH (s:Station) RETURN id(s) AS id",
    relationship_spec="""
    MATCH (s1:Station)-[t:TRACK]->(s2:Station)
    RETURN id(s1) AS source, id(s2) AS target, t.distance AS distance
    """,
)

gds.close()
