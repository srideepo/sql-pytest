import pytest
import textwrap
from app.exceptions import ItemNotFoundError

def test_udf_1_total_row_count(db_instance_empty, cursor):

    #--// load test data //--
    insert_test_data_sql = textwrap.dedent('''
        INSERT INTO TestTable (ID, Name)
        SELECT 1, 'Test Name 1' UNION
        SELECT 2, 'Test Name 2'
    ''')
    db_instance_empty.insert_rows_as_sql(cursor=cursor, stmt=insert_test_data_sql)

    #--// execute action dmls //--
    #execute_procedure

    #--// validate test case //--
    stmt = textwrap.dedent('''
        SELECT * FROM udf_TestFn ()
    ''')      
    cursor.execute(stmt)
    rs = cursor.fetchall()
    assert len(rs) == 2

def test_udf_1_distinct_row_count(db_instance_empty, cursor):

    #--// load test data //--
    insert_test_data_sql = textwrap.dedent('''
        INSERT INTO TestTable (ID, Name)
        SELECT 1, 'Test Name 1' UNION
        SELECT 1, 'Test Name 1'
    ''')
    db_instance_empty.insert_rows_as_sql(cursor=cursor, stmt=insert_test_data_sql)

    #--// execute action dmls //--
    #execute_procedure

    #--// validate test case //--
    stmt = textwrap.dedent('''
        SELECT * FROM udf_TestFn ()
    ''')      
    cursor.execute(stmt)
    rs = cursor.fetchall()
    assert len(rs) == 1