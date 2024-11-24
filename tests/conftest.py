import os
import pytest
import textwrap
import pyodbc
from app.db import DB

# --// BEGIN BOOTSTRAP CONFIGURATION ----------------------------------------------//
#STEP 1. set values for app configuration
#bootstrap the env file to load configuration
from dotenv import load_dotenv

#app configuration provided in a file named "config/.env"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
envdir = os.path.join(BASEDIR, f'../config/.env')
load_dotenv(dotenv_path = os.path.join(BASEDIR, f'../config/.env'))

# --// END BOOTSTRAP CONFIGURATION ----------------------------------------------//

@pytest.fixture
def db_instance(scope="session"):
    """
    Create a DB Instance
    """
    db = DB(os.environ.get("MSSQLDB_CONN_STR"))
    yield db


@pytest.fixture
def connection(db_instance, scope="session"):
    """
    Create a Session, close after test session, uses `db_instance` fixture
    """
    connection = db_instance.connection
    yield connection
    #connection.rollback()
    connection.close()

@pytest.fixture
def cursor(connection, scope="session"):
    """
    Create a Session, close after test session, uses `db_instance` fixture
    """
    cursor = connection.cursor()
    yield cursor
    cursor.rollback()
    cursor.close()

@pytest.fixture
def db_instance_empty(db_instance, cursor, scope="function"):
    """
    Create an Empty DB Instance, uses `db_instance` and `session` fixtures
    """
    # Clear DB before test function
    db_instance.delete_all_rows(cursor=cursor)
    yield db_instance

    # Clear DB after test function
    #db_instance.delete_all_items(cursor=cursor)
