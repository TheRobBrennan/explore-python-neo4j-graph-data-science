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

# Select your new environment by using the Python: Select Interpreter command in VS Code
#   - Enter the path: ./.venv/bin/python

# Activate your virtual environment
% source .venv/bin/activate
(.venv) %

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
