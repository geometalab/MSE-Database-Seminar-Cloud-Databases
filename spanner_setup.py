import os
import argparse

from google.cloud import spanner
from subprocess import call, run, PIPE


def set_credentials(path_to_json_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_json_file


def main_run(args):
    create_instance(args)
    spanner_client = spanner.Client()
    instance = spanner_client.instance(args.instance_id)

    create_database(instance=instance, database_name=args.database_name)


def create_instance(args):
    list_instances_command = 'gcloud spanner instances list'.split()
    answer = run(list_instances_command, stdout=PIPE).stdout.decode('utf-8')
    if args.instance_id not in answer:
        create_instance_command = 'gcloud spanner instances create {0} --config={1} --description={2} --nodes={3}'.format(
            args.instance_id, args.region, args.description, args.nodes).split()
        call(create_instance_command)


def create_database(instance, database_name):
    for db in instance.list_databases():
        db.drop()
    database = instance.database(database_name, ddl_statements=[
        """CREATE TABLE cab_types (
            cab_type_id INT64 NOT NULL,
            cab_type    STRING(1024)
            ) PRIMARY KEY (cab_type_id)
        """,
        """
            CREATE TABLE trips (
              cab_type_id INT64 NOT NULL,
              trip_id INT64 NOT NULL,
              passenger_count INT64,
              pickup_datetime TIMESTAMP,
              dropoff_datetime TIMESTAMP,
              pickup_longitude FLOAT64,
              pickup_latitude FLOAT64,
              dropoff_longitude FLOAT64,
              dropoff_latitude FLOAT64,
              trip_distance FLOAT64,
              fare_amount FLOAT64,
              total_amount FLOAT64
            )PRIMARY KEY (cab_type_id, trip_id),
            INTERLEAVE IN PARENT cab_types ON DELETE CASCADE
        """
    ])

    operation = database.create()
    print('Waiting for operation to complete...')
    operation.result()


def delete_spanner_instance(instance_id):
    delete_command = 'gcloud spanner instances delete {}'.format(instance_id).split()
    call(delete_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Cloud Spanner script for the DB Seminar HSR, Fall 2018',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--credentials', dest='credentials', help='Path to the JSON credential file')
    parser.add_argument('-i', '--instance_id', dest='instance_id', help='Instance ID')
    parser.add_argument('-r', '--region', dest='region', help='Instance deployment region')
    parser.add_argument('-n', '--nodes', dest='region', help='Number of nodes')
    parser.add_argument('-d', '--description', dest='region', help='Instance description')
    parser.add_argument('-db', '--database_name', dest='region', help='Database name')
    parser.add_argument('--delete', dest='delete', help='Delete Cloud Spanner instance.', action='store_true')

    current_directory = os.path.realpath(os.path.dirname(__file__))
    parser.set_defaults(credentials='credentials.json', instance_id='paris-instance', region='regional-europe-west1',
                        nodes=1, description='db_seminar', database_name='york')
    args = parser.parse_args()

    set_credentials(args.credentials)
    if args.delete:
        delete_spanner_instance(args.instance_id)
    else:
        main_run(args)
