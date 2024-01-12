import aiosqlite
import os

class Database:
    def __init__(self, logger):
        self.logger = logger
        # Set the database path directly in the Database class
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'DATA', 'bot_database.db')
        self.connection = None

    async def init_db(self):
        # Check if the database file exists, if not, create it
        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()
            self.logger.info("DATABASE: Database file created.")

        # Initialize connection
        self.connection = await aiosqlite.connect(self.db_path)

        # Read and execute schema.sql to create/update tables
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            await self.connection.executescript(schema_sql)
            await self.connection.commit()
            self.logger.info("DATABASE: Initialized with necessary tables.")

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
            self.logger.info("DATABASE: Connection closed.")