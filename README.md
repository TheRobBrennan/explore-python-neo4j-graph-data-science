# Welcome

This project will explore getting started developing with [Python](https://www.python.org) and Neo4j [Graph Data Science](https://neo4j.com/docs/graph-data-science/current/algorithms/) (GDS) as quickly as possible using [Visual Studio Code](https://code.visualstudio.com).

## Local development

### Install dependencies and run our project

```sh
# Verify that you have Python installed on your machine
% python3 --version
Python 3.11.1

# Create a new virtual environment for the project
% python3 -m venv .venv

# Activate your virtual environment
% source .venv/bin/activate
(.venv) %

# Select your new environment by using the Python: Select Interpreter command in VS Code
#   - Enter the path: ./.venv/bin/python

# Install Python packages in a virtual environment
# EXAMPLE: Install simplejson - https://pypi.org/project/simplejson/
# % pip3 install simplejson
# ... continue to install packages as needed ...

# When you are ready to generate a requirements.txt file
# % pip3 freeze > requirements.txt

# What happens if you want to uninstall a package?

# Uninstall the package from your virtual environment
# % pip3 uninstall simplejson

# Remove the dependency from requirements.txt if it exists
# % pip3 uninstall -r requirements.txt

# Install the packages from requirements.txt
(.venv) % pip3 install -r requirements.txt

# OPTIONAL: Deactivate your Python Virtual Environment
(.venv) % deactivate
%

# OPTIONAL: Delete your Python Virtual Environment
% rm -r .venv
```

That's it! Now, if you re-run the program - with or without the debugger - your Python script should have executed.

## EXAMPLE: Explore Neo4j Graph Data Science

For this example, I'm using the freely available [Neo4j Desktop](https://neo4j.com/download/) app on macOS Ventura 13.5.1 (22G90).

Please follow the guide at [https://neo4j.com/developer/neo4j-desktop/](https://neo4j.com/developer/neo4j-desktop/) if you are just getting started with [Neo4j Desktop](https://neo4j.com/download/).

TL;DR Already comfortable with having an empty graph database set up? Simply update `config.py` with your credentials and run the desired script(s):

- Load data into your graph database - [load-csv-data-into-neo4j.py](./load-csv-data-into-neo4j.py)
  - Configure Neo4j so that you can import files
  - Specify the full path for importing files
- Create a graph projection using Neo4j Graph Data Science - [create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py](./create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py)
  - Find the shortest path between two stations - [find-the-shortest-path-between-two-stations.py](./find-the-shortest-path-between-two-stations.py)
  - Determine the most critical station in the graph - [determine-the-most-critical-station-in-the-railway-knowledge-graph.py](./determine-the-most-critical-station-in-the-railway-knowledge-graph.py)
  - Compute centrality scores for all Station nodes and write those scores back as a new `betweenness` property - [compute-centrality-scores-for-all-railway-stations-in-our-knowledge-graph.py](./compute-centrality-scores-for-all-railway-stations-in-our-knowledge-graph.py)

### Database configuration

If you would like to follow along with this example, please make sure you following steps:

- Step 1 - Configure your Neo4j database configuration to allow importing files within your development environment
- Step 2 - Install the Graph Data Science Library plug-in

#### Step 1 - Configure your Neo4j database configuration to allow importing files within your development environment

By default, Neo4j restricts import from the `import` folder associated with your particular graph database. Please see the guide on [Modifying settings for the DBMS](https://neo4j.com/developer/neo4j-desktop/#desktop-DBMS-settings) so that you can make the following changes to your `neo4j.conf` file for your specific graph database:

```sh
# ...

# 2023.09.03 => Sets the root directory for file:/// URLs used with the Cypher LOAD CSV clause. This should be set to a single directory
# relative to the Neo4j installation path on the database server. All requests to load from file:/// URLs will then be relative to the
# specified directory. The default value set in the config settings is import. This is a security measure which prevents the database from
# accessing files outside the standard import directory, similar to how a Unix chroot operates. Setting this to an empty field will allow
# access to all files within the Neo4j installation folder. Commenting out this setting will disable the security feature, allowing
# all files in the local system to be imported. This is definitely not recommended.
# server.directories.import=import

# 2023.09.03 => This setting determines if Cypher will allow the use of file:/// URLs when loading data using LOAD CSV.
# Such URLs identify files on the filesystem of the database server. Default is true. Setting dbms.security.allow_csv_import_from_file_urls=false
# will completely disable access to the file system for LOAD CSV.
dbms.security.allow_csv_import_from_file_urls=true

# ...

```

#### Step 2 - Install the Graph Data Science Library plug-in

Please see the guide at [https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/](https://neo4j.com/docs/graph-data-science/current/installation/neo4j-desktop/) for instructions on install the Neo4j Graph Data Science Library plug-in for your graph database.

![https://neo4j.com/docs/graph-data-science/current/_images/neo4j-desktop-gds.png](https://neo4j.com/docs/graph-data-science/current/_images/neo4j-desktop-gds.png)

### Load CSV data into your Neo4j graph database

We're ready to load data into our Neo4j graph database 🤓

Assuming you have started your graph database - a locally-running Neo4j Desktop database in this example - please make sure you following steps:

- Step 1 - Create the Python virtual environment
- Step 2 - Install our dependencies
- Step 3 - Update the installation script
- Step 4 - Load data into our Neo4j graph database
- Step 5 - Explore your database using Neo4j Browser

#### Step 1 - Create the Python virtual environment

```sh
# Verify that you have Python installed on your machine
% python3 --version
Python 3.11.1

# Create a new virtual environment for the project
% python3 -m venv .venv

```

#### Step 2 - Install our dependencies

```sh
# Activate your virtual environment
% source .venv/bin/activate
(.venv) %

# Select your new environment by using the Python: Select Interpreter command in VS Code
#   - Enter the path: ./.venv/bin/python

# Install the packages from requirements.txt
(.venv) % pip3 install -r requirements.txt
```

#### Step 3 - Update the installation script

##### Update information to connect to your Neo4j graph database

```python
# Update config.py to match the credentials you chose when creating your Neo4j graph database
host = "bolt://localhost:7687"
user = "neo4j"
password = "yoloyolo"
```

##### Specify the full path for importing files

If you would like to import data from your local environment, please be sure to use the full path to the files on your system:

Replace `file:///Users/rob/repos/explore-python-neo4j-graph-data-science/data/` with `file:///path/to/my/repo/explore-python-neo4j-graph-data-science/data/`

```python
# ...

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

# ...
```

#### Step 4 - Load data into our Neo4j graph database

Let's load our data:

```sh
(.venv) % python3 load-csv-data-into-neo4j.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 load-csv-data-into-neo4j.py
python3 load-csv-data-into-neo4j.py  0.87s user 1.63s system 52% cpu 4.779 total
```

#### Step 5 - Explore your database using Neo4j Browser

##### View all nodes within your graph database

```cypher
// Return all nodes (n) in your Neo4j graph database
MATCH (n) RETURN n

// NOTE: Depending on your settings and the number of nodes within your graph database, you may receive a warning message of `Not all return nodes are being displayed due to Initial Node Display setting. Only first 300 nodes are displayed.`
```

##### Delete all nodes and relationships within your graph database

```cypher
// Delete all nodes and relationships in your Neo4j graph database
MATCH (n) DETACH DELETE n
```

### Use Neo4j Graph Data Science (GDS) to create an example graph projection

Let's use the example railway knowledge graph to create our first graph project using Neo4j Graph Data Science (GDS)

First, update `create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py` to match the credentials to connect to your Neo4j graph database

```python
# create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py
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
```

Let's run our script to create this example projection:

```sh
(.venv) % python3 create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 create-a-neo4j-gds-graph-projection-from-the-railway-knowledge-graph.py
Loading: 100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 100.0/100 [00:00<00:00, 4372.53%/s]
python3   1.16s user 1.32s system 231% cpu 1.075 total
```

#### Use Neo4j Graph Data Science (GDS) to find the shortest path between two stations

Using the `trains` Neo4j Graph Data Science (GDS) projection from above, let's find the shortest path between two stations:

```sh
(.venv) % python3 find-the-shortest-path-between-two-stations.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 find-the-shortest-path-between-two-stations.py
Station: Birmingham New Street (Cost: 0.00)
Station: Smethwick Galton Bridge (Cost: 3.91)
Station: Sandwell & Dudley (Cost: 5.16)
Station: Dudley Port (Cost: 7.12)
Station: Tipton (Cost: 8.01)
Station: Coseley (Cost: 9.39)
Station: Wolverhampton (Cost: 12.70)
Station: Penkridge (Cost: 22.30)
Station: Stafford (Cost: 28.01)
Station: Crewe (Cost: 52.27)
Station: Winsford (Cost: 59.81)
Station: Hartford (Cheshire) (Cost: 64.10)
Station: Acton Bridge (Cheshire) (Cost: 66.77)
Station: Warrington Bank Quay (Cost: 76.42)
Station: Wigan North Western (Cost: 88.16)
Station: Euxton Balshaw Lane (Cost: 96.52)
Station: Leyland (Cost: 99.27)
Station: Preston (Lancs) (Cost: 103.30)
Station: Lancaster (Cost: 124.34)
Station: Oxenholme Lake District (Cost: 143.43)
Station: Penrith (North Lakes) (Cost: 175.59)
Station: Carlisle (Cost: 193.44)
Station: Lockerbie (Cost: 219.27)
Station: Carstairs (Cost: 267.11)
Station: Kirknewton (Cost: 284.86)
Station: Curriehill (Cost: 289.36)
Station: Wester Hailes (Cost: 290.96)
Station: Kingsknowe (Cost: 292.05)
Station: Slateford (Cost: 292.93)
Station: Haymarket (Cost: 294.67)
Station: Edinburgh (Cost: 295.91)

Starting Station: Birmingham New Street
Ending Station: Edinburgh

Shortest distance from Birmingham New Street to Edinburgh involves visiting 31 station(s) for a total distance of 295.91

python3 find-the-shortest-path-between-two-stations.py  1.15s user 1.21s system 429% cpu 0.549 total
```

#### Use Neo4j Graph Data Science (GDS) to find the most critical station on the rail network

SCENARIO: Birmingham New Street is a busy hub station that serves routes across Great Britain - including routes that intersect Edinburgh in the Scottish lowlands. You might suspect this is the most critical station on the rail network. Before advocating for significant funding to improve the most vital station and surrounding track in Great Britain, you would like to double-check your assumption and verify (or debunk) the Birmingham New Street station's importance in the rail network using centrality.

Using the `trains` Neo4j Graph Data Science (GDS) projection from above, let's find the most critical station on the rail network in Great Britain.

```sh
(.venv) % python3 determine-the-most-critical-station-in-the-railway-knowledge-graph.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 determine-the-most-critical-station-in-the-railway-knowledge-graph.py

The most critical station in our railway knowledge graph (based on the highest centrality) is: Tamworth

python3 determine-the-most-critical-station-in-the-railway-knowledge-graph.py  0.90s user 1.47s system 338% cpu 0.701 total
```

Tamworth - located just a few miles away from Birmingham - has the highest centrality score and so the greatest impact on the rail network in the case of failures.

### Enriching the knowledge graph

The centrality score we calculated would be useful if it were contained within our knowledge graph - particularly if we wanted to use that centrality for future use cases (such as machine learning)/

Using the `trains` Neo4j Graph Data Science (GDS) projection from above, let's write the centrality scores of our Station nodes back to the underlying knowledge graph as a new `betweenness` property.

```sh
(.venv) % python3 compute-centrality-scores-for-all-railway-stations-in-our-knowledge-graph.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 compute-centrality-scores-for-all-railway-stations-in-our-knowledge-graph.py

Total number of stations: 2593
Number of stations with betweenness score: 2593

python3   0.96s user 1.50s system 359% cpu 0.684 total

```
