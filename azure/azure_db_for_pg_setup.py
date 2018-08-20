import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from subprocess import call, run, PIPE

table_names = dict(cab_types='cab_types', trips='trips')


def main_run(args):
    create_database(args=args)
    connection = connect_to_db(args=args)
    cursor = connection.cursor()
    create_tables(cursor=cursor)


def create_resource_group(args):
    list_resource_command = 'az group create -l westeurope -n {}'.format(args.resource_group_name).split()
    call(list_resource_command)


def create_postgres_server(args):
    list_create_command = 'az postgres server create -g {0} -n {1}  -l westeurope -u {2} -p {3} --sku-name B_Gen4_1 --version 10.0'.format(
        args.resource_group_name, args.postgres_server_name, args.user, args.password).split()
    call(list_create_command)


def connect_to_db(args):
    ssl_mode = 'require' if args.ssl else None
    connection = psycopg2.connect(database=args.database_name, user=args.user, password=args.password, host=args.host,
                                  port=args.port, sslmode=ssl_mode)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


def create_database(args):
    ssl_mode = 'require' if args.ssl else None
    connection = psycopg2.connect(database='postgres', user=args.user, password=args.password, host=args.host,
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
    connection = connect_to_db(args=args)
    cursor = connection.cursor()
    for _, value in table_names.items():
        delete_table_if_exists(cursor=cursor, table_name=value)
    cursor.execute("DROP DATABASE IF EXISTS {};".format(args.database_name))
    list_delete_command = 'az group delete --name {}'.format(args.resource_group_name)
    call(list_delete_command)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=' Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--host', dest='host', help='Host address.')
    parser.add_argument('-s', '--postgres_server_name', dest='postgres_server_name', help='Postgres server name.')
    parser.add_argument('-r', '--resource_group_name', dest='resource_group_name', help='Resource group name.')
    parser.add_argument('-u', '--user', dest='user', help='Username')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Databasename')
    parser.add_argument('-p', '--password', dest='password', help='Password')
    parser.add_argument('--delete', dest='delete', help='Delete database.', action='store_true')
    parser.add_argument('--ssl', dest='ssl', help='Use SSL.', action='store_true')
    parser.add_argument('--port', dest='port', help='Port', type=int)

    parser.set_defaults(database_name='york', host='mydemoserver.postgres.database.azure.com', port=5432,
                        user='mylogin@mydemoserver', password='test123', resource_group_name='DbSeminar',
                        postgres_server_name='DbSeminarServer')
    args = parser.parse_args()

    if args.delete:
        delete(args)
    else:
        main_run(args)
