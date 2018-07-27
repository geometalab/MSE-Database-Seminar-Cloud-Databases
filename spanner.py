import os
import argparse

from google.cloud import spanner
from subprocess import call

database_name = 'york'
instance_id = 'paris-instance'
instance_config = 'regional-europe-west1'
number_of_nodes = 1
instance_description = 'db_seminar'
project_id = 'red-dominion-109811'
region = 'europe-west1'


def set_credentials(path_to_json_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_json_file


def run():
    #    create_instance()
    create_database()


def create_instance():
    create_instance_command = 'gcloud spanner instances create {0} --config={1} --description={2} --nodes={3}'.format(
        instance_id, instance_config, instance_description, number_of_nodes)
    call(create_instance_command)


def create_database():
    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_name, ddl_statements=[
        """
            CREATE TABLE trips (
              id INT64,
              cab_type_id INT64,
              passenger_count INT64,
              pickup_datetime timestamp,
              dropoff_datetime timestamp,
              pickup_longitude FLOAT64,
              pickup_latitude FLOAT64,
              dropoff_longitude FLOAT64,
              dropoff_latitude FLOAT64,
              trip_distance FLOAT64,
              fare_amount FLOAT64,
              total_amount FLOAT64
            )PRIMARY KEY (id);
        """
    ])

    operation = database.create()

    print('Waiting for operation to complete...')
    operation.result()

    print('Created database {} on instance {}'.format(
        database_name, instance_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Cloud Spanner script for the DB Seminar HSR, Fall 2018', )
    parser.add_argument('-c', '--credentials', dest='credentials', help='Path to the JSON credential file')
    parser.set_defaults(credentials='credentials.json')
    args = parser.parse_args()
    set_credentials(args.credentials)
    run()
