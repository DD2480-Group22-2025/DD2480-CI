""" 
Small library for querying the build history database.
Database should be a sqlite3 database and is assumed to be named CI.db
and lie in the project root directory.
The functions do not handle errors and will pass them on to calling 
functions.
"""
import sqlite3, datetime, os
db_file = "database/CI.db"
time_format = "%Y-%m-%d"


def database_query(query):
    """Wrapper for database queries
    For now it only makes sure that the database exists.
    """
    def query_wrapper(*args, **kwargs):
        # For more information: https://www.sqlite.org/fileformat.html 
        assert os.path.isfile(db_file), "Could not find the database file."
        assert os.path.getsize(db_file) >= 100, "Not sqlite3 database." # Min header size
        with open(db_file, 'rb') as db_fd:
            assert db_fd.read(16) == b'SQLite format 3\x00', "Not sqlite3 database."

        result = query(*args, **kwargs)
        return result

    return query_wrapper

@database_query
def get_entries():
    """Return a list of all existing build logs"""
    query = "SELECT * FROM build_log"
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result

@database_query
def get_entry_by_commit(commit_hash : str):
    """Queries database for entry with specified hashsum"""
    query = "SELECT * FROM build_log WHERE commit_hash = (?)"
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute(query, (commit_hash,))
    result = cur.fetchall()
    conn.close()
    return result

@database_query
def get_entry_by_id(build_id : int):
    """Queries database for entry with specified rowid"""
    query = "SELECT * FROM build_log WHERE rowid = (?)"
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute(query, (build_id,))
    result = cur.fetchall()
    conn.close()
    return result

@database_query
def get_entries_by_date(build_date : str):
    """Queries database for all entries made on specified date. Dates should
    be in the form YYYY-mm-dd.
    """
    query = "SELECT * FROM build_log WHERE build_date = (?)"
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    cur.execute(query, (build_date,))
    result = cur.fetchall()
    conn.close()
    return result

@database_query
def create_new_entry(commit_hash : str, build_log : str):
    """Create a new entry in CI.db with a given commit hashsum and build log
    Will throw assertion error if an existing build_log has the same hashsum
    """
    query = "INSERT INTO build_log(commit_hash, build_date, build_log) VALUES (?, ?, ?)"
    conn = sqlite3.connect(db_file)
    cur  = conn.cursor()
    build_date = datetime.datetime.today().strftime(time_format)
    assert get_entry_by_commit(commit_hash) == []   # No earlier build with same SHA-sum
    cur.execute(query, (commit_hash, build_log, build_date))
    conn.commit()
    print(cur.fetchall())
    conn.close()
