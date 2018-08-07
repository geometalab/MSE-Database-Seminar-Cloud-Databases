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
    connection = psycopg2.connect(database=args.database_name, user=args.user, password=args.password, host=args.host,
                                  port=args.port, sslmode=ssl_mode)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return connection


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=' Azure Database for PostgreSQL-Server for the DB Seminar HSR, Fall 2018',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-a', '--host', dest='host', help='Host address.')
    parser.add_argument('-u', '--user', dest='user', help='Username')
    parser.add_argument('-db', '--database_name', dest='database_name', help='Databasename')
    parser.add_argument('-p', '--password', dest='password', help='Password')
    parser.add_argument('--ssl', dest='ssl', help='Use SSL.', action='store_true')
    parser.add_argument('--port', dest='port', help='Port', type=int)

    parser.set_defaults(database_name='york', host='mydemoserver.postgres.database.azure.com', port=5432,
                        user='mylogin@mydemoserver', password='test123')
    args = parser.parse_args()

    main_run(args)
