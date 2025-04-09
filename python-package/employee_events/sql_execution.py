from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).resolve().parent / "employee_events.db"

# OPTION 1: MIXIN
# Define a class called `QueryMixin`


class QueryMixin:

    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, query: str, params=None) -> pd.DataFrame:
        """Executes an SQL query and returns the result as a Pandas DataFrame."""
        with connect(db_path) as conn:
            return pd.read_sql_query(query, conn, params=params)

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, query: str) -> list[tuple]:
        """Executes an SQL query and returns the result as a list of tuples."""
        with connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return result

# Leave this code unchanged


def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        with connect(db_path) as connection:
            cursor = connection.cursor()
            result = cursor.execute(query_string).fetchall()
        return result

    return run_query
