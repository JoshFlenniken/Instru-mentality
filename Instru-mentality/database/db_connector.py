import pymysql

from config import Config

# Database credentials are derived from environment variables via Config.
host = Config.DB_HOST
port = Config.DB_PORT
user = Config.DB_USER
passwd = Config.DB_PASSWORD
db = Config.DB_NAME


def connectDB(host=host, port=port, user=user, passwd=passwd, db=db):
    """
    Connects to a database and returns a database connection object.
    """
    dbConnection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=passwd,
        database=db,
        cursorclass=pymysql.cursors.DictCursor,
    )
    return dbConnection

def query(dbConnection=None, query=None, query_params=()):
    """
    Executes a given SQL query on the given db connection and returns a Cursor object.
    You need to run .fetchall() or .fetchone() on that object to access the results.
    """

    if dbConnection is None:
        print("No connection to the database found! Have you called connectDB() first?")
        return None

    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params))

    cursor = dbConnection.cursor()

    cursor.execute(query, query_params)
    dbConnection.commit()

    return cursor