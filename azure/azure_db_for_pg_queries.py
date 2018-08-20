import argparse
import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

table_names = dict(cab_types='cab_types', trips='trips')

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


def main_run(args):
    connection = connect_to_db(args=args)
    cursor = connection.cursor()
    do_queries(cursor=cursor)


def do_queries(cursor):
    for i, query in enumerate(queries):
        start_time = time.time()
        cursor.execute(query)
        print('Query {} took {} seconds:'.format(i, (time.time() - start_time)))
        print('Result:')
        for record in cursor:
            print(record)
        print()


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=' Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', '--postgres_server_name', dest='postgres_server_name', help='Postgres server name.')
    parser.add_argument('-u', '--user', dest='user', help='Username')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Databasename')
    parser.add_argument('-p', '--password', dest='password', help='Password')
    parser.add_argument('--ssl', dest='ssl', help='Use SSL.', action='store_true')
    parser.add_argument('--port', dest='port', help='Port', type=int)

    parser.set_defaults(database_name='york', postgres_server_name='dbseminarserver', port=5432,
                        user='test', password='..DSka6D.!')
    args = parser.parse_args()

    main_run(args)
