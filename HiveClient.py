from sqlalchemy import create_engine
from pyhive import hive

from hive.config import DBConfig


class HiveClient():

    def __init__(self):
        """
        Instance initialization.
        """
        url = "hive://{HIVE_USERNAME}@{HIVE_HOST}:{HIVE_PORT}"
        self.engine = create_engine(url.format(
            HIVE_USERNAME=DBConfig.HIVE_USERNAME,
            HIVE_HOST=DBConfig.HIVE_HOST,
            HIVE_PORT=DBConfig.HIVE_PORT
        ))

        self.cursor = hive.Connection(
            host=DBConfig.HIVE_HOST,
            port=DBConfig.HIVE_PORT,
            username=DBConfig.HIVE_USERNAME
        ).cursor()

    def init_db(self):
        """
        Initialize database schema and client connection.
        """
        command = (
            "CREATE TABLE IF NOT EXISTS {TABLE_NAME} {TABLE_SCHEMA} "
            "clustered by (id) into 2 buckets "
            "stored as orc TBLPROPERTIES('transactional'='true')"
        )
        self.engine.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME,
            TABLE_SCHEMA=DBConfig.TABLE_SCHEMA
        ))

    def drop_db(self):
        """
        Drop database.
        """
        command = "DROP TABLE IF EXISTS {TABLE_NAME}"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME
        ))

    def get_schema(self):
        """
        Show database schema.
        """
        command = "SELECT * FROM {TABLE_NAME} LIMIT 1"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME
        ))
        return self.cursor.description

    @staticmethod
    def list_to_bundle(data):
        """
        Transform values data shape from list to sql bundle.
        """
        val_temp = "({ID}, {ADDRESS}, {VALUE})"
        val_list = []
        for row in data:
            val = val_temp.format(
                ID=str(row[0]),
                ADDRESS=str(row[1]),
                VALUE=str(row[2])
            )
            val_list += [val]

        return (", ").join(val_list)

    def create_data(self, data):
        """
        Create data within database
        """
        command = "INSERT INTO TABLE {TABLE_NAME} VALUES {VALUES}"
        bundle = HiveClient.list_to_bundle(data)
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME,
            VALUES=bundle
        ))

    def read_data(self, _id, address, limit):
        """
        Read data within database.
        """
        command = "SELECT * FROM {TABLE_NAME} WHERE id={ID} AND address={ADDRESS} LIMIT {LIMIT}"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME,
            ID=_id,
            ADDRESS=str(address),
            LIMIT=str(limit)
        ))
        return self.cursor.fetchall()

    def update_data(self, _id, address, value):
        """
        Update within database.
        """
        command = "UPDATE {TABLE_NAME} SET value={VALUE} WHERE id={ID} AND address={ADDRESS}"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME,
            VALUE=str(value),
            ID=_id,
            ADDRESS=str(address)
        ))

    def delete_data(self, _id, address):
        """
        Delete data within database.
        """
        command = "DELETE FROM {TABLE_NAME} WHERE id={ID} AND address={ADDRESS}"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME,
            ID=_id,
            ADDRESS=str(address)
        ))

    def delete_mock(self):
        """
        Delete all mock data.
        """
        command = "DELETE FROM {TABLE_NAME} WHERE id<0"
        self.cursor.execute(command.format(
            TABLE_NAME=DBConfig.TABLE_NAME
        ))