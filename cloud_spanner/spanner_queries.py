import os
import argparse
import time

from google.cloud import spanner

queries = ["""
            SELECT cab_type_id,
                   COUNT(*)
            FROM   trips
            GROUP  BY 1;
           """,
           """
           SELECT passenger_count,
                  Avg(total_amount)
           FROM   trips
           GROUP  BY 1;
           """
           ]


def set_credentials(path_to_json_file):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path_to_json_file


def main_run(args):
    spanner_client = spanner.Client()
    instance = spanner_client.instance(args.instance_id)

    do_queries(instance=instance, database_id=args.database_name)


def do_queries(instance, database_id):
    database = instance.database(database_id)

    for i, query in enumerate(queries):
        with database.snapshot() as snapshot:
            start_time = time.time()
            results = snapshot.execute_sql(query)
            print('Query {} to seconds:'.format(i, (time.time() - start_time)))
            print('Result:')
            for row in results:
                print(row)
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Cloud Spanner script for the DB Seminar HSR, Fall 2018',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-c', '--credentials', dest='credentials', help='Path to the JSON credential file')
    parser.add_argument('-i', '--instance_id', dest='instance_id', help='Instance ID')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Database name')

    parser.set_defaults(credentials='credentials.json', instance_id='paris-instance', database_name='york')
    args = parser.parse_args()

    set_credentials(args.credentials)
    main_run(args)
