import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        print("Trying to connect to sqlite db=[{}] ...".format(db_file))
        conn = sqlite3.connect(db_file)
        print("  -> SUCCESS connected! sqlite3.version=[{}]".format(sqlite3.version))
    except Error as e:
        print("  -> FAILED to connect! error=[{}]".format(e))
        if conn:
            conn.close()
    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"/Users/malo/Desktop/myConduiteAccompagnee/@sandboxes/2.serverWithDatabase/mcaDatabase.db"

    sql_create_drivingsessions_table = """ CREATE TABLE IF NOT EXISTS drivingsessions (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create drivingsessions table
        print("Creation de la table ...")
        create_table(conn, sql_create_drivingsessions_table)
        print("  -> SUCCESS")
       
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()


