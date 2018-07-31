# Database Seminar HSR, Fall 2018: CLOUD SPANNER
## Setup
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
To setup the Cloud Spanner instance and the database use the spanner_setup.py

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
