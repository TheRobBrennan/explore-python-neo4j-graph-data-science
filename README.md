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

### Database configuration

If you would like to follow along with this example, please make sure you following steps:

- Step 1 - Configure your Neo4j database configuration to allow importing files within your development environment
- Step 2 - Install the Graph Data Science Library plug-in

#### Step 1 - Configure your Neo4j database configuration to allow importing files within your development environment

By default, Neo4j restricts import from the `import` folder associated with your particular graph database. Please see the guide on [Modifying settings for the DBMS](https://neo4j.com/developer/neo4j-desktop/#desktop-DBMS-settings) so that you can make the following changes to your `neo4j.conf` file for your specific graph database:

```sh
# ...

# 2023.09.03 => Uncommented so that we can import from file URLs when loading data from our local environment
dbms.security.allow_csv_import_from_file_urls=true

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
# Update load_csv_data_into_neo4j.py to match the credentials you chose when creating your Neo4j graph database
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

```python
(.venv) % python3 load_csv_data_into_neo4j.py

# OPTIONAL: On macOS and Linux, you can see how long it takes to execute the script with "time"
(.venv) % time python3 load_csv_data_into_neo4j.py
python3 load_csv_data_into_neo4j.py  0.87s user 1.63s system 52% cpu 4.779 total
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
