import os
import argparse
import time

from google.cloud import spanner

queries = ["""
            SELECT cab_type_id,
                   Count(*)
            FROM   trips
            GROUP  BY 1;
           """,
           """
           SELECT passenger_count,
                  Avg(total_amount)
           FROM   trips
           GROUP  BY 1;
           """,
           """
           SELECT passenger_count,
                  Extract(year FROM pickup_datetime),
                  Count(*)
           FROM   trips
           GROUP  BY 1,
                     2;
           """,
           """
           SELECT passenger_count,
                  Extract(year FROM pickup_datetime),
                  Cast(trip_distance AS INT),
                  Count(*)
           FROM   trips
           GROUP  BY 1,
                     2,
                     3
           ORDER  BY 2,
                     4 DESC;
           """,

           """
           SELECT *
           FROM   trips
           WHERE  ( pickup_longitude BETWEEN -74.007511 AND -73.983479 )
                  AND ( pickup_latitude BETWEEN 40.7105 AND 40.731071 ) LIMIT 10;
           """,
           """
           SELECT Extract(hour FROM pickup_datetime) AS h,
                  Avg(Round(trip_distance / NULLIF(Date_part('hour',
                                                       dropoff_datetime - pickup_datetime),
                                            0)))
                                                    AS speed
           FROM   trips
           WHERE  ( pickup_longitude BETWEEN -74.007511 AND -73.983479 )
                  AND ( pickup_latitude BETWEEN 40.7105 AND 40.731071 )
                  AND trip_distance > 0
                  AND fare_amount / trip_distance BETWEEN 2 AND 10
                  AND dropoff_datetime > pickup_datetime
                  AND cab_type_id = 1
           GROUP  BY h
           ORDER  BY h;
           """,
           """
           SELECT Extract(hour FROM pickup_datetime) AS h,
                  Avg(Round(trip_distance / NULLIF(Date_part('hour',
                                                       dropoff_datetime - pickup_datetime),
                                            0)))
                                                    AS speed
           FROM   trips
           WHERE  trip_distance > 0
                  AND fare_amount / trip_distance BETWEEN 2 AND 10
                  AND dropoff_datetime > pickup_datetime
                  AND cab_type_id = 1
           GROUP  BY h
           ORDER  BY h;
           """,
           """
           SELECT Extract(dow FROM pickup_datetime) AS dow,
                  Avg(Round(trip_distance / NULLIF(Date_part('hour',
                                                       dropoff_datetime - pickup_datetime),
                                            0)))
                                                    AS speed
           FROM   trips
           WHERE  trip_distance > 0
                  AND fare_amount / trip_distance BETWEEN 2 AND 10
                  AND dropoff_datetime > pickup_datetime
                  AND cab_type_id = 1
           GROUP  BY dow
           ORDER  BY dow;
           """,
           """
           SELECT Extract(dow FROM pickup_datetime) AS dow,
                  Avg(Round(trip_distance / NULLIF(Date_part('hour',
                                                       dropoff_datetime - pickup_datetime),
                                            0)))
                                                    AS speed
           FROM   trips
           WHERE  ( pickup_longitude BETWEEN -74.007511 AND -73.983479 )
                  AND ( pickup_latitude BETWEEN 40.7105 AND 40.731071 )
                  AND trip_distance > 0
                  AND fare_amount / trip_distance BETWEEN 2 AND 10
                  AND dropoff_datetime > pickup_datetime
                  AND cab_type_id = 1
           GROUP  BY dow
           ORDER  BY dow;
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
