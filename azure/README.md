# Azure Database for PostgreSQL-Server 
## Goal
Your goal is to use and edit the script examples of the azure directory to benchmark all the queries from the queries.sql file in the queries folder.

## Getting started
First you have to register your HSR account for the Microsoft Azure products.   
For that purpose visit: https://office365.hsr.ch/

### Azure
After the registration you are able to go to the azure portal.  
Reachable at: https://portal.azure.com

### Python
The first steps using Azure in combination with Python are described under:  
https://docs.microsoft.com/en-us/azure/postgresql/connect-python

The main dependencies are (as you can see in the requirements.txt):  
```
psycopg2==2.7.5
pandas==0.23.3
```

To install them use the command:
```
$ pip install -r requirements.txt
```

### Setup Azure
To setup the Cloud Spanner instance and the database use the spanner_setup.py.
The usage is listed below. For most of the values the defaults are fitting and are the same in the other scripts.  
It is important to provide an credentials file (JSON) which is available from the Google Cloud.

```
$ python azure_db_for_pg_setup.py --help
usage: azure_db_for_pg_setup.py [-h] [-a HOST] [-u USER] [-db DATABASE_NAME]
                                [-p PASSWORD] [--delete] [--ssl] [--port PORT]

Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -a HOST, --host HOST  Host address. (default:
                        mydemoserver.postgres.database.azure.com)
  -u USER, --user USER  Username (default: mylogin@mydemoserver)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Databasename (default: york)
  -p PASSWORD, --password PASSWORD
                        Password (default: test123)
  --delete              Delete database. (default: False)
  --ssl                 Use SSL. (default: False)
  --port PORT           Port (default: 5432)

```

#### Example Usage
```
$ python azure_db_for_pg_setup.py
```
Don't forget to delete your database after the usage.
Since the running instances are pricey.

```
$ python azure_db_for_pg_setup.py --delete
```

### Import the data
After the database has been set up we are ready to import the downloaded data.
For that purpose the azure_data_import.py script exists. The usage is listed below:

```
$ python azure_db_for_pg_data_import.py --help
usage: azure_db_for_pg_data_import.py [-h] [-a HOST] [-u USER]
                                      [-db DATABASE_NAME] [-p PASSWORD]
                                      [-s SOURCE] [--port PORT] [--ssl]

Azure Database for PostgreSQL-Server script for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -a HOST, --host HOST  Host address. (default:
                        mydemoserver.postgres.database.azure.com)
  -u USER, --user USER  Username (default: mylogin@mydemoserver)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Databasename (default: york)
  -p PASSWORD, --password PASSWORD
                        Password (default: test123)
  -s SOURCE, --source SOURCE
                        Data directory (default:
                        /home/murthy/projects/ifs/MSE-Database-Seminar-Cloud-
                        Databases/data/)
  --port PORT           Port (default: 5432)
  --ssl                 Use SSL. (default: False)
```

#### Example Usage
```
$ python azure_db_for_pg_data_import.py
```
Since there is a lot of data you have to be a little bit pessant.


### Query the data
To query the data there is the azure_queries.py. 
It provides an example of how to query Azure Database for PostgreSQL-Server from a python script and two example queries.
The usage is listed below:
```
$ python azure_db_for_pg_queries.py --help
usage: azure_db_for_pg_queries.py [-h] [-a HOST] [-u USER] [-db DATABASE_NAME]
                                  [-p PASSWORD] [--ssl] [--port PORT]

Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -a HOST, --host HOST  Host address. (default:
                        mydemoserver.postgres.database.azure.com)
  -u USER, --user USER  Username (default: mylogin@mydemoserver)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Databasename (default: york)
  -p PASSWORD, --password PASSWORD
                        Password (default: test123)
  --ssl                 Use SSL. (default: False)
  --port PORT           Port (default: 5432)
```

#### Example Usage
```
$ python azure_db_for_pg_queries.py
```

