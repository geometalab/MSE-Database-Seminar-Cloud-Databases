import glob
import os
import re
import argparse

import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values

table_names = dict(cab_types='cab_types', trips='trips')

green = 2
yellow = 1
year_month_regex = "tripdata_([0-9]{4})-([0-9]{2})"
yellow_schema_2015_2016_h1 = ['vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
                              'trip_distance', 'pickup_longitude', 'pickup_latitude', 'rate_code_id',
                              'store_and_fwd_flag', 'dropoff_longitude', 'dropoff_latitude', 'payment_type',
                              'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge',
                              'total_amount']

green_schema_2015_h1 = ['vendor_id', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'store_and_fwd_flag',
                        'rate_code_id', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude',
                        'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax,tip_amount',
                        'tolls_amount,ehail_fee', 'improvement_surcharge', 'total_amount', 'payment_type', 'trip_type',
                        'junk1', 'junk2']

green_schema_2015_h2_2016_h1 = ['vendor_id', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'store_and_fwd_flag',
                                'rate_code_id', 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude',
                                'dropoff_latitude', 'passenger_count', 'trip_distance', 'fare_amount', 'extra,mta_tax',
                                'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge', 'total_amount',
                                'payment_type', 'trip_type']


def main_run(args):
    connection = connect_to_db(args=args)
    cursor = connection.cursor()
    # insert_cab_type(cursor=cursor)
    insert_trips(cursor=cursor, data_source=args.source)


def connect_to_db(args):
    ssl_mode = 'require' if args.ssl else None
    connection = psycopg2.connect(database=args.database_name, user=get_user(args), password=args.password,
                                  host=get_host(args), port=args.port, sslmode=ssl_mode)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def get_host(args):
    return '{}.postgres.database.azure.com'.format(args.postgres_server_name)


def get_user(args):
    return '{}@{}'.format(args.user, args.postgres_server_name)


def insert_cab_type(cursor):
    cursor.execute("INSERT INTO {} (cab_type_id, cab_type) VALUES (%s, %s);".format(table_names['cab_types'], yellow),
                   (yellow, u'yellow'))
    cursor.execute("INSERT INTO {} (cab_type_id, cab_type) VALUES (%s, %s);".format(table_names['cab_types'], green),
                   (green, u'yellow'))
    print('Inserted {}.'.format(table_names['cab_types']))


def insert_trips(cursor, data_source):
    os.chdir(data_source)
    cab_type = green
    for file in glob.glob("*.csv"):
        year, month = get_year_month(file)
        schema = None
        if "green" in file:
            if year == 2015 and month < 7:
                schema = green_schema_2015_h1
            else:
                schema = green_schema_2015_h2_2016_h1
        elif "yellow" in file:
            cab_type = yellow
            schema = yellow_schema_2015_2016_h1
        df = load_data(file, schema, cab_type)
        df = convert_data(df)
        values = []
        for _, row in df.iterrows():
            values.append((
                row['cab_type_id'], row['passenger_count'], row['pickup_datetime'], row['dropoff_datetime'],
                row['pickup_longitude'], row['pickup_latitude'], row['dropoff_longitude'], row['dropoff_latitude'],
                row['trip_distance'], row['fare_amount'], row['total_amount']
            ))

        insert_query = """insert into {} (cab_type_id, passenger_count, pickup_datetime, dropoff_datetime, pickup_longitude, 
                                         pickup_latitude, dropoff_longitude, dropoff_latitude, trip_distance, fare_amount, 
                                         total_amount) values %s""".format(table_names['trips'])
        execute_values(cursor, insert_query, values, template=None, page_size=100)
        print('Inserted {} from file {}'.format(table_names['trips'], file))


def convert_data(df):
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropoff_datetime'] = pd.to_datetime(df['dropoff_datetime'])
    df[['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'trip_distance', 'fare_amount',
        'total_amount']] = df[
        ['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude', 'trip_distance', 'fare_amount',
         'total_amount']].astype(float)

    return df


def load_data(file, schema, cab_type):
    df = pd.read_csv(file, names=schema)
    df = df.iloc[1:]
    df = rename_columns(df, cab_type=cab_type)
    df = df.fillna(0.0)
    return df


def rename_columns(df, cab_type=2):
    df['cab_type_id'] = cab_type
    df = add_non_existing_columns(df)
    df = df.rename(columns={'lpep_pickup_datetime': 'pickup_datetime', 'lpep_dropoff_datetime': 'dropoff_datetime',
                            'tpep_pickup_datetime': 'pickup_datetime', 'tpep_dropoff_datetime': 'dropoff_datetime'})
    return df[
        ['cab_type_id', 'passenger_count', 'pickup_datetime', 'dropoff_datetime', 'pickup_longitude', 'pickup_latitude',
         'dropoff_longitude', 'dropoff_latitude', 'trip_distance', 'fare_amount', 'total_amount']]


def add_non_existing_columns(df):
    if 'pickup_longitude' not in df:
        df["pickup_longitude"] = np.nan
    if 'pickup_latitude' not in df:
        df["pickup_latitude"] = np.nan
    if 'pickup_longitude' not in df:
        df["pickup_longitude"] = np.nan
    if 'dropoff_longitude' not in df:
        df["dropoff_longitude"] = np.nan
    if 'dropoff_latitude' not in df:
        df["dropoff_latitude"] = np.nan
    return df


def get_year_month(file):
    match = re.findall(year_month_regex, file)
    year = int(match[0][0])
    month = int(match[0][1])
    return year, month


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=' Azure Database for PostgreSQL-Server script for the DB Seminar HSR, Fall 2018',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--postgres_server_name', dest='postgres_server_name', help='Postgres server name.')
    parser.add_argument('-u', '--user', dest='user', help='Username')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Databasename')
    parser.add_argument('-p', '--password', dest='password', help='Password')
    parser.add_argument('-s', '--source', dest='source', help='Data directory')
    parser.add_argument('--port', dest='port', help='Port', type=int)
    parser.add_argument('--ssl', dest='ssl', help='Use SSL.', action='store_true')

    current_directory = os.path.realpath(os.path.dirname(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    parser.set_defaults(database_name='york', postgres_server_name='dbseminarserver', port=5432,
                        user='test', password='..DSka6D.!', source=parent_directory + "/data/")
    args = parser.parse_args()

    main_run(args)
