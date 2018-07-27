# CLOUD SPANNER
## Setup
To use Google Cloud Spanner you need to have Google account.  
After that you are able to activate the coupon of the DB Seminar.  
For that purpose go to: https://console.cloud.google.com/education  

If everything works as expected you have 100$ for your intentions.

### gcloud
To interact with the Google Cloud from your own device you need to install the gcloud tool.  
The installation is described on: https://cloud.google.com/sdk/gcloud/  
Don't forget to initialize gloud after the installation. The command is listed below.  
```bash
gcloud init
```

If gcloud is initialised you are ready to set up a project as you see in:  
https://cloud.google.com/spanner/docs/getting-started/set-up

### Python
The first steps using Cloud Spanner in combination with Python are described under:  
https://cloud.google.com/spanner/docs/getting-started/python/

The repository python-docs-samples provides examples for the basic usage.
The main dependencies are:  
```
google-cloud-spanner==1.3.0
futures==3.2.0; python_version < "3"
```