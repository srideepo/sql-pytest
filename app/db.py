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
            --DELETE FROM TestTable
            SELECT 1
        ''')        
        cursor.execute(stmt) 

    def execute_sql(self, cursor, stmt) -> list:
        """
        Execute sql

        Args:
            cursor (pyodbc.cursor): The connection cursor

        Returns:
            None
        """
        logger.info("Executing sql")
        cursor.execute(stmt)
        try:
            rs = cursor.fetchall()
            return rs
        except:
            return None
