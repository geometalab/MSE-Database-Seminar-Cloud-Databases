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
```

## Dashboard
To get an overview of your Google Clouds Services have a look at:  
* https://console.cloud.google.com/home/
* https://console.cloud.google.com/apis