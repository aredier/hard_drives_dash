import json
import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if os.environ.get('CHARIOTS_LOCAL') == 'true':
    engine = create_engine('postgresql://aredier2@localhost:5432/mydb')
else:
    with open('../credentials.json', 'r') as credential_file:
        credentials = json.load(credential_file)
    engine = create_engine(
        # Equivalent URL:
        sqlalchemy.engine.url.URL(
            drivername='postgres+pg8000',
            username=credentials['db_user'],
            password=credentials['db_password'],
            database='postgres',
            query={
                'unix_sock': '/cloudsql/{}/.s.PGSQL.5432'.format(
                    'chariots-poc:us-central1:maindb')
            }
        ),
    )

Session = sessionmaker(bind=engine)


def get_session():
    return Session()

