import aiosqlite
import os

import datetime
import shutil
import zipfile

class Database:
    def __init__(self, logger):
        self.logger = logger
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'DATA', 'bot_database.db')
        self.connection = None

    async def init_db(self):
        # Check if the database file exists, if not, create it
        if not os.path.exists(self.db_path):
            open(self.db_path, 'w').close()
            self.logger.info("DATABASE: Database file created.")

        # Initialize connection
        self.connection = await aiosqlite.connect(self.db_path)

        # Check if schema.sql file exists
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if not os.path.exists(schema_path):
            self.logger.error("DATABASE: schema.sql file not found.")
            return

        # Read and execute schema.sql to create/update tables
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
            await self.connection.executescript(schema_sql)
            await self.connection.commit()
            self.logger.info("DATABASE: Initialized with necessary tables.")

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
            self.logger.info("DATABASE: Connection closed.")

    async def query_records(self, table_name, select_columns, where_clause=None, where_args=()):
        try:
            columns = ', '.join(select_columns)
            query = f"SELECT {columns} FROM {table_name}"
            if where_clause:
                query += f" WHERE {where_clause}"
            cursor = await self.connection.execute(query, where_args)
            return await cursor.fetchall()
        except Exception as e:
            self.logger.error(f"DATABASE: Error in query_records: {e}")
            return []
        
    #backup_database
    async def backup_database(self):
        try:
            backup_folder = os.path.join(os.path.dirname(__file__), '..', 'BACKUP')
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file_path = os.path.join(backup_folder, 'bot_database.db')
            backup_schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            zip_path = os.path.join(backup_folder, f"{timestamp}.zip")

            # Ensure the database connection is closed before copying
            if self.connection:
                await self.connection.close()

            # Create a ZIP archive
            with zipfile.ZipFile(zip_path, 'w') as backup_zip:
                # Copy and add the database file to the ZIP
                shutil.copyfile(self.db_path, backup_file_path)
                backup_zip.write(backup_file_path, os.path.basename(backup_file_path))

                # Add the schema file to the ZIP
                if os.path.exists(backup_schema_path):
                    backup_zip.write(backup_schema_path, os.path.basename(backup_schema_path))

            # Clean up the temporary database backup file
            os.remove(backup_file_path)

            # Reopen the database connection
            self.connection = await aiosqlite.connect(self.db_path)

            self.logger.info(f"DATABASE: Backup created successfully at {zip_path}")
            return True
        except Exception as e:
            self.logger.error(f"DATABASE: Error creating backup: {e}")
            return False
        
    async def restore_database(self, backup_filename):
        try:
            backup_folder = os.path.join(os.path.dirname(__file__), '..', 'BACKUP')
            zip_path = os.path.join(backup_folder, backup_filename)

            # Check if the backup file exists
            if not os.path.exists(zip_path):
                self.logger.error(f"DATABASE: Backup file {backup_filename} not found.")
                return False

            # Perform a backup before restoring
            if not await self.backup_database():
                self.logger.error("DATABASE: Failed to create a backup before restoration.")
                return False

            # Close the database connection
            if self.connection:
                await self.connection.close()

            # Delete the current database file
            if os.path.exists(self.db_path):
                os.remove(self.db_path)

            # Extract files from the backup ZIP
            with zipfile.ZipFile(zip_path, 'r') as backup_zip:
                backup_zip.extractall(os.path.dirname(self.db_path))

            # Reinitialize the database connection
            self.connection = await aiosqlite.connect(self.db_path)

            self.logger.info(f"DATABASE: Restoration from {backup_filename} completed successfully.")
            return True
        except Exception as e:
            self.logger.error(f"DATABASE: Error during restoration: {e}")
            return False
