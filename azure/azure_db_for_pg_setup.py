import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from subprocess import call, run, PIPE

table_names = dict(cab_types='cab_types', trips='trips')


def main_run(args):
    create_resource_group(args=args)
    create_postgres_server(args=args)
    allow_all_ips(args=args)
    create_database(args=args)
    connection = connect_to_db(args=args)
    cursor = connection.cursor()
    create_tables(cursor=cursor)


def create_resource_group(args):
    list_resource_command = 'az group create -l westeurope -n {}'.format(args.resource_group_name).split()
    call(list_resource_command)


def create_postgres_server(args):
    list_create_command = 'az postgres server create -g {0} -n {1}  -l westeurope -u {2} -p {3} --sku-name B_Gen4_1 --version 10.0 --storage-size 51200'.format(
        args.resource_group_name, args.postgres_server_name, args.user, args.password).split()
    call(list_create_command)


def allow_all_ips(args):
    list_create_command = 'az postgres server firewall-rule create -g {} -s {} -n allowall --start-ip-address 0.0.0.0 --end-ip-address 255.255.255.255'.format(
        args.resource_group_name, args.postgres_server_name, args.user, args.password).split()
    call(list_create_command)


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


def create_database(args):
    ssl_mode = 'require' if args.ssl else None
    connection = psycopg2.connect(database='postgres', user=get_user(args), password=args.password, host=get_host(args),
                                  port=args.port, sslmode=ssl_mode)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS {};".format(args.database_name))
    cursor.execute("CREATE DATABASE {};".format(args.database_name))


def create_tables(cursor):
    cab_types = 'cab_types'
    delete_table_if_exists(cursor=cursor, table_name=cab_types)
    cursor.execute(
        "CREATE TABLE {} (cab_type_id INTEGER PRIMARY KEY, cab_type VARCHAR(512));".format(table_names['cab_types']))
    print('Create table {}.'.format(table_names['cab_types']))

    cab_types = 'trips'
    delete_table_if_exists(cursor=cursor, table_name=cab_types)
    cursor.execute("""
        CREATE TABLE trips(
            trip_id SERIAL PRIMARY KEY,
            cab_type_id INTEGER references cab_types(cab_type_id),
            passenger_count INTEGER,
            pickup_datetime TIMESTAMP,
            dropoff_datetime TIMESTAMP,
            pickup_longitude REAL,
            pickup_latitude REAL,
            dropoff_longitude REAL,
            dropoff_latitude REAL,
            trip_distance REAL,
            fare_amount REAL,
            total_amount REAL);""".format(table_names['trips']))
    print('Create table {}.'.format(table_names['trips']))


def delete_table_if_exists(cursor, table_name):
    cursor.execute("DROP TABLE IF EXISTS {};".format(table_name))


def delete(args):
    list_delete_command = 'az group delete -n {}'.format(args.resource_group_name).split()
    call(list_delete_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=' Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--postgres_server_name', dest='postgres_server_name', help='Postgres server name.')
    parser.add_argument('-r', '--resource_group_name', dest='resource_group_name', help='Resource group name.')
    parser.add_argument('-u', '--user', dest='user', help='Username')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Databasename')
    parser.add_argument('-p', '--password', dest='password', help='Password')
    parser.add_argument('--delete', dest='delete', help='Delete all.', action='store_true')
    parser.add_argument('--ssl', dest='ssl', help='Use SSL.', action='store_true')
    parser.add_argument('--port', dest='port', help='Port', type=int)

    parser.set_defaults(database_name='york', port=5432, user='test', password='..DSka6D.!',
                        resource_group_name='DbSeminar', postgres_server_name='dbseminarserver')
    args = parser.parse_args()

    if args.delete:
        delete(args)
    else:
        main_run(args)
