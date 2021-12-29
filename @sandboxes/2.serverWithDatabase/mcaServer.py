from flask import Flask
from flask import Response
from flask import request
import sqlite3
from sqlite3 import Error
import uuid



app = Flask(__name__)



#
#
# API (Flask)
#
#



@app.route("/createDrivingSession", methods=['GET'])
def createDrivingSession():
    uuidDrivingSession = MCADrivingSessionService_createDrivingSession() 
    return str(uuidDrivingSession)



@app.route("/deleteDrivingSession/<uuidDeletedDrivingSession>", methods=['GET'])
def deleteDrivingSession(uuidDeletedDrivingSession):
    MCADrivingSessionService_deleteDrivingSession(uuidDeletedDrivingSession)
    return uuidDeletedDrivingSession






#
#
# Service (MCADrivingSessionService)
#
#



def MCADrivingSessionService_createDrivingSession():
    uuidDrivingSession = uuid.uuid4()
    drivingSession = (str(uuidDrivingSession), 'Session Matinale', '2023/12/26Z13:37:37', '2023/12/26Z13:57:45')
    print("Creation session conduite uuidDrivingSession=[{}]".format(uuidDrivingSession))
    MCADataBaseAccess_insertDrivingSession(drivingSession)
    return uuidDrivingSession



def MCADrivingSessionService_deleteDrivingSession(uuidDeletedDrivingSession):
    MCADataBaseAccess_deleteDrivingSession(uuidDeletedDrivingSession)
    print("Destruction session conduite uuidDeletedDrivingSession=[{}]".format(uuidDeletedDrivingSession))
    return uuidDeletedDrivingSession






#
#
# Database access (MCADataBaseAccess)
#
#



def MCADataBaseAccess_insertDrivingSession(drivingSession):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    # create a database connection
    conn = MCADataBaseAccess_create_connection()
    with conn:
        sqlRequest = ''' INSERT INTO drivingsessions(id,name,begin_date,end_date)
                  VALUES(?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sqlRequest, drivingSession)
        conn.commit()
        return cur.lastrowid



def MCADataBaseAccess_deleteDrivingSession(uuidDeletedDrivingSession):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    conn = MCADataBaseAccess_create_connection()
    with conn:
        sql = 'DELETE FROM drivingsessions WHERE id=?'
        cur = conn.cursor()
        cur.execute(sql, (uuidDeletedDrivingSession,))
        conn.commit()


#
# Helper functions
#

def MCADataBaseAccess_create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    database = r"/Users/malo/Desktop/myConduiteAccompagnee/@sandboxes/2.serverWithDatabase/mcaDatabase.db"
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn







if __name__ == "__main__":
    app.run(debug=True)


