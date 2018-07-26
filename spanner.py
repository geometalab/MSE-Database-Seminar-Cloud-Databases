from google.cloud import spanner
from subprocess import call

database_name = 'york'
instance_id = 'red-dominion-109811'


def run():
    command = 'gcloud sql databases create {}'.format(database_name).split()
    call(command)

    spanner_client = spanner.Client()
    instance = spanner_client.instance(instance_id)

    database = instance.database(database_name)

    # Execute a simple SQL statement.
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql('SELECT 1')

        for row in results:
            print(row)
            # [END spanner_quickstart]


if __name__ == '__main__':
    run()
