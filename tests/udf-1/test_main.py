import pytest
import textwrap
from app.exceptions import ItemNotFoundError

def test_udf_1_total_row_count(db_instance_empty, cursor):

    #--// load test data //--
    stmt = textwrap.dedent('''
        CREATE TABLE TestTable(ID int, Name varchar(25));
        INSERT INTO TestTable (ID, Name)
        SELECT 1, 'Test Name 1' UNION
        SELECT 2, 'Test Name 2'
    ''')
    db_instance_empty.execute_sql(cursor=cursor, stmt=stmt)
    
    stmt = textwrap.dedent('''
        CREATE FUNCTION udf_TestFn () RETURNS TABLE AS RETURN(SELECT DISTINCT * FROM TestTable);
    ''')
    db_instance_empty.execute_sql(cursor=cursor, stmt=stmt)

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
    stmt = textwrap.dedent('''
        INSERT INTO TestTable (ID, Name)
        SELECT 1, 'Test Name 1' UNION
        SELECT 1, 'Test Name 1' UNION
        SELECT 3, 'Test Name 3'
    ''')
    db_instance_empty.execute_sql(cursor=cursor, stmt=stmt)

    #--// execute action dmls //--
    #execute_procedure

    #--// validate test case //--
    stmt = textwrap.dedent('''
        SELECT * FROM udf_TestFn ()
    ''')      
    rs = db_instance_empty.execute_sql(cursor=cursor, stmt=stmt)
    assert len(rs) == 3