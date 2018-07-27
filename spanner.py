import os
import argparse

from google.cloud import spanner
from subprocess import call


def set_credentials(path_to_json_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_json_file


def run(args):
    #    create_instance()
    create_database(args)


def create_instance(args):
    create_instance_command = 'gcloud spanner instances create {0} --config={1} --description={2} --nodes={3}'.format(
        args.instance_id, args.instance_config, args.instance_description, args.number_of_nodes)
    call(create_instance_command)


def create_database(args):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(args.instance_id)

    database = instance.database(args.database_name, ddl_statements=[
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
            )PRIMARY KEY (id)
        """
    ])

    operation = database.create()

    print('Waiting for operation to complete...')
    operation.result()

    print('Created database {} on instance {}'.format(
        args.database_name, args.instance_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Cloud Spanner script for the DB Seminar HSR, Fall 2018',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--credentials', dest='credentials', help='Path to the JSON credential file')
    parser.add_argument('-i', '--instance_id', dest='instance_id', help='Instance ID')
    parser.add_argument('-r', '--region', dest='region', help='Instance deployment region')
    parser.add_argument('-n', '--nodes', dest='region', help='Number of nodes')
    parser.add_argument('-d', '--description', dest='region', help='Instance description')
    parser.add_argument('-db', '--database_name', dest='region', help='Database name')

    parser.set_defaults(credentials='credentials.json', instance_id='paris-instance', region='regional-europe-west1',
                        nodes=1, description='db_seminar', database_name='your')
    args = parser.parse_args()
    set_credentials(args.credentials)
    run(args)
