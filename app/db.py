"""
Database Operations for the Task Manager
"""
import os
from typing import List
from datetime import datetime, timezone
from app.exceptions import ItemNotFoundError
from app.logger import create_logger
import pyodbc
import urllib
import textwrap

# Extract the filename without extension
filename = os.path.splitext(os.path.basename(__file__))[0]
logger = create_logger(logger_name=filename)

class DB:
    def __init__(self, conn_str:str):
        # Create DB connection
        self.connection = pyodbc.connect(conn_str)

        cursor = self.connection.cursor()

        # Create DB objects (if needs priming)
        cursor.execute(textwrap.dedent('''
            CREATE TABLE TestTable(ID int, Name varchar(25))
        '''))
        cursor.execute(textwrap.dedent('''
            CREATE FUNCTION udf_TestFn ()
            RETURNS TABLE
            AS
            RETURN(
                SELECT DISTINCT * FROM TestTable
            )
        ''')) 

    def delete_all_rows(self, cursor) -> None:
        """
        Delete all data from the database

        Args:
            cursor (pyodbc.cursor): The connection cursor

        Returns:
            None
        """
        logger.info("Deleting all data from DB")
        stmt = textwrap.dedent('''
            DELETE FROM TestTable
        ''')        
        cursor.execute(stmt) 

    def insert_rows(self, cursor) -> None:
        """
        Delete all data from the database

        Args:
            cursor (pyodbc.cursor): The connection cursor

        Returns:
            None
        """
        logger.info("Insert rows into DB")
        stmt = textwrap.dedent('''
            INSERT INTO TestTable (ID, Name)
            SELECT 1, 'Name 1' UNION
            SELECT 2, 'Name 2'
        ''')         
        cursor.execute(stmt) 


    def insert_rows_as_sql(self, cursor, stmt) -> None:
        """
        Insert data into database

        Args:
            cursor (pyodbc.cursor): The connection cursor

        Returns:
            None
        """
        logger.info("Inserting data into DB")
        cursor.execute(stmt) 
