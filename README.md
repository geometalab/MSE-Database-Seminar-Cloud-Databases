# Database Seminar HSR, Fall 2018: CLOUD SPANNER

## Getting started
To use Google Cloud Spanner you need to have Google account.  
After that you are able to activate the coupon of the DB Seminar.  
For that purpose go to: https://console.cloud.google.com/education  

If everything works as expected you have 100$ for your intentions.

### gcloud
To interact with the Google Cloud from your own device you need to install the gcloud tool.  
The installation is described on: https://cloud.google.com/sdk/gcloud/  
Don't forget to initialize gloud and set the project id after the installation. The commands are listed below.  
```bash
gcloud init
gcloud config set project [MY_PROJECT_ID]
```

If gcloud is initialised you are ready to set up a project as you see in:  
https://cloud.google.com/spanner/docs/getting-started/set-up  

### Python
The first steps using Cloud Spanner in combination with Python are described under:  
https://cloud.google.com/spanner/docs/getting-started/python/  

The repository python-docs-samples provides examples for the basic usage.  
The main dependencies are (as you can see in the requirements.txt):  
```
google-cloud-spanner==1.3.0
futures==3.2.0; python_version < "3"
pandas==0.23.3
```

To install them use the command:
```
$ pip install -r requirements.txt
```

## Dashboard
To get an overview of your Google Clouds Services have a look at:  
* https://console.cloud.google.com/home/
* https://console.cloud.google.com/apis

## Data
The data we are using for the current Database Seminar are the New York City Taxi trips. (http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml)

### Download
Downloadable CSV files are provided on Amazon S3.
We do only focus on the data from 2015 of the yellow and green taxis.
To download them switch into the data directory and execute the download.py script.
Since it is still a lot of data this may take a while.
```
$ cd data
$ python download.py 
```
After that your data folder should provide the CSV files.

### Setup Cloud Spanner
To setup the Cloud Spanner instance and the database use the spanner_setup.py.
The usage is listed below. For most of the values the defaults are fitting and are the same in the other scripts.  
It is important to provide an credentials file (JSON) which is available from the Google Cloud.

```
$ python spanner_setup.py --help
usage: spanner_setup.py [-h] [-c CREDENTIALS] [-i INSTANCE_ID] [-r REGION]
                        [-n NODES] [-d DESCRIPTION] [-db DATABASE_NAME]
                        [--delete]

Google Cloud Spanner script for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        Path to the JSON credential file (default:
                        credentials.json)
  -i INSTANCE_ID, --instance_id INSTANCE_ID
                        Instance ID (default: paris-instance)
  -r REGION, --region REGION
                        Instance deployment region (default: regional-europe-
                        west1)
  -n NODES, --nodes NODES
                        Number of nodes (default: 1)
  -d DESCRIPTION, --description DESCRIPTION
                        Instance description (default: db_seminar)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Database name (default: york)
  --delete              Delete Cloud Spanner instance. (default: False)
```

#### Example Usage
```
$ python spanner_setup.py
```
Don't forget to delete your instances after the usage.
Since the running instances are pricey.

```
$ python spanner_setup.py --delete
```

### Import the data
After the database has been set up we are ready to import the downloaded data.
For that purpose the spanner_data_import.py script exists. The usage is listed below:

```
$ python spanner_data_import.py --help
usage: spanner_data_import.py [-h] [-c CREDENTIALS] [-i INSTANCE_ID]
                              [-db DATABASE_NAME] [-s SOURCE]

Google Cloud Spanner script for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        Path to the JSON credential file (default:
                        credentials.json)
  -i INSTANCE_ID, --instance_id INSTANCE_ID
                        Instance ID (default: paris-instance)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Database name (default: york)
  -s SOURCE, --source SOURCE
                        Data directory (default: data/)
```

#### Example Usage
```
$ python spanner_data_import.py
```
Since there is a lot of data you have to be a little bit pessant.


### Query the data
To query the data there is the spanner_queries.py. 
It provides an example of how to query Cloud Spanner from a python script and two example queries.
The usage is listed below:
```
$ python spanner_queries.py --help
usage: spanner_queries.py [-h] [-c CREDENTIALS] [-i INSTANCE_ID]
                          [-db DATABASE_NAME]

Google Cloud Spanner script for the DB Seminar HSR, Fall 2018

optional arguments:
  -h, --help            show this help message and exit
  -c CREDENTIALS, --credentials CREDENTIALS
                        Path to the JSON credential file (default:
                        credentials.json)
  -i INSTANCE_ID, --instance_id INSTANCE_ID
                        Instance ID (default: paris-instance)
  -db DATABASE_NAME, --database_name DATABASE_NAME
                        Database name (default: york)
```

#### Example Usage
```
$ python spanner_data_queries.py
```

## Goal
Your goal is now to use and edit the script examples to benchmark all the queries from the queries.sql file in the queries folder.
Be aware of the SQL syntax the queries.sql is written in PostgreSQL syntax and has to be adopted for Cloud Spanner.